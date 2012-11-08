# -*- coding: utf8 -*-
__all__ = (
    'Instruction',
    'Operand',
    'OperandTypes',
    'read_instruction',
    'write_instruction',
    'opcode_table',
    'definition_from_mnemonic',
    'definition_from_opcode'
)

import struct

from itertools import repeat
from collections import namedtuple

Operand = namedtuple('Operand', ['op_type', 'value'])
_Instruction = namedtuple('Instruction', [
    'mnemonic',
    'opcode',
    'operands',
    'pos'
])

# Opcodes that can be prefixed by the `wide` opcode.
_wide = (
    0x15, 0x17, 0x19, 0x16,
    0x18, 0x36, 0x38, 0x3A,
    0x37, 0x39, 0xA9, 0x84
)


class Instruction(_Instruction):
    """
    Represents a single JVM instruction, consisting
    of an opcode and its potential operands.
    """
    __slots__ = ()

    @classmethod
    def from_mnemonic(cls, mnemonic, operands=None):
        return cls(
            mnemonic,
            _opcode_by_opname[mnemonic][0],
            operands or [],
            0
        )

    @classmethod
    def from_opcode(cls, opcode, operands=None):
        return cls(
            opcode_table[opcode][0],
            opcode,
            operands or [],
            0
        )

    def size_on_disk(self, start_pos=0):
        """
        Returns the size of this instruction and its operands when
        packed. `start_pos` is required for the `tableswitch` and
        `lookupswitch` instruction as the padding depends on alignment.
        """
        size, fmts = 1, definition_from_opcode(self.opcode)[1]
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
        if self.opcode not in _wide:
            return False

        if self.operands[0].value >= 255:
            return True

        if self.opcode == 0x84:
            if self.operands[1].value >= 255:
                return True

        return False


class OperandTypes(object):
    """
    Constants used to determine the "type" of operand on an opcode,
    such as a BRANCH [offset] or a LITERAL [value].
    """
    LITERAL = 10
    LOCAL_INDEX = 20
    CONSTANT_INDEX = 30
    BRANCH = 40
    PADDING = 50


ubyte = struct.Struct('>B')
ushort = struct.Struct('>H')
byte = struct.Struct('>b')
short = struct.Struct('>h')
integer = struct.Struct('>i')

#: An opcode to mnemonic & operand format mapping for every opcode
#: supported by the JVM.
opcode_table = {
    0x32: ('aaload', None),
    0x53: ('aastore', None),
    0x01: ('aconst_null', None),
    0x19: ('aload', [(ubyte, 20)]),
    0x2A: ('aload_0', None),
    0x2B: ('aload_1', None),
    0x2C: ('aload_2', None),
    0x2D: ('aload_3', None),
    0xBD: ('anewarray', [(ushort, 10)]),
    0xB0: ('areturn', None),
    0xBE: ('arraylength', None),
    0x3A: ('astore', [(ubyte, 20)]),
    0x4B: ('astore_0', None),
    0x4C: ('astore_1', None),
    0x4D: ('astore_2', None),
    0x4E: ('astore_3', None),
    0xBF: ('athrow', None),
    0x33: ('baload', None),
    0x54: ('bastore', None),
    0x10: ('bipush', [(ubyte, 10)]),
    0x34: ('caload', None),
    0x55: ('castore', None),
    0xC0: ('checkcast', [(ushort, 30)]),
    0x90: ('d2f', None),
    0x8E: ('d2i', None),
    0x8F: ('d2l', None),
    0x63: ('dadd', None),
    0x31: ('daload', None),
    0x52: ('dastore', None),
    0x98: ('dcmpg', None),
    0x97: ('dcmpl', None),
    0x0E: ('dconst_0', None),
    0x0F: ('dconst_1', None),
    0x6F: ('ddiv', None),
    0x18: ('dload', [(ubyte, 20)]),
    0x26: ('dload_0', None),
    0x27: ('dload_1', None),
    0x28: ('dload_2', None),
    0x29: ('dload_3', None),
    0x6B: ('dmul', None),
    0x77: ('dneg', None),
    0x73: ('drem', None),
    0xAF: ('dreturn', None),
    0x39: ('dstore', [(ubyte, 20)]),
    0x47: ('dstore_0', None),
    0x48: ('dstore_1', None),
    0x49: ('dstore_2', None),
    0x4a: ('dstore_3', None),
    0x67: ('dsub', None),
    0x59: ('dup', None),
    0x5A: ('dup_x1', None),
    0x5B: ('dup_x2', None),
    0x5C: ('dup2', None),
    0x5D: ('dup2_x1', None),
    0x5E: ('dup2_x2', None),
    0x8D: ('f2d', None),
    0x8B: ('f2i', None),
    0x8C: ('f2l', None),
    0x62: ('fadd', None),
    0x30: ('faload', None),
    0x51: ('fastore', None),
    0x96: ('fcmpg', None),
    0x95: ('fcmpl', None),
    0x0B: ('fconst_0', None),
    0x0C: ('fconst_1', None),
    0x0D: ('fconst_2', None),
    0x6E: ('fdiv', None),
    0x17: ('fload', [(ubyte, 20)]),
    0x22: ('fload_0', None),
    0x23: ('fload_1', None),
    0x24: ('fload_2', None),
    0x25: ('fload_3', None),
    0x6A: ('fmul', None),
    0x76: ('fneg', None),
    0x72: ('frem', None),
    0xAE: ('freturn', None),
    0x38: ('fstore', [(ubyte, 20)]),
    0x43: ('fstore_0', None),
    0x44: ('fstore_1', None),
    0x45: ('fstore_2', None),
    0x46: ('fstore_3', None),
    0x66: ('fsub', None),
    0xB4: ('getfield', [(ushort, 30)]),
    0xB2: ('getstatic', [(ushort, 30)]),
    0xA7: ('goto', [(short, 40)]),
    0xC8: ('goto_w', [(integer, 40)]),
    0x91: ('ib2', None),
    0x92: ('i2c', None),
    0x87: ('i2d', None),
    0x86: ('i2f', None),
    0x85: ('i2l', None),
    0x93: ('i2s', None),
    0x60: ('iadd', None),
    0x2E: ('iaload', None),
    0x7E: ('iand', None),
    0x4F: ('iastore', None),
    0x02: ('iconst_m1', None),
    0x03: ('iconst_0', None),
    0x04: ('iconst_1', None),
    0x05: ('iconst_2', None),
    0x06: ('iconst_3', None),
    0x07: ('iconst_4', None),
    0x08: ('iconst_5', None),
    0x6C: ('idiv', None),
    0xA5: ('if_acmpeq', [(short, 40)]),
    0xA6: ('if_acmpne', [(short, 40)]),
    0x9F: ('if_icmpeq', [(short, 40)]),
    0xA0: ('if_icmpne', [(short, 40)]),
    0xA1: ('if_icmplt', [(short, 40)]),
    0xA2: ('if_icmpge', [(short, 40)]),
    0xA3: ('if_icmpgt', [(short, 40)]),
    0xA4: ('if_icmple', [(short, 40)]),
    0x99: ('ifeq', [(short, 40)]),
    0x9A: ('ifne', [(short, 40)]),
    0x9B: ('iflt', [(short, 40)]),
    0x9C: ('ifge', [(short, 40)]),
    0x9D: ('ifgt', [(short, 40)]),
    0x9E: ('ifle', [(short, 40)]),
    0xC7: ('ifnonnull', [(short, 40)]),
    0xC6: ('ifnull', [(short, 40)]),
    0x84: ('iinc', [(ubyte, 20), (ubyte, 10)]),
    0x15: ('iload', [(ubyte, 20)]),
    0x1A: ('iload_0', None),
    0x1B: ('iload_1', None),
    0x1C: ('iload_2', None),
    0x1D: ('iload_3', None),
    0x68: ('imul', None),
    0x74: ('ineg', None),
    0xC1: ('instanceof', [(ushort, 30)]),
    0xB9: ('invokeinterface', [(ushort, 30), (ubyte, 10), (ubyte, 50)]),
    0xB7: ('invokespecial', [(ushort, 30)]),
    0xB8: ('invokestatic', [(ushort, 30)]),
    0xB6: ('invokevirtual', [(ushort, 30)]),
    0x80: ('ior', None),
    0x70: ('irem', None),
    0xAC: ('ireturn', None),
    0x78: ('ishl', None),
    0x7A: ('ishr', None),
    0x36: ('istore', [(ubyte, 20)]),
    0x3B: ('istore_0', None),
    0x3C: ('istore_1', None),
    0x3D: ('istore_2', None),
    0x3E: ('istore_3', None),
    0x64: ('isub', None),
    0x7C: ('iushr', None),
    0x82: ('ixor', None),
    0xA8: ('jsr', [(short, 40)]),
    0xC9: ('jsr_w', [(integer, 40)]),
    0x8A: ('l2d', None),
    0x89: ('l2f', None),
    0x88: ('l2i', None),
    0x61: ('ladd', None),
    0x2F: ('laload', None),
    0x7F: ('land', None),
    0x50: ('lastore', None),
    0x94: ('lcmp', None),
    0x09: ('lconst_0', None),
    0x0A: ('lconst_1', None),
    0x12: ('ldc', [(ubyte, 30)]),
    0x13: ('ldc_w', [(ushort, 30)]),
    0x14: ('ldc2_w', [(ushort, 30)]),
    0x6D: ('ldiv', None),
    0x16: ('lload', [(ubyte, 20)]),
    0x1E: ('lload_0', None),
    0x1F: ('lload_1', None),
    0x20: ('lload_2', None),
    0x21: ('lload_3', None),
    0x69: ('lmul', None),
    0x75: ('lneg', None),
    0xAB: ('lookupswitch', None),
    0x81: ('lor', None),
    0x71: ('lrem', None),
    0xAD: ('lreturn', None),
    0x79: ('lshl', None),
    0x7B: ('lshr', None),
    0x37: ('lstore', [(ubyte, 20)]),
    0x3F: ('lstore_0', None),
    0x40: ('lstore_1', None),
    0x41: ('lstore_2', None),
    0x42: ('lstore_3', None),
    0x65: ('lsub', None),
    0x7D: ('lushr', None),
    0x83: ('lxor', None),
    0xC2: ('monitorenter', None),
    0xC3: ('monitorexit', None),
    0xC5: ('multianewarray', [(ushort, 30), (ubyte, 10)]),
    0xBB: ('new', [(ushort, 30)]),
    0xBC: ('newarray', [(ubyte, 10)]),
    0x00: ('nop', None),
    0x57: ('pop', None),
    0x58: ('pop2', None),
    0xB5: ('putfield', [(ushort, 30)]),
    0xB3: ('putstatic', [(ushort, 30)]),
    0xA9: ('ret', [(ubyte, 20)]),
    0xB1: ('return', None),
    0x35: ('saload', None),
    0x56: ('sastore', None),
    0x11: ('sipush', [(ushort, 10)]),
    0x5F: ('swap', None),
    0xAA: ('tableswitch', None),
    0xC4: ('wide', None),
    0xCA: ('breakpoint', None),
    0xFE: ('impdep1', None),
    0xFF: ('impdep2', None)
}

# Creates a new dict with operand and mnemonic swapped for assembling.
_opcode_by_opname = dict((o[0], (k,) + o[1:]) for k, o in opcode_table.items())


def write_instruction(fout, start_pos, ins):
    """
    Writes a single instruction of `opcode` with `operands` to `fout`.

    :param fout: Any file-like object providing ``write()``.
    :param start_pos: The current position in the stream.
    :param ins: The `Instruction` to write.
    """
    opcode, operands = ins.opcode, ins.operands
    fmt_operands = definition_from_opcode(opcode)[1]

    if ins.wide:
        # The "WIDE" prefix
        fout.write(ubyte.pack(0xC4))
        # The real opcode.
        fout.write(ubyte.pack(opcode))
        fout.write(ushort.pack(operands[0].value))
        if opcode == 0x84:
            fout.write(short.pack(operands[1].value))
    # A normal simple opcode with simple operands.
    elif fmt_operands:
        fout.write(ubyte.pack(opcode))
        for i, (fmt, _) in enumerate(fmt_operands):
            fout.write(fmt.pack(operands[i].value))
    # Special case for lookupswitch, which also has a unique.
    elif opcode == 0xAB:
        fout.write(ubyte.pack(opcode))
        # assemble([
        #     ('lookupswitch', {
        #         2: -3,
        #         4: 5
        #     }, <default>)
        # ])
        padding = 4 - (start_pos + 1) % 4
        padding = padding if padding != 4 else 0
        fout.write(struct.pack('{0}x'.format(padding)))
        fout.write(struct.pack('>ii',
            operands[1].value,
            len(operands[0])
        ))
        for key in sorted(operands[0].keys()):
            fout.write(struct.pack('>ii',
                key,
                operands[0][key].value
            ))
    # Special case for tableswitch.
    elif opcode == 0xAA:
        raise NotImplementedError()
    else:
        # opcode with no operands.
        fout.write(ubyte.pack(opcode))


def read_instruction(fio, start_pos):
    """
    Reads a single instruction from `fio` and returns it, or ``None`` if
    the stream is empty.

    :param fio: Any file-like object providing ``read()``.
    :param start_pos: The current position in the stream.
    """
    try:
        op = ubyte.unpack(fio.read(1))[0]
    except struct.error:
        return None

    name, operands = opcode_table[op][:2]

    final_operands = []
    # Most opcodes have simple operands.
    if operands:
        for fmt, type_ in operands:
            final_operands.append(
                Operand(type_, fmt.unpack(fio.read(fmt.size))[0]))
    # Special case for lookupswitch.
    elif op == 0xAB:
        # Get rid of the alignment padding.
        padding = 4 - (start_pos + 1) % 4
        padding = padding if padding != 4 else 0
        fio.read(padding)

        # Default branch address and branch count.
        default, npairs = struct.unpack('>ii', fio.read(8))

        pairs = {}
        for _ in repeat(None, npairs):
            match, offset = struct.unpack('>ii', fio.read(8))
            pairs[match] = offset

        final_operands.append(pairs)
        final_operands.append(Operand(OperandTypes.BRANCH, default))
    # Special case for tableswitch
    elif op == 0xAA:
        # Get rid of the alignment padding.
        padding = 4 - (start_pos + 1) % 4
        padding = padding if padding != 4 else 0
        fio.read(padding)

        default, low, high = struct.unpack('>iii', fio.read(12))
        final_operands.append(Operand(OperandTypes.BRANCH, default))
        final_operands.append(Operand(OperandTypes.LITERAL, low))
        final_operands.append(Operand(OperandTypes.LITERAL, high))

        for _ in repeat(None, high - low + 1):
            offset = struct.unpack('>i', fio.read(4))[0]
            final_operands.append(Operand(OperandTypes.BRANCH, offset))
    # Special case for the wide prefix
    elif op == 0xC4:
        real_op = ubyte.unpack(fio.read(1))[0]
        name, operands = opcode_table[real_op][:2]
        final_operands.append(Operand(
            OperandTypes.LOCAL_INDEX,
            ushort.unpack(fio.read(2))[0]
        ))
        # Further special case for iinc.
        if real_op == 0x84:
            final_operands.append(Operand(
                OperandTypes.LITERAL,
                short.unpack(fio.read(2))[0]
            ))

    return Instruction(name, op, final_operands, start_pos)


def definition_from_mnemonic(mnemonic):
    """
    Returns the definition of an instruction by its mnemonic in the
    form: ``(opcode, operand_fmt)``
    """
    return _opcode_by_opname[mnemonic]


def definition_from_opcode(opcode):
    """
    Returns the definition of an instruction by its opcode in the
    form: ``(mnemonic, operand_fmt)``
    """
    return opcode_table[opcode]
