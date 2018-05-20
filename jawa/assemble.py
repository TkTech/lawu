from collections import namedtuple

from jawa.constants import Constant
from jawa.util.bytecode import (
    Operand,
    OperandTypes,
    Instruction,
    opcode_table
)


Label = namedtuple('Label', ['name'])


def assemble(code):
    """
    Assemble the given iterable of mnemonics, operands, and lables.

    A convienience over constructing individual Instruction and Operand
    objects, the output of this function can be directly piped to
    :class:`~jawa.attributes.code.CodeAttribute.assemble()` to produce
    executable bytecode.

    As a simple example, lets produce an infinite loop:

        >>> from jawa.assemble import assemble, Label
        >>> print(list(assemble((
        ...     Label('start'),
        ...     ('goto', Label('start'))
        ... ))))
        [Instruction(mnemonic='goto', opcode=167, operands=[
            Operand(op_type=40, value=0)], pos=0)]

    For a more complex example, see examples/hello_world.py.
    """
    final = []

    # We need to make three passes, because we cannot know the offset for
    # jump labels until after we've figured out the PC for each instructions,
    # which is complicated by the variable-width instructions set and
    # alignment padding.
    for line in code:
        if isinstance(line, Label):
            final.append(line)
            continue

        mnemonic, operands = line[0], line[1:]
        operand_fmts = opcode_table[mnemonic]['operands']

        # We need to coerce each opcodes operands into their
        # final `Operand` form.
        final_operands = []
        for i, operand in enumerate(operands):
            if isinstance(operand, Operand):
                # Already in Operand form.
                final_operands.append(operand)
            elif isinstance(operand, Constant):
                # Convert constants into CONSTANT_INDEX'es
                final_operands.append(Operand(
                    OperandTypes.CONSTANT_INDEX,
                    operand.index
                ))
            elif isinstance(operand, dict):
                # lookupswitch's operand is a dict as
                # a special usability case.
                final_operands.append(operand)
            elif isinstance(operand, Label):
                final_operands.append(operand)
            else:
                # For anything else, lookup that opcode's operand
                # type from its definition.
                final_operands.append(Operand(
                    operand_fmts[i][1],
                    operand
                ))

        # Build the final, immutable `Instruction`.
        final.append(Instruction.create(mnemonic, final_operands))

    label_pcs = {}

    # The second pass, find the absolute PC for each label.
    current_pc = 0
    for ins in final:
        if isinstance(ins, Label):
            label_pcs[ins.name] = current_pc
            continue

        # size_on_disk must know the current pc because of alignment on
        # tableswitch and lookupswitch.
        current_pc += ins.size_on_disk(current_pc)

    # The third pass, now that we know where each label is we can figure
    # out the offset for each jump.
    current_pc = 0

    for ins in final:
        if isinstance(ins, Label):
            continue

        for i, operand in enumerate(ins.operands):
            if isinstance(operand, dict):
                # lookupswitch is a special case
                for k, v in operand.items():
                    if isinstance(v, Label):
                        operand[k] = Operand(40, label_pcs[v.name] - current_pc)
            elif isinstance(operand, Label):
                ins.operands[i] = Operand(
                    40,
                    label_pcs[operand.name] - current_pc
                )

        current_pc += ins.size_on_disk(current_pc)

        yield ins
