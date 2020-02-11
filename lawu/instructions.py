"""
Machine-generated from bytecode.yaml. This file aids with typing and
autocompletion in IDEs by providing types for every instruction.
"""
from lawu._instruction import Instruction, OperandTypes


class aaload(Instruction):
    """load onto the stack a reference from an array"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x32
    #: The JVM instruction name as appears in the specification.
    name = 'aaload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class aastore(Instruction):
    """store into a reference in an array"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x53
    #: The JVM instruction name as appears in the specification.
    name = 'aastore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class aconst_null(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x01
    #: The JVM instruction name as appears in the specification.
    name = 'aconst_null'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class aload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x19
    #: The JVM instruction name as appears in the specification.
    name = 'aload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class aload_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x2a
    #: The JVM instruction name as appears in the specification.
    name = 'aload_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class aload_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x2b
    #: The JVM instruction name as appears in the specification.
    name = 'aload_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class aload_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x2c
    #: The JVM instruction name as appears in the specification.
    name = 'aload_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class aload_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x2d
    #: The JVM instruction name as appears in the specification.
    name = 'aload_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class anewarray(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xbd
    #: The JVM instruction name as appears in the specification.
    name = 'anewarray'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class areturn(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xb0
    #: The JVM instruction name as appears in the specification.
    name = 'areturn'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class arraylength(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xbe
    #: The JVM instruction name as appears in the specification.
    name = 'arraylength'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class astore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x3a
    #: The JVM instruction name as appears in the specification.
    name = 'astore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class astore_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x4b
    #: The JVM instruction name as appears in the specification.
    name = 'astore_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class astore_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x4c
    #: The JVM instruction name as appears in the specification.
    name = 'astore_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class astore_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x4d
    #: The JVM instruction name as appears in the specification.
    name = 'astore_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class astore_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x4e
    #: The JVM instruction name as appears in the specification.
    name = 'astore_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class athrow(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xbf
    #: The JVM instruction name as appears in the specification.
    name = 'athrow'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class baload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x33
    #: The JVM instruction name as appears in the specification.
    name = 'baload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class bastore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x54
    #: The JVM instruction name as appears in the specification.
    name = 'bastore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class bipush(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x10
    #: The JVM instruction name as appears in the specification.
    name = 'bipush'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>b', 'L'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class caload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x34
    #: The JVM instruction name as appears in the specification.
    name = 'caload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class castore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x55
    #: The JVM instruction name as appears in the specification.
    name = 'castore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class checkcast(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xc0
    #: The JVM instruction name as appears in the specification.
    name = 'checkcast'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class d2f(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x90
    #: The JVM instruction name as appears in the specification.
    name = 'd2f'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class d2i(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x8e
    #: The JVM instruction name as appears in the specification.
    name = 'd2i'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class d2l(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x8f
    #: The JVM instruction name as appears in the specification.
    name = 'd2l'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dadd(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x63
    #: The JVM instruction name as appears in the specification.
    name = 'dadd'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class daload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x31
    #: The JVM instruction name as appears in the specification.
    name = 'daload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dastore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x52
    #: The JVM instruction name as appears in the specification.
    name = 'dastore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dcmpg(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x98
    #: The JVM instruction name as appears in the specification.
    name = 'dcmpg'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dcmpl(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x97
    #: The JVM instruction name as appears in the specification.
    name = 'dcmpl'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dconst_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x0e
    #: The JVM instruction name as appears in the specification.
    name = 'dconst_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dconst_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x0f
    #: The JVM instruction name as appears in the specification.
    name = 'dconst_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ddiv(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x6f
    #: The JVM instruction name as appears in the specification.
    name = 'ddiv'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x18
    #: The JVM instruction name as appears in the specification.
    name = 'dload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class dload_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x26
    #: The JVM instruction name as appears in the specification.
    name = 'dload_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dload_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x27
    #: The JVM instruction name as appears in the specification.
    name = 'dload_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dload_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x28
    #: The JVM instruction name as appears in the specification.
    name = 'dload_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dload_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x29
    #: The JVM instruction name as appears in the specification.
    name = 'dload_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dmul(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x6b
    #: The JVM instruction name as appears in the specification.
    name = 'dmul'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dneg(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x77
    #: The JVM instruction name as appears in the specification.
    name = 'dneg'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class drem(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x73
    #: The JVM instruction name as appears in the specification.
    name = 'drem'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dreturn(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xaf
    #: The JVM instruction name as appears in the specification.
    name = 'dreturn'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dstore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x39
    #: The JVM instruction name as appears in the specification.
    name = 'dstore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class dstore_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x47
    #: The JVM instruction name as appears in the specification.
    name = 'dstore_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dstore_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x48
    #: The JVM instruction name as appears in the specification.
    name = 'dstore_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dstore_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x49
    #: The JVM instruction name as appears in the specification.
    name = 'dstore_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dstore_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x4a
    #: The JVM instruction name as appears in the specification.
    name = 'dstore_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dsub(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x67
    #: The JVM instruction name as appears in the specification.
    name = 'dsub'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dup(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x59
    #: The JVM instruction name as appears in the specification.
    name = 'dup'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dup_x1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x5a
    #: The JVM instruction name as appears in the specification.
    name = 'dup_x1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dup_x2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x5b
    #: The JVM instruction name as appears in the specification.
    name = 'dup_x2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dup2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x5c
    #: The JVM instruction name as appears in the specification.
    name = 'dup2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dup2_x1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x5d
    #: The JVM instruction name as appears in the specification.
    name = 'dup2_x1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class dup2_x2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x5e
    #: The JVM instruction name as appears in the specification.
    name = 'dup2_x2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class f2d(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x8d
    #: The JVM instruction name as appears in the specification.
    name = 'f2d'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class f2i(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x8b
    #: The JVM instruction name as appears in the specification.
    name = 'f2i'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class f2l(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x8c
    #: The JVM instruction name as appears in the specification.
    name = 'f2l'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fadd(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x62
    #: The JVM instruction name as appears in the specification.
    name = 'fadd'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class faload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x30
    #: The JVM instruction name as appears in the specification.
    name = 'faload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fastore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x51
    #: The JVM instruction name as appears in the specification.
    name = 'fastore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fcmpg(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x96
    #: The JVM instruction name as appears in the specification.
    name = 'fcmpg'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fcmpl(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x95
    #: The JVM instruction name as appears in the specification.
    name = 'fcmpl'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fconst_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x0b
    #: The JVM instruction name as appears in the specification.
    name = 'fconst_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fconst_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x0c
    #: The JVM instruction name as appears in the specification.
    name = 'fconst_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fconst_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x0d
    #: The JVM instruction name as appears in the specification.
    name = 'fconst_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fdiv(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x6e
    #: The JVM instruction name as appears in the specification.
    name = 'fdiv'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x17
    #: The JVM instruction name as appears in the specification.
    name = 'fload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class fload_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x22
    #: The JVM instruction name as appears in the specification.
    name = 'fload_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fload_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x23
    #: The JVM instruction name as appears in the specification.
    name = 'fload_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fload_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x24
    #: The JVM instruction name as appears in the specification.
    name = 'fload_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fload_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x25
    #: The JVM instruction name as appears in the specification.
    name = 'fload_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fmul(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x6a
    #: The JVM instruction name as appears in the specification.
    name = 'fmul'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fneg(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x76
    #: The JVM instruction name as appears in the specification.
    name = 'fneg'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class frem(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x72
    #: The JVM instruction name as appears in the specification.
    name = 'frem'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class freturn(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xae
    #: The JVM instruction name as appears in the specification.
    name = 'freturn'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fstore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x38
    #: The JVM instruction name as appears in the specification.
    name = 'fstore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class fstore_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x43
    #: The JVM instruction name as appears in the specification.
    name = 'fstore_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fstore_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x44
    #: The JVM instruction name as appears in the specification.
    name = 'fstore_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fstore_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x45
    #: The JVM instruction name as appears in the specification.
    name = 'fstore_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fstore_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x46
    #: The JVM instruction name as appears in the specification.
    name = 'fstore_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class fsub(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x66
    #: The JVM instruction name as appears in the specification.
    name = 'fsub'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class getfield(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xb4
    #: The JVM instruction name as appears in the specification.
    name = 'getfield'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class getstatic(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xb2
    #: The JVM instruction name as appears in the specification.
    name = 'getstatic'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class goto(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xa7
    #: The JVM instruction name as appears in the specification.
    name = 'goto'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class goto_w(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xc8
    #: The JVM instruction name as appears in the specification.
    name = 'goto_w'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>i', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class i2b(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x91
    #: The JVM instruction name as appears in the specification.
    name = 'i2b'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class i2c(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x92
    #: The JVM instruction name as appears in the specification.
    name = 'i2c'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class i2d(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x87
    #: The JVM instruction name as appears in the specification.
    name = 'i2d'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class i2f(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x86
    #: The JVM instruction name as appears in the specification.
    name = 'i2f'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class i2l(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x85
    #: The JVM instruction name as appears in the specification.
    name = 'i2l'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class i2s(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x93
    #: The JVM instruction name as appears in the specification.
    name = 'i2s'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iadd(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x60
    #: The JVM instruction name as appears in the specification.
    name = 'iadd'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iaload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x2e
    #: The JVM instruction name as appears in the specification.
    name = 'iaload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iand(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x7e
    #: The JVM instruction name as appears in the specification.
    name = 'iand'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iastore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x4f
    #: The JVM instruction name as appears in the specification.
    name = 'iastore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iconst_m1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x02
    #: The JVM instruction name as appears in the specification.
    name = 'iconst_m1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iconst_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x03
    #: The JVM instruction name as appears in the specification.
    name = 'iconst_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iconst_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x04
    #: The JVM instruction name as appears in the specification.
    name = 'iconst_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iconst_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x05
    #: The JVM instruction name as appears in the specification.
    name = 'iconst_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iconst_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x06
    #: The JVM instruction name as appears in the specification.
    name = 'iconst_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iconst_4(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x07
    #: The JVM instruction name as appears in the specification.
    name = 'iconst_4'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iconst_5(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x08
    #: The JVM instruction name as appears in the specification.
    name = 'iconst_5'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class idiv(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x6c
    #: The JVM instruction name as appears in the specification.
    name = 'idiv'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class if_acmpeq(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xa5
    #: The JVM instruction name as appears in the specification.
    name = 'if_acmpeq'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class if_acmpne(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xa6
    #: The JVM instruction name as appears in the specification.
    name = 'if_acmpne'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class if_icmpeq(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x9f
    #: The JVM instruction name as appears in the specification.
    name = 'if_icmpeq'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class if_icmpne(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xa0
    #: The JVM instruction name as appears in the specification.
    name = 'if_icmpne'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class if_icmplt(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xa1
    #: The JVM instruction name as appears in the specification.
    name = 'if_icmplt'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class if_icmpge(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xa2
    #: The JVM instruction name as appears in the specification.
    name = 'if_icmpge'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class if_icmpgt(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xa3
    #: The JVM instruction name as appears in the specification.
    name = 'if_icmpgt'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class if_icmple(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xa4
    #: The JVM instruction name as appears in the specification.
    name = 'if_icmple'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ifeq(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x99
    #: The JVM instruction name as appears in the specification.
    name = 'ifeq'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ifne(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x9a
    #: The JVM instruction name as appears in the specification.
    name = 'ifne'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iflt(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x9b
    #: The JVM instruction name as appears in the specification.
    name = 'iflt'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ifge(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x9c
    #: The JVM instruction name as appears in the specification.
    name = 'ifge'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ifgt(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x9d
    #: The JVM instruction name as appears in the specification.
    name = 'ifgt'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ifle(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x9e
    #: The JVM instruction name as appears in the specification.
    name = 'ifle'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ifnonnull(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xc7
    #: The JVM instruction name as appears in the specification.
    name = 'ifnonnull'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ifnull(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xc6
    #: The JVM instruction name as appears in the specification.
    name = 'ifnull'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iinc(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x84
    #: The JVM instruction name as appears in the specification.
    name = 'iinc'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'), ('>B', 'L'))
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class iload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x15
    #: The JVM instruction name as appears in the specification.
    name = 'iload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class iload_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x1a
    #: The JVM instruction name as appears in the specification.
    name = 'iload_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iload_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x1b
    #: The JVM instruction name as appears in the specification.
    name = 'iload_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iload_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x1c
    #: The JVM instruction name as appears in the specification.
    name = 'iload_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iload_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x1d
    #: The JVM instruction name as appears in the specification.
    name = 'iload_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class imul(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x68
    #: The JVM instruction name as appears in the specification.
    name = 'imul'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ineg(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x74
    #: The JVM instruction name as appears in the specification.
    name = 'ineg'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class instanceof(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xc1
    #: The JVM instruction name as appears in the specification.
    name = 'instanceof'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class invokedynamic(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xba
    #: The JVM instruction name as appears in the specification.
    name = 'invokedynamic'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'), ('>B', 'P'), ('>B', 'P'))
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class invokeinterface(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xb9
    #: The JVM instruction name as appears in the specification.
    name = 'invokeinterface'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'), ('>B', 'L'), ('>B', 'P'))
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class invokespecial(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xb7
    #: The JVM instruction name as appears in the specification.
    name = 'invokespecial'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class invokestatic(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xb8
    #: The JVM instruction name as appears in the specification.
    name = 'invokestatic'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class invokevirtual(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xb6
    #: The JVM instruction name as appears in the specification.
    name = 'invokevirtual'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ior(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x80
    #: The JVM instruction name as appears in the specification.
    name = 'ior'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class irem(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x70
    #: The JVM instruction name as appears in the specification.
    name = 'irem'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ireturn(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xac
    #: The JVM instruction name as appears in the specification.
    name = 'ireturn'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ishl(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x78
    #: The JVM instruction name as appears in the specification.
    name = 'ishl'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ishr(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x7a
    #: The JVM instruction name as appears in the specification.
    name = 'ishr'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class istore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x36
    #: The JVM instruction name as appears in the specification.
    name = 'istore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class istore_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x3b
    #: The JVM instruction name as appears in the specification.
    name = 'istore_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class istore_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x3c
    #: The JVM instruction name as appears in the specification.
    name = 'istore_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class istore_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x3d
    #: The JVM instruction name as appears in the specification.
    name = 'istore_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class istore_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x3e
    #: The JVM instruction name as appears in the specification.
    name = 'istore_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class isub(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x64
    #: The JVM instruction name as appears in the specification.
    name = 'isub'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class iushr(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x7c
    #: The JVM instruction name as appears in the specification.
    name = 'iushr'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ixor(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x82
    #: The JVM instruction name as appears in the specification.
    name = 'ixor'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class jsr(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xa8
    #: The JVM instruction name as appears in the specification.
    name = 'jsr'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class jsr_w(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xc9
    #: The JVM instruction name as appears in the specification.
    name = 'jsr_w'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>i', 'B'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class l2d(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x8a
    #: The JVM instruction name as appears in the specification.
    name = 'l2d'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class l2f(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x89
    #: The JVM instruction name as appears in the specification.
    name = 'l2f'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class l2i(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x88
    #: The JVM instruction name as appears in the specification.
    name = 'l2i'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ladd(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x61
    #: The JVM instruction name as appears in the specification.
    name = 'ladd'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class laload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x2f
    #: The JVM instruction name as appears in the specification.
    name = 'laload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class land(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x7f
    #: The JVM instruction name as appears in the specification.
    name = 'land'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lastore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x50
    #: The JVM instruction name as appears in the specification.
    name = 'lastore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lcmp(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x94
    #: The JVM instruction name as appears in the specification.
    name = 'lcmp'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lconst_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x09
    #: The JVM instruction name as appears in the specification.
    name = 'lconst_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lconst_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x0a
    #: The JVM instruction name as appears in the specification.
    name = 'lconst_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ldc(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x12
    #: The JVM instruction name as appears in the specification.
    name = 'ldc'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ldc_w(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x13
    #: The JVM instruction name as appears in the specification.
    name = 'ldc_w'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ldc2_w(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x14
    #: The JVM instruction name as appears in the specification.
    name = 'ldc2_w'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ldiv(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x6d
    #: The JVM instruction name as appears in the specification.
    name = 'ldiv'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x16
    #: The JVM instruction name as appears in the specification.
    name = 'lload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class lload_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x1e
    #: The JVM instruction name as appears in the specification.
    name = 'lload_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lload_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x1f
    #: The JVM instruction name as appears in the specification.
    name = 'lload_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lload_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x20
    #: The JVM instruction name as appears in the specification.
    name = 'lload_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lload_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x21
    #: The JVM instruction name as appears in the specification.
    name = 'lload_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lmul(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x69
    #: The JVM instruction name as appears in the specification.
    name = 'lmul'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lneg(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x75
    #: The JVM instruction name as appears in the specification.
    name = 'lneg'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lookupswitch(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xab
    #: The JVM instruction name as appears in the specification.
    name = 'lookupswitch'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lor(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x81
    #: The JVM instruction name as appears in the specification.
    name = 'lor'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lrem(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x71
    #: The JVM instruction name as appears in the specification.
    name = 'lrem'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lreturn(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xad
    #: The JVM instruction name as appears in the specification.
    name = 'lreturn'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lshl(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x79
    #: The JVM instruction name as appears in the specification.
    name = 'lshl'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lshr(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x7b
    #: The JVM instruction name as appears in the specification.
    name = 'lshr'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lstore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x37
    #: The JVM instruction name as appears in the specification.
    name = 'lstore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class lstore_0(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x3f
    #: The JVM instruction name as appears in the specification.
    name = 'lstore_0'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lstore_1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x40
    #: The JVM instruction name as appears in the specification.
    name = 'lstore_1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lstore_2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x41
    #: The JVM instruction name as appears in the specification.
    name = 'lstore_2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lstore_3(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x42
    #: The JVM instruction name as appears in the specification.
    name = 'lstore_3'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lsub(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x65
    #: The JVM instruction name as appears in the specification.
    name = 'lsub'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lushr(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x7d
    #: The JVM instruction name as appears in the specification.
    name = 'lushr'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class lxor(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x83
    #: The JVM instruction name as appears in the specification.
    name = 'lxor'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class monitorenter(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xc2
    #: The JVM instruction name as appears in the specification.
    name = 'monitorenter'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class monitorexit(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xc3
    #: The JVM instruction name as appears in the specification.
    name = 'monitorexit'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class multianewarray(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xc5
    #: The JVM instruction name as appears in the specification.
    name = 'multianewarray'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'), ('>B', 'L'))
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class new(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xbb
    #: The JVM instruction name as appears in the specification.
    name = 'new'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class newarray(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xbc
    #: The JVM instruction name as appears in the specification.
    name = 'newarray'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'L'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class nop(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x00
    #: The JVM instruction name as appears in the specification.
    name = 'nop'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class pop(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x57
    #: The JVM instruction name as appears in the specification.
    name = 'pop'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class pop2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x58
    #: The JVM instruction name as appears in the specification.
    name = 'pop2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class putfield(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xb5
    #: The JVM instruction name as appears in the specification.
    name = 'putfield'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class putstatic(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xb3
    #: The JVM instruction name as appears in the specification.
    name = 'putstatic'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>H', 'C'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class ret(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xa9
    #: The JVM instruction name as appears in the specification.
    name = 'ret'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>B', 'I'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = True


class return_(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xb1
    #: The JVM instruction name as appears in the specification.
    name = 'return'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class saload(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x35
    #: The JVM instruction name as appears in the specification.
    name = 'saload'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class sastore(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x56
    #: The JVM instruction name as appears in the specification.
    name = 'sastore'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class sipush(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x11
    #: The JVM instruction name as appears in the specification.
    name = 'sipush'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = (('>h', 'L'),)
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class swap(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0x5f
    #: The JVM instruction name as appears in the specification.
    name = 'swap'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class tableswitch(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xaa
    #: The JVM instruction name as appears in the specification.
    name = 'tableswitch'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class wide(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xc4
    #: The JVM instruction name as appears in the specification.
    name = 'wide'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class breakpoint(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xca
    #: The JVM instruction name as appears in the specification.
    name = 'breakpoint'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class impdep1(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xfe
    #: The JVM instruction name as appears in the specification.
    name = 'impdep1'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


class impdep2(Instruction):
    """"""
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = 0xff
    #: The JVM instruction name as appears in the specification.
    name = 'impdep2'
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = ()
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = False


BY_OP = {
    0: nop,
    1: aconst_null,
    2: iconst_m1,
    3: iconst_0,
    4: iconst_1,
    5: iconst_2,
    6: iconst_3,
    7: iconst_4,
    8: iconst_5,
    9: lconst_0,
    10: lconst_1,
    11: fconst_0,
    12: fconst_1,
    13: fconst_2,
    14: dconst_0,
    15: dconst_1,
    16: bipush,
    17: sipush,
    18: ldc,
    19: ldc_w,
    20: ldc2_w,
    21: iload,
    22: lload,
    23: fload,
    24: dload,
    25: aload,
    26: iload_0,
    27: iload_1,
    28: iload_2,
    29: iload_3,
    30: lload_0,
    31: lload_1,
    32: lload_2,
    33: lload_3,
    34: fload_0,
    35: fload_1,
    36: fload_2,
    37: fload_3,
    38: dload_0,
    39: dload_1,
    40: dload_2,
    41: dload_3,
    42: aload_0,
    43: aload_1,
    44: aload_2,
    45: aload_3,
    46: iaload,
    47: laload,
    48: faload,
    49: daload,
    50: aaload,
    51: baload,
    52: caload,
    53: saload,
    54: istore,
    55: lstore,
    56: fstore,
    57: dstore,
    58: astore,
    59: istore_0,
    60: istore_1,
    61: istore_2,
    62: istore_3,
    63: lstore_0,
    64: lstore_1,
    65: lstore_2,
    66: lstore_3,
    67: fstore_0,
    68: fstore_1,
    69: fstore_2,
    70: fstore_3,
    71: dstore_0,
    72: dstore_1,
    73: dstore_2,
    74: dstore_3,
    75: astore_0,
    76: astore_1,
    77: astore_2,
    78: astore_3,
    79: iastore,
    80: lastore,
    81: fastore,
    82: dastore,
    83: aastore,
    84: bastore,
    85: castore,
    86: sastore,
    87: pop,
    88: pop2,
    89: dup,
    90: dup_x1,
    91: dup_x2,
    92: dup2,
    93: dup2_x1,
    94: dup2_x2,
    95: swap,
    96: iadd,
    97: ladd,
    98: fadd,
    99: dadd,
    100: isub,
    101: lsub,
    102: fsub,
    103: dsub,
    104: imul,
    105: lmul,
    106: fmul,
    107: dmul,
    108: idiv,
    109: ldiv,
    110: fdiv,
    111: ddiv,
    112: irem,
    113: lrem,
    114: frem,
    115: drem,
    116: ineg,
    117: lneg,
    118: fneg,
    119: dneg,
    120: ishl,
    121: lshl,
    122: ishr,
    123: lshr,
    124: iushr,
    125: lushr,
    126: iand,
    127: land,
    128: ior,
    129: lor,
    130: ixor,
    131: lxor,
    132: iinc,
    133: i2l,
    134: i2f,
    135: i2d,
    136: l2i,
    137: l2f,
    138: l2d,
    139: f2i,
    140: f2l,
    141: f2d,
    142: d2i,
    143: d2l,
    144: d2f,
    145: i2b,
    146: i2c,
    147: i2s,
    148: lcmp,
    149: fcmpl,
    150: fcmpg,
    151: dcmpl,
    152: dcmpg,
    153: ifeq,
    154: ifne,
    155: iflt,
    156: ifge,
    157: ifgt,
    158: ifle,
    159: if_icmpeq,
    160: if_icmpne,
    161: if_icmplt,
    162: if_icmpge,
    163: if_icmpgt,
    164: if_icmple,
    165: if_acmpeq,
    166: if_acmpne,
    167: goto,
    168: jsr,
    169: ret,
    170: tableswitch,
    171: lookupswitch,
    172: ireturn,
    173: lreturn,
    174: freturn,
    175: dreturn,
    176: areturn,
    177: return_,
    178: getstatic,
    179: putstatic,
    180: getfield,
    181: putfield,
    182: invokevirtual,
    183: invokespecial,
    184: invokestatic,
    185: invokeinterface,
    186: invokedynamic,
    187: new,
    188: newarray,
    189: anewarray,
    190: arraylength,
    191: athrow,
    192: checkcast,
    193: instanceof,
    194: monitorenter,
    195: monitorexit,
    196: wide,
    197: multianewarray,
    198: ifnull,
    199: ifnonnull,
    200: goto_w,
    201: jsr_w,
    202: breakpoint,
    254: impdep1,
    255: impdep2
}
BY_NAME = {
    'aaload': aaload,
    'aastore': aastore,
    'aconst_null': aconst_null,
    'aload': aload,
    'aload_0': aload_0,
    'aload_1': aload_1,
    'aload_2': aload_2,
    'aload_3': aload_3,
    'anewarray': anewarray,
    'areturn': areturn,
    'arraylength': arraylength,
    'astore': astore,
    'astore_0': astore_0,
    'astore_1': astore_1,
    'astore_2': astore_2,
    'astore_3': astore_3,
    'athrow': athrow,
    'baload': baload,
    'bastore': bastore,
    'bipush': bipush,
    'breakpoint': breakpoint,
    'caload': caload,
    'castore': castore,
    'checkcast': checkcast,
    'd2f': d2f,
    'd2i': d2i,
    'd2l': d2l,
    'dadd': dadd,
    'daload': daload,
    'dastore': dastore,
    'dcmpg': dcmpg,
    'dcmpl': dcmpl,
    'dconst_0': dconst_0,
    'dconst_1': dconst_1,
    'ddiv': ddiv,
    'dload': dload,
    'dload_0': dload_0,
    'dload_1': dload_1,
    'dload_2': dload_2,
    'dload_3': dload_3,
    'dmul': dmul,
    'dneg': dneg,
    'drem': drem,
    'dreturn': dreturn,
    'dstore': dstore,
    'dstore_0': dstore_0,
    'dstore_1': dstore_1,
    'dstore_2': dstore_2,
    'dstore_3': dstore_3,
    'dsub': dsub,
    'dup': dup,
    'dup2': dup2,
    'dup2_x1': dup2_x1,
    'dup2_x2': dup2_x2,
    'dup_x1': dup_x1,
    'dup_x2': dup_x2,
    'f2d': f2d,
    'f2i': f2i,
    'f2l': f2l,
    'fadd': fadd,
    'faload': faload,
    'fastore': fastore,
    'fcmpg': fcmpg,
    'fcmpl': fcmpl,
    'fconst_0': fconst_0,
    'fconst_1': fconst_1,
    'fconst_2': fconst_2,
    'fdiv': fdiv,
    'fload': fload,
    'fload_0': fload_0,
    'fload_1': fload_1,
    'fload_2': fload_2,
    'fload_3': fload_3,
    'fmul': fmul,
    'fneg': fneg,
    'frem': frem,
    'freturn': freturn,
    'fstore': fstore,
    'fstore_0': fstore_0,
    'fstore_1': fstore_1,
    'fstore_2': fstore_2,
    'fstore_3': fstore_3,
    'fsub': fsub,
    'getfield': getfield,
    'getstatic': getstatic,
    'goto': goto,
    'goto_w': goto_w,
    'i2b': i2b,
    'i2c': i2c,
    'i2d': i2d,
    'i2f': i2f,
    'i2l': i2l,
    'i2s': i2s,
    'iadd': iadd,
    'iaload': iaload,
    'iand': iand,
    'iastore': iastore,
    'iconst_0': iconst_0,
    'iconst_1': iconst_1,
    'iconst_2': iconst_2,
    'iconst_3': iconst_3,
    'iconst_4': iconst_4,
    'iconst_5': iconst_5,
    'iconst_m1': iconst_m1,
    'idiv': idiv,
    'if_acmpeq': if_acmpeq,
    'if_acmpne': if_acmpne,
    'if_icmpeq': if_icmpeq,
    'if_icmpge': if_icmpge,
    'if_icmpgt': if_icmpgt,
    'if_icmple': if_icmple,
    'if_icmplt': if_icmplt,
    'if_icmpne': if_icmpne,
    'ifeq': ifeq,
    'ifge': ifge,
    'ifgt': ifgt,
    'ifle': ifle,
    'iflt': iflt,
    'ifne': ifne,
    'ifnonnull': ifnonnull,
    'ifnull': ifnull,
    'iinc': iinc,
    'iload': iload,
    'iload_0': iload_0,
    'iload_1': iload_1,
    'iload_2': iload_2,
    'iload_3': iload_3,
    'impdep1': impdep1,
    'impdep2': impdep2,
    'imul': imul,
    'ineg': ineg,
    'instanceof': instanceof,
    'invokedynamic': invokedynamic,
    'invokeinterface': invokeinterface,
    'invokespecial': invokespecial,
    'invokestatic': invokestatic,
    'invokevirtual': invokevirtual,
    'ior': ior,
    'irem': irem,
    'ireturn': ireturn,
    'ishl': ishl,
    'ishr': ishr,
    'istore': istore,
    'istore_0': istore_0,
    'istore_1': istore_1,
    'istore_2': istore_2,
    'istore_3': istore_3,
    'isub': isub,
    'iushr': iushr,
    'ixor': ixor,
    'jsr': jsr,
    'jsr_w': jsr_w,
    'l2d': l2d,
    'l2f': l2f,
    'l2i': l2i,
    'ladd': ladd,
    'laload': laload,
    'land': land,
    'lastore': lastore,
    'lcmp': lcmp,
    'lconst_0': lconst_0,
    'lconst_1': lconst_1,
    'ldc': ldc,
    'ldc2_w': ldc2_w,
    'ldc_w': ldc_w,
    'ldiv': ldiv,
    'lload': lload,
    'lload_0': lload_0,
    'lload_1': lload_1,
    'lload_2': lload_2,
    'lload_3': lload_3,
    'lmul': lmul,
    'lneg': lneg,
    'lookupswitch': lookupswitch,
    'lor': lor,
    'lrem': lrem,
    'lreturn': lreturn,
    'lshl': lshl,
    'lshr': lshr,
    'lstore': lstore,
    'lstore_0': lstore_0,
    'lstore_1': lstore_1,
    'lstore_2': lstore_2,
    'lstore_3': lstore_3,
    'lsub': lsub,
    'lushr': lushr,
    'lxor': lxor,
    'monitorenter': monitorenter,
    'monitorexit': monitorexit,
    'multianewarray': multianewarray,
    'new': new,
    'newarray': newarray,
    'nop': nop,
    'pop': pop,
    'pop2': pop2,
    'putfield': putfield,
    'putstatic': putstatic,
    'ret': ret,
    'return': return_,
    'saload': saload,
    'sastore': sastore,
    'sipush': sipush,
    'swap': swap,
    'tableswitch': tableswitch,
    'wide': wide
}
