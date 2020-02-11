import click
import keyword

PRELUDE = """\"\"\"
Machine-generated from bytecode.yaml. This file aids with typing and
autocompletion in IDEs by providing types for every instruction.
\"\"\"
from lawu._instruction import Instruction, OperandTypes
"""

BASE_INSTRUCTION_TEMPLATE = """
class {safename}(Instruction):
    \"\"\"{docstring}\"\"\"
    __slots__ = ()

    #: Numerical opcode for this instruction.
    op = {op:#04x}
    #: The JVM instruction name as appears in the specification.
    name = {name!r}
    #: Alias for the `name` property.
    mnemonic = name
    #: List of operands this instruction takes, if any.
    fmt = {operands!r}
    #: True if this instruction can be prefixed by WIDE.
    can_be_wide = {can_be_wide!r}
"""

SEQUEL = """
BY_OP = {{
{by_op}
}}
BY_NAME = {{
{by_name}
}}"""


@click.group()
def bytecode():
    pass


@bytecode.command(name='generate')
@click.argument('source')
def generate_command(source):
    """
    Generate the python stubs from a bytecode.yaml file.
    """
    try:
        import yaml
    except ImportError:
        click.echo('This advanced command requires that pyyaml is installed.')
        return

    with open(source, 'r') as definitions_io:
        definitions = yaml.safe_load(definitions_io)

    click.echo(PRELUDE)

    by_name = {}
    by_op = {}

    for k, v in definitions.items():
        operands = v.get('operands', tuple())
        operands = tuple(({
            'UBYTE': '>B',
            'BYTE': '>b',
            'USHORT': '>H',
            'SHORT': '>h',
            'INTEGER': '>i'
        }.get(size), {
            'CONSTANT_INDEX': 'C',
            'LOCAL_INDEX': 'I',
            'LITERAL': 'L',
            'BRANCH': 'B',
            'PADDING': 'P'
        }.get(of_type)) for (size, of_type) in operands)

        safename = f'{k}_' if keyword.iskeyword(k) else k

        click.echo(BASE_INSTRUCTION_TEMPLATE.format(
            safename=safename,
            op=v['op'],
            name=k,
            docstring=v.get('desc', ''),
            operands=operands,
            can_be_wide=v.get('can_be_wide', False)
        ))

        by_name[k] = safename
        by_op[v['op']] = safename

    click.echo(SEQUEL.format(
        by_op=',\n'.join(
            f'    {k!r}: {v}'
            for k, v in sorted(by_op.items(), key=lambda v: v[0])
        ),
        by_name=',\n'.join(
            f'    {k!r}: {v}'
            for k, v in sorted(by_name.items(), key=lambda v: v[0])
        ),
    ))
