from struct import unpack, calcsize
from itertools import repeat


class BytecodeError(Exception):
    pass


class Operand(object):
    __slots__ = ()


class PaddingOperand(Operand):
    __slots__ = ()

    def __init__(self, pad=0):
        pass


class ConstantIndexOperand(Operand):
    __slots__ = ('_index', )

    def __init__(self, index):
        self._index = index

    @property
    def index(self):
        return self._index

    def __repr__(self):
        return '<ConstantIndexOperand(index=%r)>' % self.index


class LocalIndexOperand(Operand):
    __slots__ = ('_index')

    def __init__(self, index):
        self._index = index

    @property
    def index(self):
        return self._index

    def __repr__(self):
        return '<LocalIndexOperand(index=%r)>' % self.index


class LiteralOperand(Operand):
    __slots__ = ('_value')

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return '<LiteralOperand(value=%r)>' % self.value


class BranchOperand(Operand):
    __slots__ = ('_offset')

    def __init__(self, offset):
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    def __repr__(self):
        return '<BranchOperand(offset=%r)>' % self.offset


class Opcode(object):
    __slots__ = ('_op', '_operands', '_idx')

    def __init__(self, op, operands=None, idx=None):
        self._op = op
        self._operands = operands or []
        self._idx = idx

    @property
    def operands(self):
        return self._operands

    @property
    def opcode(self):
        return self._op

    @property
    def name(self):
        return _opcodes[self._op][0]

    @property
    def fmt(self):
        return _opcodes[self._op][1]

    @property
    def index(self):
        return self._idx

    def __repr__(self):
        return '<Opcode(opcode=%r, name=%r, operands=%r, idx=%r)>' % (
            self.opcode,
            self.name,
            self.operands,
            self.index
        )


_opcodes = {
    0x32: ('aaload', None, (2, 1)),
    0x53: ('aastore', None, (3, 0)),
    0x01: ('aconst_null', None, (0, 1)),
    0x19: ('aload', [('>B', LocalIndexOperand)], (0, 1)),
    0x2A: ('aload_0', None, (0, 1)),
    0x2B: ('aload_1', None, (0, 1)),
    0x2C: ('aload_2', None, (0, 1)),
    0x2D: ('aload_3', None, (0, 1)),
    0xBD: ('anewarray', [('>H', LiteralOperand)], (1, 1)),
    0xB0: ('areturn', None, (1, 0)),
    0xBE: ('arraylength', None, (1, 1)),
    0x3A: ('astore', [('>B', LocalIndexOperand)], (1, 0)),
    0x4B: ('astore_0', None, (1, 0)),
    0x4C: ('astore_1', None, (1, 0)),
    0x4D: ('astore_2', None, (1, 0)),
    0x4E: ('astore_3', None, (1, 0)),
    0xBF: ('athrow', None),
    0x33: ('baload', None),
    0x54: ('bastore', None),
    0x10: ('bipush', [('>B', LiteralOperand)]),
    0x34: ('caload', None),
    0x55: ('castore', None),
    0xC0: ('checkcast', [('>H', ConstantIndexOperand)]),
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
    0x18: ('dload', [('>B', LocalIndexOperand)]),
    0x26: ('dload_0', None),
    0x27: ('dload_1', None),
    0x28: ('dload_2', None),
    0x29: ('dload_3', None),
    0x6B: ('dmul', None),
    0x77: ('dneg', None),
    0x73: ('drem', None),
    0xAF: ('dreturn', None),
    0x39: ('dstore', [('>B', LocalIndexOperand)]),
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
    0x17: ('fload', [('>B', LocalIndexOperand)]),
    0x22: ('fload_0', None),
    0x23: ('fload_1', None),
    0x24: ('fload_2', None),
    0x25: ('fload_3', None),
    0x6A: ('fmul', None),
    0x76: ('fneg', None),
    0x72: ('frem', None),
    0xAE: ('freturn', None),
    0x38: ('fstore', [('>B', LocalIndexOperand)]),
    0x43: ('fstore_0', None),
    0x44: ('fstore_1', None),
    0x45: ('fstore_2', None),
    0x46: ('fstore_3', None),
    0x66: ('fsub', None),
    0xB4: ('getfield', [('>H', ConstantIndexOperand)]),
    0xB2: ('getstatic', [('>H', ConstantIndexOperand)]),
    0xA7: ('goto', [('>h', BranchOperand)]),
    0xC8: ('goto_w', [('>i', BranchOperand)]),
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
    0xA5: ('if_acmpeq', [('>h', BranchOperand)]),
    0xA6: ('if_acmpne', [('>h', BranchOperand)]),
    0x9F: ('if_icmpeq', [('>h', BranchOperand)]),
    0xA0: ('if_icmpne', [('>h', BranchOperand)]),
    0xA1: ('if_icmplt', [('>h', BranchOperand)]),
    0xA2: ('if_icmpge', [('>h', BranchOperand)]),
    0xA3: ('if_icmpgt', [('>h', BranchOperand)]),
    0xA4: ('if_icmple', [('>h', BranchOperand)]),
    0x99: ('ifeq', [('>h', BranchOperand)]),
    0x9A: ('ifne', [('>h', BranchOperand)]),
    0x9B: ('iflt', [('>h', BranchOperand)]),
    0x9C: ('ifge', [('>h', BranchOperand)]),
    0x9D: ('ifgt', [('>h', BranchOperand)]),
    0x9E: ('ifle', [('>h', BranchOperand)]),
    0xC7: ('ifnonnull', [('>h', BranchOperand)]),
    0xC6: ('ifnull', [('>h', BranchOperand)]),
    0x84: ('iinc', [('>B', LocalIndexOperand), ('>B', LiteralOperand)]),
    0x15: ('iload', [('>B', LocalIndexOperand)]),
    0x1A: ('iload_0', None),
    0x1B: ('iload_1', None),
    0x1C: ('iload_2', None),
    0x1D: ('iload_3', None),
    0x68: ('imul', None),
    0x74: ('ineg', None),
    0xC1: ('instanceof', [('>H', ConstantIndexOperand)]),
    0xB9: ('invokeinterface', [
        ('>H', ConstantIndexOperand),
        ('>B', LiteralOperand),
        ('>B', PaddingOperand)
    ]),
    0xB7: ('invokespecial', [('>H', ConstantIndexOperand)]),
    0xB8: ('invokestatic', [('>H', ConstantIndexOperand)]),
    0xB6: ('invokevirtual', [('>H', ConstantIndexOperand)]),
    0x80: ('ior', None),
    0x70: ('irem', None),
    0xAC: ('ireturn', None),
    0x78: ('ishl', None),
    0x7A: ('ishr', None),
    0x36: ('istore', [('>B', LocalIndexOperand)]),
    0x3B: ('istore_0', None),
    0x3C: ('istore_1', None),
    0x3D: ('istore_2', None),
    0x3E: ('istore_3', None),
    0x64: ('isub', None),
    0x7C: ('iushr', None),
    0x82: ('ixor', None),
    0xA8: ('jsr', [('>h', BranchOperand)]),
    0xC9: ('jsr_w', [('>i', BranchOperand)]),
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
    0x12: ('ldc', [('>B', ConstantIndexOperand)]),
    0x13: ('ldc_w', [('>H', ConstantIndexOperand)]),
    0x14: ('ldc2_w', [('>H', ConstantIndexOperand)]),
    0x6D: ('ldiv', None),
    0x16: ('lload', [('>B', LocalIndexOperand)]),
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
    0x37: ('lstore', [('>B', LocalIndexOperand)]),
    0x3F: ('lstore_0', None),
    0x40: ('lstore_1', None),
    0x41: ('lstore_2', None),
    0x42: ('lstore_3', None),
    0x65: ('lsub', None),
    0x7D: ('lushr', None),
    0x83: ('lxor', None),
    0xC2: ('monitorenter', None),
    0xC3: ('monitorexit', None),
    0xC5: ('multianewarray', [
        ('>H', ConstantIndexOperand),
        ('>B', LiteralOperand)
    ]),
    0xBB: ('new', [('>H', ConstantIndexOperand)]),
    0xBC: ('newarray', [('>B', LiteralOperand)]),
    0x00: ('nop', None),
    0x57: ('pop', None),
    0x58: ('pop2', None),
    0xB5: ('putfield', [('>H', ConstantIndexOperand)]),
    0xB3: ('putstatic', [('>H', ConstantIndexOperand)]),
    0xA9: ('ret', [('>B', LocalIndexOperand)]),
    0xB1: ('return', None),
    0x35: ('saload', None),
    0x56: ('sastore', None),
    0x11: ('sipush', [('>H', LiteralOperand)]),
    0x5F: ('swap', None),
    0xAA: ('tableswitch', None),
    0xC4: ('wide', None),
    0xCA: ('breakpoint', None),
    0xFE: ('impdep1', None),
    0xFF: ('impdep2', None)
}


class StreamDisassembler(object):
    """
    Disassembles a stream of JVM instructions without caching or otherwise
    doing anything with them. Once the stream has been consumed, it cannot
    be re-iterated.
    """
    def __init__(self, io):
        self._io = io

    @staticmethod
    def get_single(io):
        """
        Parses and returns a single opcode and its operands from the stream
        `io`. `io` must support a blocking `read()` and `tell()`.
        """
        read = io.read
        start_pos = io.tell()

        try:
            op = ord(read(1))
        except TypeError:
            raise IOError()

        if op not in _opcodes:
            raise BytecodeError('0x%X is not a recognized opcode.' % op)

        name, operands = _opcodes[op][:2]
        f_operands = []
        if operands:
            for struct_fmt, operand_type in operands:
                f_operands.append(operand_type(
                    unpack(struct_fmt, read(calcsize(struct_fmt))
                )[0]))
        # Special case the Lookupswitch instruction.
        elif op == 0xAB:
            padding = 4 - (start_pos + 1) % 4
            if padding != 4:
                read(padding)
            default, npairs = unpack('>ii', read(8))
            f_operands.append(BranchOperand(default))
            # TODO: Unroll.
            for _ in repeat(None, npairs):
                match, offset = unpack('>ii', read(8))
                f_operands.append(LiteralOperand(match))
                f_operands.append(BranchOperand(offset))
        # Special case for the Tableswitch instruction.
        elif op == 0xAA:
            padding = 4 - (start_pos + 1) % 4
            if padding != 4:
                read(padding)
            default, low, high = unpack('>iii', read(12))
            count = high - low + 1
            f_operands.append(BranchOperand(default))
            f_operands.append(LiteralOperand(low))
            f_operands.append(LiteralOperand(high))
            # TODO: Unroll.
            for _ in repeat(None, count):
                f_operands.append(BranchOperand(
                    unpack('>i', read(4))[0]
                ))
        # Special case for the wide prefix.
        elif op == 0xC4:
            real_opcode = ord(read(1))
            name, operands = _opcodes[real_opcode][:2]
            f_operands.append(LocalIndexOperand(
                unpack('>H', read(2))[0]
            ))
            if real_opcode == 0x84:
                f_operands.append(LiteralOperand(
                    unpack('>h', read(2))[0]
                ))
        return Opcode(op, f_operands, idx=start_pos)

    def __iter__(self):
        """
        Iterates and yields each instruction in the stream until no more
        can be read.
        """
        while True:
            try:
                yield StreamDisassembler.get_single(self._io)
            except IOError:
                raise StopIteration()
