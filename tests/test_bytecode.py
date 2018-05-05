from pathlib import Path
from jawa.util.bytecode import Instruction, Operand, OperandTypes
from jawa.util.classloader import ClassLoader


GOOD_TABLE_SWITCH = [
    Instruction(mnemonic='iconst_1', opcode=4, operands=[], pos=0),
    Instruction(mnemonic='tableswitch', opcode=170, operands=[
        # DEFAULT
        Operand(OperandTypes.BRANCH, value=30),
        # LOW
        Operand(OperandTypes.LITERAL, value=1),
        # HIGH
        Operand(OperandTypes.LITERAL, value=3),
        # TABLE
        Operand(OperandTypes.BRANCH, value=27),
        Operand(OperandTypes.BRANCH, value=28),
        Operand(OperandTypes.BRANCH, value=29)
    ], pos=1),
    Instruction(mnemonic='return', opcode=177, operands=[], pos=28),
    Instruction(mnemonic='return', opcode=177, operands=[], pos=29),
    Instruction(mnemonic='return', opcode=177, operands=[], pos=30),
    Instruction(mnemonic='return', opcode=177, operands=[], pos=31)
]

GOOD_LOOKUP_SWITCH = [
    Instruction(mnemonic='iconst_1', opcode=4, operands=[], pos=0),
    Instruction(mnemonic='lookupswitch', opcode=171, operands=[
        {1: 27, 3: 28},
        Operand(op_type=OperandTypes.BRANCH, value=29)
    ], pos=1),
    Instruction(mnemonic='return', opcode=177, operands=[], pos=28),
    Instruction(mnemonic='return', opcode=177, operands=[], pos=29),
    Instruction(mnemonic='return', opcode=177, operands=[], pos=30)
]


def test_table_switch():
    # Ensure we can both read and write table switch opcodes.
    loader = ClassLoader()
    loader.update(str(Path(__file__).parent / 'data'))

    cf = loader['TableSwitch']
    main = cf.methods.find_one(name='main')

    instructions = list(main.code.disassemble())
    assert instructions == GOOD_TABLE_SWITCH

    main.code.assemble(instructions)

    instructions = list(main.code.disassemble())
    assert instructions == GOOD_TABLE_SWITCH


def test_lookup_switch():
    # Ensure we can both read and write lookup switch opcodes.
    loader = ClassLoader()
    loader.update(str(Path(__file__).parent / 'data'))

    cf = loader['LookupSwitch']
    main = cf.methods.find_one(name='main')

    instructions = list(main.code.disassemble())
    assert instructions == GOOD_LOOKUP_SWITCH

    main.code.assemble(instructions)

    instructions = list(main.code.disassemble())
    assert instructions == GOOD_LOOKUP_SWITCH
