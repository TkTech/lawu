"""
Utilities for reading & writing JVM method bytecode.
"""
import enum
from struct import unpack, pack, Struct
from itertools import repeat
from collections import namedtuple
from lawu.instructions import Instruction, BY_OP

Operand = namedtuple('Operand', ['op_type', 'value'])


class OperandTypes(enum.IntEnum):
    """Constants used to determine the "type" of operand on an opcode.
    """
    #: A numerical literal value.
    LITERAL = 10
    #: A numerical index into the current method's local table.
    LOCAL_INDEX = 20
    #: A numerical index into the constant pool.
    CONSTANT_INDEX = 30
    #: A signed jump offset.
    BRANCH = 40
    #: A padding byte for alignment.
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
            fout.write(fmt.value.pack(operands[i].value))
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
