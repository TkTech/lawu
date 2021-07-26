import io
import importlib
import traceback

import click

from lawu import constants
from lawu.classloader import ClassLoader
from lawu.cf import ClassFile
from lawu.util import shell


@click.group()
@click.option(
    '--class-path',
    '-cp',
    type=click.Path(exists=True),
    multiple=True,
    default=['.'],
    help='One or more classpaths to use when looking up files.'
)
@click.pass_context
def debug(ctx, class_path):
    """Debugging utilities."""
    ctx.ensure_object(dict)
    ctx.obj['loader'] = ClassLoader(*class_path)


@debug.command(name='shell')
@click.pass_context
def shell_command(ctx):
    """Drop into a debugging shell."""
    shell.start_shell(local_ns={
        'ClassFile': ClassFile,
        'loader': ctx.obj['loader'],
        'constants': importlib.import_module('lawu.constants'),
    })


@debug.command(name='tree')
@click.argument('source')
@click.pass_context
def tree_command(ctx, source):
    """View the AST for the given source file."""
    loader = ctx.obj['loader']
    cf = loader[source]

    with io.StringIO() as temp:
        cf.node.pprint(file=temp)
        click.echo_via_pager(temp.getvalue())


@debug.command(name='strings')
@click.argument('source')
@click.pass_context
def strings_command(ctx, source):
    """View all of the String entries in the constant pool.

    This is not the same as viewing all possible strings, since there may be
    human-readable values in other Utf8-type constants. These are only strings
    declared as such in the ClassFile.
    """
    loader = ctx.obj['loader']
    with loader.open(source + '.class') as fio:
        # 4 byte magic, 4 byte version
        fio.read(8)
        pool = constants.ConstantPool()
        pool.unpack(fio)

        for string in pool.find(type_=constants.String):
            click.echo(string)


@debug.command(name='test')
@click.pass_context
def test_command(ctx):
    """Simply attempts to parse every class file found in the classpath.

    When an error occurs, drops into a Lawu shell with the failed class already
    loaded. When done, use exit() to quit or ctrl-d to continue to the next
    failure.
    """
    loader = ctx.obj['loader']

    for klassname in loader.classes:
        cf = None

        try:
            cf = loader[klassname]
        except Exception as exc:
            traceback.print_exc()

            click.echo(f'Failed to load {klassname}, dropping to shell.')

            shell.start_shell(local_ns={
                'ClassFile': ClassFile,
                'loader': ctx.obj['loader'],
                'constants': importlib.import_module('lawu.constants'),
                'cf': cf,
                'exc': exc
            })
