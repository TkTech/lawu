# -*- coding: utf8 -*-
"""
Methods for parsing standard JVM type descriptors for fields and methods.
It does not depend on any other modules.

.. note::
    This module has not yet been optimized for performance and is not
    in its final form.
"""


class DescriptorError(Exception):
    pass


def method_descriptor(descriptor):
    """
    Parses a Method descriptor as described in section 4.3.3 of the JVM
    specification. Returns the method argument types and return type.
    """
    if not descriptor.startswith('('):
        raise DescriptorError('missing opening bracket')
    end_para = descriptor.find(')')
    if end_para == -1:
        raise DescriptorError('missing closing bracket')

    method_args = parse_descriptor(descriptor[1:end_para])
    return_args = parse_descriptor(descriptor[end_para + 1:])

    return method_args, return_args[0]


def field_descriptor(descriptor):
    """
    Parses a Field descriptor as described in section 4.3.2 of the JVM
    specification. Returns the simple type of the field.
    """
    return parse_descriptor(descriptor)[0]


# JVM Descriptor "BaseType" characters to their
# full simple type.
_HUMAN_NAMES = {
    'L': 'reference',
    'B': 'byte',
    'C': 'char',
    'D': 'double',
    'F': 'float',
    'I': 'int',
    'J': 'long',
    'S': 'short',
    'Z': 'boolean',
    'V': 'void'
}


def parse_descriptor(descriptor):
    """
    Uses a tiny state machine to parse JVM descriptors. To get useful wrappers
    around the results, use :py:method:`jawa.core.descriptor.method_descriptor`
    or :py:method:`jawa.core.descriptor.field_descriptor`.
    """
    # States:
    #   10 == NORMAL,
    #   20 == OBJECT REFERENCE
    state = 10
    tokens = []
    token = []
    dimensions = 0
    for char in descriptor:
        if state == 10 and char == 'L':
            state = 20
        elif state == 10 and char == '[':
            dimensions += 1
        elif state == 10:
            tokens.append((char, dimensions, _HUMAN_NAMES[char]))
            dimensions = 0
        elif state == 20 and char == ';':
            tokens.append((''.join(token), dimensions, 'reference'))
            dimensions = 0
            state = 10
            del token[:]
        elif state == 20:
            token.append(char)
    return tokens
