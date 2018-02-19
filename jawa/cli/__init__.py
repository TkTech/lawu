#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from jawa.cf import ClassVersion, ClassFile
from jawa.attribute import get_attribute_classes
from jawa.util import bytecode, shell, classloader


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
    """Drop into a debugging shell.

    Once the shell is loaded you can use `load(<class name>)` to load
    any class on the set classpath.
    """
    loader = classloader.ClassLoader()
    loader.add_path(*class_path)

    shell.start_shell(local_ns={
        'ClassFile': ClassFile,
        'load': loader.load,
        'loader': loader
    })
