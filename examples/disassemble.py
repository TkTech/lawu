#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
A simple example disassembler.
"""
import sys
from jawa import ClassFile, Label
from jawa.util.bytecode import OperandTypes

if __name__ == '__main__':
    with open(sys.argv[1]) as fin:
        cf = ClassFile(fin)

        # The constant pool.
        print('; {0:->60}'.format(' constant pool'))
        print('; {0:->60}'.format(
            ' total: {0}'.format(cf.constants.count)
        ))
        for constant in cf.constants.find():
            print('; {0:04}: {1!r}'.format(constant.index, constant))

        # The fields table.
        print('; {0:->60}'.format(' fields'))
        print('; {0:->60}'.format(
            ' total: {0}'.format(cf.fields.count)
        ))
        for field in cf.fields.find():
            print('; {0!r}'.format(field))

        # The methods table.
        print('; {0:->60}'.format(' methods'))
        print('; {0:->60}'.format(
            ' total: {0}'.format(cf.methods.count)
        ))
        for method in cf.methods.find():
            # Find all enabled flags and print them out (such as acc_public
            # and acc_private)
            flags = method.access_flags.to_dict()
            flags = [k for k, v in flags.items() if v]

            print('{0} {1} {2}({3}) {{'.format(
                ' '.join(flags),
                method.returns.name,
                method.name.value,
                ', '.join(a.name + ('[]' * a.dimensions) for a in method.args)
            ).strip())

            if method.code:
                instructions, labels = method.code.disassemble(constants=False)
                for ins in instructions:
                    if ins.pos in labels:
                        print('=> {0.name}:'.format(labels[ins.pos]))

                    line = [
                        '{ins.pos:04}',
                        '[0x{ins.opcode:02X}]',
                        '{ins.mnemonic:>15} <-'
                    ]

                    for operand in ins.operands:
                        if isinstance(operand, Label):
                            line.append('J[{0}]'.format(operand.name))
                        elif operand.op_type == OperandTypes.CONSTANT_INDEX:
                            line.append('C[{0}]'.format(operand.value))
                        elif operand.op_type == OperandTypes.BRANCH:
                            line.append(operand)
                        elif operand.op_type == OperandTypes.LITERAL:
                            line.append('#[{0}]'.format(operand.value))
                        elif operand.op_type == OperandTypes.LOCAL_INDEX:
                            line.append('L[{0}]'.format(operand.value))

                    print('  ' + ' '.join(line).format(ins=ins))
            print('}')
