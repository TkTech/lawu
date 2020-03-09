import io

from struct import unpack
from itertools import repeat
from dataclasses import dataclass
from typing import Dict, BinaryIO, List

from lawu import ast
from lawu.blocks import jump_targets
from lawu.attribute import Attribute, read_attribute_table
from lawu.instructions import Instruction, OperandTypes


@dataclass
class CodeException:
    start_pc: int
    end_pc: int
    target: int
    handles: int


class CodeAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    @staticmethod
    def get_labels(instructions, exceptions) -> Dict[int, str]:
        """Given a list of instructions and exceptions, return a mapping
        of PC -> label."""
        labels = {
            target: f'label_{i}'
            for i, target in enumerate(
                sorted(jump_targets(instructions)),
                1
            )
        }

        for excs in exceptions.values():
            for exc in excs:
                if exc.target not in labels:
                    labels[exc.target] = f'catch_{len(labels) + 1}'

        return labels

    @staticmethod
    def exceptions_from_binary(source: BinaryIO) -> Dict[int, List[Exception]]:
        """Read an ExceptionTable from a binary Code attribute."""
        exception_table_length = unpack('>H', source.read(2))[0]
        exceptions = {}
        for _ in repeat(None, exception_table_length):
            exc = CodeException(*unpack('>HHHH', source.read(8)))
            exceptions.setdefault(exc.start_pc, []).append(exc)

        return exceptions

    @classmethod
    def from_binary(cls, pool, source: BinaryIO) -> ast.Code:
        code = ast.Code()
        max_stack, max_locals, c_len = unpack('>HHI', source.read(8))
        code.max_stack = max_stack
        code.max_locals = max_locals
        blob = source.read(c_len)

        # We need to read the exception table before disassembly,
        # since it provides additional jump targets.
        exceptions = cls.exceptions_from_binary(source)

        with io.BytesIO(blob) as code_io:
            instructions = list(iter(
                lambda: Instruction.read(code_io, offset=code_io.tell()),
                None
            ))

        labels = cls.get_labels(instructions, exceptions)

        block = code
        exc_stack = []
        for ins in instructions:
            # This instruction is a jump target so we want to prepend a
            # label node.
            if ins.pos in labels:
                block += ast.Label(name=labels[ins.pos])

            # We've found the end of a try-catch block.
            if exc_stack and ins.pos == exc_stack[-1].end_pc:
                exc = exc_stack.pop()
                block = block.parent

            # We've found the start of a try-catch block.
            if ins.pos in exceptions:
                excs = exceptions[ins.pos]
                for exc in excs:
                    exc_stack.append(exc)
                    # A handler of 0 means it is called for *all* types of
                    # exceptions. Typically used to implement the `finally`
                    # keyword.
                    if exc.handles != 0:
                        block += ast.TryCatch(
                            target=labels[exc.target],
                            handles=pool[exc.handles].name.value
                        )
                    else:
                        block += ast.Finally(target=labels[exc.target])

                    block = block.children[-1]

            ins_node = ast.Instruction(name=ins.name)
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

            block += ins_node

        code.extend(read_attribute_table(pool, source))
        return code
