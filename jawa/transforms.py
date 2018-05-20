"""
Transforms are simple Instruction modifiers that can be called on each
Instruction by the :func:`~jawa.attributes.code.CodeAttribute.disassemble`
function.
"""
from jawa.util.bytecode import Instruction, Operand, OperandTypes, opcode_table


def expand_constants(ins: Instruction, *, cf) -> Instruction:
    """Replace CONSTANT_INDEX operands with the literal Constant object from
    the constant pool.

    :param ins: Instruction to potentially modify.
    :param cf: The ClassFile instance used to resolve Constants.
    :return: Potentially modified instruction.
    """
    for i, operand in enumerate(ins.operands):
        if not isinstance(operand, Operand):
            continue

        if operand.op_type == OperandTypes.CONSTANT_INDEX:
            ins.operands[i] = cf.constants[operand.value]

    return ins


def simple_swap(ins: Instruction) -> Instruction:
    """Replaces one instruction with another based on the transform rules in
    the bytecode definitions. This can help simplify your code as it reduces
    the overall number of instructions. For example, `aload_0` will become
    `aload 0`.

    :param ins: Instruction to potentially modify.
    :return: Potentially modified instruction.
    """
    try:
        rule = ins.details['transform']['simple_swap']
    except KeyError:
        return ins

    replacement_ins = opcode_table[rule['op']]

    return Instruction(
        replacement_ins['mnemonic'],
        replacement_ins['op'],
        [Operand(
            replacement_ins['operands'][i][1],
            r
        ) for i, r in enumerate(rule['operands'])],
        ins.pos
    )
