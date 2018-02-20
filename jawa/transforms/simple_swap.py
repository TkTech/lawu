from jawa.util.bytecode import Instruction, Operand, opcode_table


def simple_swap(ins: Instruction) -> Instruction:
    """
    Replaces one instruction with another based on the transform rules in
    the bytecode definitions file.

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