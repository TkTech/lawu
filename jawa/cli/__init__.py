import click

from jawa.cli.debug import debug
from jawa.cli.bytecode import bytecode


@click.group()
def cli():
    pass


cli.add_command(debug)
cli.add_command(bytecode)
