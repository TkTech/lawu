import re
import json
import importlib

import click

from jawa.classloader import ClassLoader
from jawa.cf import ClassVersion, ClassFile
from jawa.attribute import get_attribute_classes
from jawa.util import bytecode, shell
from jawa.constants import UTF8


@click.group()
def cli():
    pass


@cli.command()
def attributes():
    """List enabled Attributes.

    Prints a list of all enabled ClassFile Attributes.
    """
    attribute_classes = get_attribute_classes()
    for name, class_ in attribute_classes.items():
        click.echo(
            u'{name} - Added in: {ai} ({cv})'.format(
                name=click.style(name, fg='green'),
                ai=click.style(class_.ADDED_IN, fg='yellow'),
                cv=click.style(
                    ClassVersion(*class_.MINIMUM_CLASS_VERSION).human,
                    fg='yellow'
                )
            )
        )


@cli.command()
@click.argument('mnemonic')
def ins(mnemonic):
    """Lookup instruction information.

    Lookup an instruction by its mnemonic.
    """
    try:
        opcode = bytecode.opcode_table[mnemonic]
    except KeyError:
        click.secho(u'No definition found.', fg='red')
        return

    click.echo(u'{mnemonic} (0x{op})'.format(
        mnemonic=click.style(opcode['mnemonic'], fg='green', underline=True),
        op=click.style(format(opcode['op'], '02x'), fg='green')
    ))

    if opcode.get('desc'):
        click.secho('Description:', fg='yellow')
        click.echo(opcode['desc'])

    if opcode['can_be_wide']:
        click.echo(u'This instruction can be prefixed by the WIDE opcode.')

    if opcode.get('runtime'):
        click.secho('Possible runtime exceptions:', fg='yellow')
        for runtime_exception in opcode['runtime']:
            click.echo('- {runtime_exception}'.format(
                runtime_exception=click.style(runtime_exception, fg='red')
            ))

    if opcode['operands']:
        click.secho(u'Operand Format:', fg='yellow')
        for operand_fmt, operand_type in opcode['operands']:
            click.echo(u'- {ty} as a {fmt}'.format(
                ty=click.style(operand_type.name, fg='yellow'),
                fmt=click.style(operand_fmt.name, fg='yellow')
            ))
    elif opcode['op'] in (0xAB, 0xAA, 0xC4):
        # lookup[table|switch] and WIDE.
        click.secho(u'\nOperand Format:', fg='yellow')
        click.echo(
            u'This is a special-case opcode with variable operand parsing.'
        )


@cli.command(name='shell')
@click.option('--class-path', '-cp', multiple=True)
def shell_command(class_path):
    """Drop into a debugging shell."""
    loader = ClassLoader(*class_path)
    shell.start_shell(local_ns={
        'ClassFile': ClassFile,
        'loader': loader,
        'constants': importlib.import_module('jawa.constants'),
    })


@cli.command(name='def2json')
@click.argument('source', type=click.File('rb'))
def definition_to_json(source):
    """Convert a bytecode.yaml file into a prepared bytecode.json.

    Jawa internally uses a YAML file to define all bytecode opcodes, operands,
    runtime exceptions, default transforms, etc...

    However since JSON is available in the python stdlib and YAML is not, we
    process this YAML file before distribution to prevent adding an unnecessary
    dependency.
    """
    try:
        import yaml
    except ImportError:
        click.echo(
            'The pyyaml module could not be found and is required'
            ' to use this command.',
            err=True
        )
        return

    y = yaml.load(source)

    for k, v in y.items():
        # We guarantee some keys should always exist to make life easier for
        # developers.
        v.setdefault('operands', None)
        v.setdefault('can_be_wide', False)
        v.setdefault('transform', {})
        v['mnemonic'] = k

    click.echo(json.dumps(y, indent=4, sort_keys=True))


@cli.command()
@click.argument('source', type=click.Path(exists=True))
def dependencies(source):
    """Output a list of all classes referenced by the given source."""
    loader = ClassLoader(source, max_cache=-1)
    all_dependencies = set()
    for klass in loader.classes:
        new_dependencies = loader.dependencies(klass) - all_dependencies
        all_dependencies.update(new_dependencies)
        for new_dep in new_dependencies:
            click.echo(new_dep)


@cli.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('regex')
@click.option(
    '--stop-on-first',
    default=False,
    is_flag=True,
    help='Stop iteration on first matching class.'
)
def grep(source, regex, stop_on_first=False):
    """Grep the constant pool of all classes in source."""
    loader = ClassLoader(source, max_cache=-1)
    r = re.compile(regex)

    def _matches(constant):
        return r.match(constant.value)

    for klass in loader.classes:
        it = loader.search_constant_pool(path=klass, type_=UTF8, f=_matches)
        if next(it, None):
            print(klass)
            if stop_on_first:
                break
