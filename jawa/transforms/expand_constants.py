from jawa.util.bytecode import Instruction, Operand, OperandTypes


def expand_constants(ins: Instruction, *, cf) -> Instruction:
    """Replace CONSTANT_INDEX operand values with the literal CONSTANT."""
    for i, operand in enumerate(ins.operands):
        if not isinstance(operand, Operand):
            continue

        if operand.op_type == OperandTypes.CONSTANT_INDEX:
            ins.operands[i] = cf.constants[operand.value]

    return ins
