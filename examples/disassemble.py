import click

from jawa.classloader import ClassLoader
from jawa.util.bytecode import OperandTypes


@click.command()
@click.option('--class-path', multiple=True, type=click.Path(exists=True))
@click.argument('classes', nargs=-1)
def main(class_path, classes):
    loader = ClassLoader(*class_path)
    for class_ in classes:
        cf = loader[class_]

        # The constant pool.
        print('; {0:->60}'.format(' constant pool'))
        print('; {0:->60}'.format(
            ' total: {0}'.format(len(cf.constants))
        ))
        for constant in cf.constants:
            print('; {0:04}: {1!r}'.format(constant.index, constant))

        # The fields table.
        print('; {0:->60}'.format(' fields'))
        print('; {0:->60}'.format(
            ' total: {0}'.format(len(cf.fields))
        ))
        for field in cf.fields:
            print('; {0!r}'.format(field))

        # The methods table.
        print('; {0:->60}'.format(' methods'))
        print('; {0:->60}'.format(
            ' total: {0}'.format(len(cf.methods))
        ))
        for method in cf.methods:
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

            r = []
            if method.code:
                for ins in method.code.disassemble():
                    line = [
                        f'{ins.pos:04}',
                        f'[0x{ins.opcode:02X}]',
                        f'{ins.mnemonic:>15} <-'
                    ]

                    for operand in ins.operands:
                        if isinstance(operand, dict):
                            line.append(f'JT[{operand!r}]')
                            continue

                        line.append({
                            OperandTypes.CONSTANT_INDEX: f'C[{operand.value}]',
                            OperandTypes.BRANCH: f'J[{operand.value}]',
                            OperandTypes.LITERAL: f'#[{operand.value}]',
                            OperandTypes.LOCAL_INDEX: f'L[{operand.value}]',
                            OperandTypes.PADDING: 'P'
                        }[operand.op_type])

                    print('  ' + ' '.join(line))
            print('}')


if __name__ == '__main__':
    main()
