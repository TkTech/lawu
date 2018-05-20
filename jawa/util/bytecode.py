"""
Utilities for reading & writing JVM method bytecode.
"""
import json
import enum
import pkgutil
from struct import unpack, pack, Struct
from itertools import repeat
from collections import namedtuple

Operand = namedtuple('Operand', ['op_type', 'value'])
_Instruction = namedtuple('Instruction', [
    'mnemonic',
    'opcode',
    'operands',
    'pos'
])


class Instruction(_Instruction):
    """
    Represents a single JVM instruction, consisting
    of an opcode and its potential operands.
    """
    __slots__ = ()

    def size_on_disk(self, start_pos=0):
        """
        Returns the size of this instruction and its operands when
        packed. `start_pos` is required for the `tableswitch` and
        `lookupswitch` instruction as the padding depends on alignment.
        """
        # All instructions are at least 1 byte (the opcode itself)
        size = 1
        fmts = opcode_table[self.opcode]['operands']

        if self.wide:
            size += 2
            # Special case for iinc which has a 2nd extended operand.
            if self.opcode == 0x84:
                size += 2
        elif fmts:
            # A simple opcode with simple operands.
            for fmt, _ in fmts:
                size += fmt.size
        elif self.opcode == 0xAB:
            # lookupswitch
            padding = 4 - (start_pos + 1) % 4
            padding = padding if padding != 4 else 0
            size += padding
            # default & npairs
            size += 8
            size += len(self.operands[0]) * 8
        elif self.opcode == 0xAA:
            # tableswitch
            raise NotImplementedError()

        return size

    @property
    def wide(self):
        """
        ``True`` if this instruction needs to be prefixed by the WIDE
        opcode.
        """
        if not opcode_table[self.opcode].get('can_be_wide'):
            return False

        if self.operands[0].value >= 255:
            return True

        if self.opcode == 0x84:
            if self.operands[1].value >= 255:
                return True

        return False

    @property
    def name(self):
        """Alias for mnemonic."""
        return self.mnemonic

    @property
    def details(self):
        """Extended opcode information."""
        return opcode_table[self.opcode]

    @classmethod
    def create(cls, mnemonic_or_op, operands=None):
        op = opcode_table[mnemonic_or_op]

        return cls(
            op['mnemonic'],
            op['op'],
            operands or [],
            0
        )

    def __eq__(self, other):
        return other == self.mnemonic or super().__eq__(other)


class OperandTypes(enum.IntEnum):
    """
    Constants used to determine the "type" of operand on an opcode,
    such as a BRANCH [offset] or a LITERAL [value].
    """
    LITERAL = 10
    LOCAL_INDEX = 20
    CONSTANT_INDEX = 30
    BRANCH = 40
    PADDING = 50


class OperandFmts(enum.Enum):
    UBYTE = Struct('>B')
    BYTE = Struct('>b')
    USHORT = Struct('>H')
    SHORT = Struct('>h')
    INTEGER = Struct('>i')


def write_instruction(fout, start_pos, ins):
    """
    Writes a single instruction of `opcode` with `operands` to `fout`.

    :param fout: Any file-like object providing ``write()``.
    :param start_pos: The current position in the stream.
    :param ins: The `Instruction` to write.
    """
    opcode, operands = ins.opcode, ins.operands
    fmt_operands = opcode_table[opcode]['operands']

    if ins.wide:
        # The "WIDE" prefix
        fout.write(pack('>B', 0xC4))
        # The real opcode.
        fout.write(pack('>B', opcode))
        fout.write(pack('>H', operands[0].value))
        if opcode == 0x84:
            fout.write(pack('>h', operands[1].value))
    elif fmt_operands:
        # A normal simple opcode with simple operands.
        fout.write(pack('>B', opcode))
        for i, (fmt, _) in enumerate(fmt_operands):
            fout.write(fmt.pack(operands[i].value))
    elif opcode == 0xAB:
        # Special case for lookupswitch.
        fout.write(pack('>B', opcode))
        # assemble([
        #     ('lookupswitch', {
        #         2: -3,
        #         4: 5
        #     }, <default>)
        # ])
        padding = 4 - (start_pos + 1) % 4
        padding = padding if padding != 4 else 0
        fout.write(pack(f'{padding}x'))
        fout.write(pack('>ii', operands[1].value, len(operands[0])))
        for key in sorted(operands[0].keys()):
            fout.write(pack('>ii', key, operands[0][key]))
    elif opcode == 0xAA:
        # Special case for table switch.
        fout.write(pack('>B', opcode))
        padding = 4 - (start_pos + 1) % 4
        padding = padding if padding != 4 else 0
        fout.write(pack(f'{padding}x'))
        fout.write(pack(
            f'>iii{len(operands) - 3}i',
            # Default branch offset
            operands[0].value,
            operands[1].value,
            operands[2].value,
            *(o.value for o in operands[3:])
        ))
    else:
        # opcode with no operands.
        fout.write(pack('>B', opcode))


def read_instruction(fio, start_pos):
    """
    Reads a single instruction from `fio` and returns it, or ``None`` if
    the stream is empty.

    :param fio: Any file-like object providing ``read()``.
    :param start_pos: The current position in the stream.
    """
    op = fio.read(1)

    if not op:
        return None

    op = ord(op)

    ins = opcode_table[op]
    operands = ins['operands']
    name = ins['mnemonic']

    final_operands = []
    # Most opcodes have simple operands.
    if operands:
        for fmt, type_ in operands:
            final_operands.append(
                Operand(
                    type_,
                    fmt.value.unpack(fio.read(fmt.value.size))[0]
                )
            )
    # Special case for lookupswitch.
    elif op == 0xAB:
        # Get rid of the alignment padding.
        padding = 4 - (start_pos + 1) % 4
        padding = padding if padding != 4 else 0
        fio.read(padding)

        # Default branch address and branch count.
        default, npairs = unpack('>ii', fio.read(8))

        pairs = {}
        for _ in repeat(None, npairs):
            match, offset = unpack('>ii', fio.read(8))
            pairs[match] = offset

        final_operands.append(pairs)
        final_operands.append(Operand(OperandTypes.BRANCH, default))
    # Special case for tableswitch
    elif op == 0xAA:
        # Get rid of the alignment padding.
        padding = 4 - (start_pos + 1) % 4
        padding = padding if padding != 4 else 0
        fio.read(padding)

        default, low, high = unpack('>iii', fio.read(12))
        final_operands.append(Operand(OperandTypes.BRANCH, default))
        final_operands.append(Operand(OperandTypes.LITERAL, low))
        final_operands.append(Operand(OperandTypes.LITERAL, high))

        for _ in repeat(None, high - low + 1):
            offset = unpack('>i', fio.read(4))[0]
            final_operands.append(Operand(OperandTypes.BRANCH, offset))
    # Special case for the wide prefix
    elif op == 0xC4:
        real_op = unpack('>B', fio.read(1))[0]
        ins = opcode_table[real_op]
        name = ins['mnemonic']

        final_operands.append(Operand(
            OperandTypes.LOCAL_INDEX,
            unpack('>H', fio.read(2))[0]
        ))
        # Further special case for iinc.
        if real_op == 0x84:
            final_operands.append(Operand(
                OperandTypes.LITERAL,
                unpack('>H', fio.read(2))[0]
            ))

    return Instruction(name, op, final_operands, start_pos)


def load_bytecode_definitions(*, path=None) -> dict:
    """Load bytecode definitions from JSON file.

    If no path is provided the default bytecode.json will be loaded.

    :param path: Either None or a path to a JSON file to load containing
                 bytecode definitions.
    """
    if path is not None:
        with open(path, 'rb') as file_in:
            j = json.load(file_in)
    else:
        try:
            j = json.loads(pkgutil.get_data('jawa.util', 'bytecode.json'))
        except json.JSONDecodeError:
            # Unfortunately our best way to handle missing/malformed/empty
            # bytecode.json files since it may not actually be backed by a
            # "real" file.
            return {}

    for definition in j.values():
        # If the entry has any operands take the text labels and convert
        # them into pre-cached struct objects and operand types.
        operands = definition['operands']
        if operands:
            definition['operands'] = [
                [getattr(OperandFmts, oo[0]), OperandTypes[oo[1]]]
                for oo in operands
            ]

    # Return one dict that contains both mnemonic keys and opcode keys.
    return {**j, **{v['op']: v for v in j.values()}}


opcode_table = load_bytecode_definitions()
