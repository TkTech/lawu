import io

from struct import unpack, unpack_from
from itertools import repeat

from lawu import ast
from lawu.blocks import jump_targets
from lawu.attribute import Attribute
from lawu.instructions import Instruction, OperandTypes


class CodeAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    @staticmethod
    def _parse_attribute_table(pool, source):
        size = unpack('>H', source.read(2))[0]
        for _ in repeat(None, size):
            name_idx, length = unpack('>HI', source.read(6))
            yield pool[name_idx].value, source.read(length)

    @staticmethod
    def from_binary(pool, source, blob):
        code = ast.Code()
        max_stack, max_locals, c_len = unpack_from('>HHI', blob)
        code.max_stack = max_stack
        code.max_locals = max_locals

        code_blob = blob[8:8 + c_len]
        with io.BytesIO(code_blob) as code_io:
            instructions = list(iter(
                lambda: Instruction.read(code_io, offset=code_io.tell()),
                None
            ))

            # Find all of the jump targets and make labels for them.
            labels = {
                target: f'label_{i}'
                for i, target in enumerate(
                    sorted(jump_targets(instructions)),
                    1
                )
            }

            for ins in instructions:
                # This instruction is a jump target so we want to prepend a
                # label node.
                if ins.pos in labels:
                    code += ast.Label(name=labels[ins.pos])

                ins_node = ast.Instruction(opcode=ins.mnemonic)
                for operand in ins.operands:
                    if isinstance(operand, dict):
                        # Lookupswitch has one unique operand which is a
                        # dict of value -> [relative] offset.
                        for match, offset in operand.items():
                            ins_node += ast.ConditionalJump(
                                match=match,
                                target=labels[ins.pos + offset]
                            )
                    elif operand.op_type == OperandTypes.BRANCH:
                        # Replace relative branch offsets with the branch
                        # label, since we lose the packed offset of
                        # instructions when converting to the AST.
                        ins_node += ast.Jump(
                            target=labels[ins.pos + operand.value]
                        )
                    elif operand.op_type == OperandTypes.CONSTANT:
                        # Decompose a Constant subclass into a higher-level AST
                        # object with no external references.
                        ins_node += pool[operand.value].as_ast
                    elif operand.op_type == OperandTypes.LOCAL:
                        ins_node += ast.Local(slot=operand.value)
                    elif operand.op_type == OperandTypes.LITERAL:
                        ins_node += ast.Number(value=operand.value)
                    elif operand.op_type != OperandTypes.PADDING:
                        # Alignement padding is fluff in the AST, we always
                        # know how to re-pad.
                        pass

                code += ins_node

        return code
