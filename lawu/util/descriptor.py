"""
Methods for parsing standard JVM type descriptors for fields and methods.
"""
from collections import namedtuple


JVMType = namedtuple('JVMType', [
    'base_type',
    'dimensions',
    'name'
])

MethodDescriptor = namedtuple('MethodDescriptor', [
    'returns',
    'args',
    'returns_descriptor',
    'args_descriptor',
    'descriptor'
])


def method_descriptor(descriptor: str) -> MethodDescriptor:
    """
    Parses a Method descriptor as described in section 4.3.3 of the JVM
    specification.
    """
    end_para = descriptor.find(')')
    returns = descriptor[end_para + 1:]
    args = descriptor[1:end_para]

    return MethodDescriptor(
        parse_descriptor(returns)[0],
        parse_descriptor(args),
        returns,
        args,
        descriptor
    )


def field_descriptor(descriptor: str) -> str:
    """
    Parses a Field descriptor as described in section 4.3.2 of the JVM
    specification.
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


def parse_descriptor(descriptor: str) -> list:
    """
    Uses a tiny state machine to parse JVM descriptors. To get useful wrappers
    around the results, use :py:func:`lawu.core.descriptor.method_descriptor`
    or :py:func:`lawu.core.descriptor.field_descriptor`.
    """
    # TokenType:
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
            tokens.append(JVMType(char, dimensions, _HUMAN_NAMES[char]))
            dimensions = 0
        elif state == 20 and char == ';':
            tokens.append(JVMType('L', dimensions, ''.join(token)))
            dimensions = 0
            state = 10
            del token[:]
        elif state == 20:
            token.append(char)
    return tokens
