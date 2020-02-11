import click

from lawu.cli.debug import debug
from lawu.cli.bytecode import bytecode


@click.group()
def cli():
    pass


cli.add_command(debug)
cli.add_command(bytecode)
