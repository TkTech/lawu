from typing import List

from jawa.util.bytecode import Instruction, OperandTypes


RETURN_INS = (
    'ireturn',
    'lreturn',
    'freturn',
    'dreturn',
    'areturn',
    'return'
)

BRANCH_INS = (
    # Unconditional
    'goto',
    'goto_w',
    'jsr',
    'jsr_w',
    'ret',
    # Conditional
    'ifeq',
    'iflt',
    'ifle',
    'ifne',
    'ifgt',
    'ifge',
    'ifnull',
    'ifnonnull',
    'if_icmpeq',
    'if_icmpne',
    'if_icmplt',
    'if_icmpgt',
    'if_icmple',
    'if_icmpge',
    'if_acmpeq',
    'if_acmpne'
)


def basic_blocks(instructions: List[Instruction]):
    """
    Given an iterable of instructions, produce a list of basic blocks.

    :param instructions: Any iterable of Instructions.
    :return: An iterator over (block_start, block_end) pairs.
    """
    instructions = list(instructions)
    ins_count = len(instructions)

    block_starts = set()

    # Our first pass through the instructions finds us all the possible
    # branches.
    for i, ins in enumerate(instructions):
        if ins.mnemonic == 'tableswitch':
            # The default branch
            block_starts.add(ins.pos + ins.operands[0].value)
            # The table branches
            for operand in ins.operands[3:]:
                block_starts.add(ins.pos + operand.value)
        elif ins.mnemonic == 'lookupswitch':
            # The default branch
            block_starts.add(ins.pos + ins.operands[1].value)
            # The lookup branches
            block_starts.update(ins.pos + v for v in ins.operands[0].values())
        elif ins.mnemonic in RETURN_INS:
            # All return instructions are their own blocks
            block_starts.add(ins.pos)
        elif ins.mnemonic in BRANCH_INS:
            # The target of all branches, as well as the instruction following
            # the branch, are block starts.
            for operand in ins.operands:
                if operand.op_type == OperandTypes.BRANCH:
                    jump_target = ins.pos + operand.value
                    block_starts.add(jump_target)
                    if i + 1 <= ins_count:
                        block_starts.add(instructions[i + 1].pos)

    start = 0
    for i, ins in enumerate(instructions):
        if ins.pos in block_starts:
            yield (start, instructions[i-1].pos)
            start = ins.pos
            # Handle the typical case where the last instruction is a
            # [x]return but wasn't the target of a branch.
            if i == ins_count - 1:
                yield (start, ins.pos)
