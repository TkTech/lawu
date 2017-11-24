#!/usr/bin/env python
# -*- coding: utf-8 -*-
import six
import click

from jawa.cf import ClassVersion
from jawa.attribute import get_attribute_classes


@click.group()
def cli():
    pass


@cli.command()
def attributes():
    """List enabled Attributes.

    Prints a list of all enabled ClassFile Attributes.
    """
    attribute_classes = get_attribute_classes()
    for name, class_ in six.iteritems(attribute_classes):
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
