import click
import itertools
from rich.console import Console

from lawu import instructions, attribute, ast
from lawu.cli.debug import debug
from lawu.cli.bytecode import bytecode
from lawu.util.structify import structify


@click.group()
def cli():
    pass


@cli.command('what')
@click.argument('topic')
def what_command(topic):
    """Displays information about known JVM instructions, attribute entries,
    and types.
    """
    console = Console()

    topic = topic.lower()
    if topic.isdigit():
        ins = instructions.BY_OP.get(int(topic))
    else:
        ins = instructions.BY_NAME.get(topic)

    if ins:
        console.print(
            f'[magenta]{topic}[/] is a [magenta]JVM instruction.[/]'
        )
        # Need to special case lookupswitch and tableswitch, which do not
        # follow the regular instruction rules and thus aren't encoded in
        # the instruction table.

        console.print(f'[green bold]Name:[/] {ins.name}')
        console.print(f'[green bold]Description:[/] {ins.__doc__}')
        console.print(
            f'[green bold]Opcode:[/] '
            f'Hex: {ins.op:#02x} / Dec: {ins.op} / Oct: {ins.op:o}'
        )
        console.print(f'[green bold]Has a wide version:[/] {ins.can_be_wide}')

        if ins.fmt:
            # Opcode has operands
            segments = list(itertools.chain.from_iterable(
                structify(
                    fmt,
                    labels=(instructions.OperandTypes(of_type).name,)
                ) for fmt, of_type in ins.fmt
            ))
            console.print('[green bold]Has operands:[/]')
            for seg in segments:
                console.print(
                    f'- A [magenta]{seg.label}[/] field, which is a'
                    f' [magenta]{seg.of_type.name}[/]'
                    f' of {seg.size} bytes'
                )

        return

    all_attributes = attribute.get_attribute_classes()
    attr = all_attributes.get(topic)
    if attr:
        console.print(
            f'[magenta]{topic}[/] is a [magenta]JVM attribute.[/]'
        )

        console.print(f'[green bold]Added in:[/] Java SE {attr.ADDED_IN}')
        console.print(
            f'[green bold]Minimum Class Version:[/]'
            f' Major: {attr.MINIMUM_CLASS_VERSION[0]:#02x} /'
            f' Minor: {attr.MINIMUM_CLASS_VERSION[1]:#02x}'
        )


cli.add_command(debug)
cli.add_command(bytecode)
