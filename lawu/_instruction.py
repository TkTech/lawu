import enum

from itertools import repeat
from struct import unpack, calcsize
from typing import BinaryIO, List, Tuple
from dataclasses import dataclass


class OperandTypes(enum.Enum):
    #: A literal numerical value.
    LITERAL = 'L'
    #: An index into the locals table.
    LOCAL = 'I'
    #: An absolutel or relative offset for the target of a jump.
    BRANCH = 'B'
    #: An index into the constants pool.
    CONSTANT = 'C'
    #: A padding byte, usually used for alignment.
    PADDING = 'P'


@dataclass
class Operand:
    op_type: str
    value: int


class InstructionMeta(type):
    def __repr__(cls):
        return f'<{cls.__name__}(op={cls.op:#04x}, name={cls.name!r})>'

    def __eq__(cls, other):
        return cls is other


class Instruction(metaclass=InstructionMeta):
    """Represents a single Instruction in the JVM specification.
    """
    __slots__ = ('pos', 'operands')

    op: int
    name: str
    mnemonic: str
    can_be_wide: bool
    fmt: List[Tuple[str, str]]

    def __init__(self, *operands, pos=0):
        #: Offset from the start of a Code block, if it is known.
        self.pos: int = pos
        #: List of Operands.
        self.operands: List[Operand] = operands

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}(op={self.op:#04x},'
            f' name={self.name!r}, operands={self.operands!r})>'
        )

    @staticmethod
    def read(source: BinaryIO, *, offset=0) -> 'Instruction':
        """Read and return a single Instruction from `source`.

        If `offset` is provided, it is the offset from the start of the Code
        block. It is required to properly parse the alignment padding on the
        :class:`~lawu.instruction.tableswitch` and
        :class:`lawu.instruction.lookupswitch` instructions.
        """
        # TODO: This is temporary, until _instruction is merged with the
        #       auto-generated instructions.py.
        from lawu.instructions import BY_OP

        op = source.read(1)
        if not op:
            return None

        # TODO: Better error message for unknown opcodes.
        ins = BY_OP[ord(op)]
        ins_operands = []

        # Most opcodes have simple operands that can be parsed with a simple
        # struct format string.
        # Special case the lookupswitch instruction which has variable
        # operands.
        if ins.op == 0xAB:
            # Get rid of the alignment padding.
            padding = (offset + 1) % 4
            padding = (4 - padding) if padding != 4 else 0
            source.read(padding)

            # Default branch address and branch count.
            default, npairs = unpack('>ii', source.read(8))

            pairs = {}
            for _ in repeat(None, npairs):
                match, p_offset = unpack('>ii', source.read(8))
                pairs[match] = p_offset

            ins_operands.append(pairs)
            ins_operands.append(Operand(OperandTypes.BRANCH, default))
        # Special case the tableswitch instruction which has variable
        # operands.
        elif ins.op == 0xAA:
            # Get rid of the alignment padding.
            padding = (offset + 1) % 4
            padding = (4 - padding) if padding != 4 else 0
            source.read(padding)

            default, low, high = unpack('>iii', source.read(12))
            ins_operands.append(Operand(OperandTypes.BRANCH, default))
            ins_operands.append(Operand(OperandTypes.LITERAL, low))
            ins_operands.append(Operand(OperandTypes.LITERAL, high))

            for _ in repeat(None, high - low + 1):
                p_offset = unpack('>i', source.read(4))[0]
                ins_operands.append(Operand(OperandTypes.BRANCH, p_offset))
        # Special case for the wide prefix
        elif ins.op == 0xC4:
            real_op = unpack('>B', source.read(1))[0]
            ins = BY_OP[real_op]

            ins_operands.append(Operand(
                OperandTypes.LOCAL,
                unpack('>H', source.read(2))[0]
            ))
            # Further special case for iinc.
            if real_op == 0x84:
                ins_operands.append(Operand(
                    OperandTypes.LITERAL,
                    unpack('>H', source.read(2))[0]
                ))
        elif ins.operands:
            for size, of_type in ins.fmt:
                ins_operands.append(
                    Operand(
                        OperandTypes(of_type),
                        unpack(size, source.read(calcsize(size)))[0]
                    )
                )

        return ins(*ins_operands, pos=offset)

    def __getitem__(self, idx: int):
        return self.operands[idx]

    def __iteritems__(self):
        yield from self.operands

    @property
    def wide(self) -> bool:
        """True if this instructions needs to be prefixed by the WIDE
        opcode due to the size of its operands.
        """
        if not self.can_be_wide:
            return False

        if self[0].value >= 255:
            return True

        # Special case for IINC.
        if self.op == 0x84:
            if self[1].value >= 255:
                return True

        return False

    def size_on_disk(self, offset=0):
        """
        Returns the size of this instruction and its operands when
        packed.

        If `offset` is provided, it is the offset from the start of the Code
        block. It is required to properly parse the alignment padding on the
        :class:`~lawu.instruction.tableswitch` and
        :class:`lawu.instruction.lookupswitch` instructions.
        """
        # All instructions are at least 1 byte (the opcode itself)
        size = 1

        # Instruction that must be prefied by WIDE before it can be written.
        if self.wide:
            size += 2
            # Special case for iinc which has a 2nd extended operand.
            if self.opcode == 0x84:
                size += 2
        # A simple opcode with simple operands.
        elif self.fmt:
            for fmt, _ in self.fmt:
                size += calcsize(fmt)
        # lookupswitch
        elif self.opcode == 0xAB:
            padding = 4 - (offset + 1) % 4
            padding = padding if padding != 4 else 0
            size += padding
            # default & npairs
            size += 8
            size += len(self[0]) * 8
        # tableswitch
        elif self.opcode == 0xAA:
            raise NotImplementedError()

        return size
