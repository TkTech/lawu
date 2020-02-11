"""
ClassFile reader & writer.

The :mod:`jawa.cf` module provides tools for working with JVM ``.class``
ClassFiles.
"""
from itertools import repeat
from typing import BinaryIO
from struct import unpack

from jawa import ast
from jawa import constants as consts
from jawa.attribute import get_attribute_classes


def _parse_attribute_table(pool, source):
    size = unpack('>H', source.read(2))[0]
    for _ in repeat(None, size):
        name_idx, length = unpack('>HI', source.read(6))
        yield pool[name_idx].value, source.read(length)


class ClassFile:
    #: The JVM ClassFile magic number.
    MAGIC = 0xCAFEBABE

    def __init__(self, source: BinaryIO = None, *, loader=None):
        self.node = ast.Class(
            descriptor=None,
            access_flags=['public'],
            children=[
                ast.Bytecode(major=0x33, minor=0x00),
                ast.Super(descriptor='java/lang/Object')
            ]
        )

        if source:
            self._load_from_io(source)

    def _load_from_io(self, source: BinaryIO):
        """Given a file-like object parse a binary JVM ClassFile into the Jawa
        internal AST model.

        :param source: Any file-like object implementing `read()`.
        """
        read = source.read

        if unpack('>I', read(4))[0] != ClassFile.MAGIC:
            raise ValueError('invalid magic number')

        version = unpack('>HH', read(4))
        v = self.node.find_one(name='bytecode')
        v.major = version[1]
        v.minor = version[0]

        pool = consts.ConstantPool()
        pool.unpack(source)

        # FIXME: Access flags
        read(2)
        this, super_, if_count = unpack('>HHH', read(6))
        self.this = pool[this].name.value
        self.super_ = pool[super_].name.value

        self.node.extend(
            ast.Implements(
                descriptor=pool[if_idx].name.value
            )
            for if_idx in unpack(f'>{if_count}H', read(2 * if_count))
        )

        attributes = get_attribute_classes()

        for _ in repeat(None, unpack('>H', read(2))[0]):
            flags, name, descriptor = unpack('>HHH', read(6))
            field = ast.Field(
                name=pool[name].value,
                descriptor=pool[descriptor].value,
                # FIXME: Access flags
                access_flags=['temp'],
            )

            for name, blob in _parse_attribute_table(pool, source):
                field += attributes[name.lower()](pool, source, blob)

            self.node += field

        for _ in repeat(None, unpack('>H', read(2))[0]):
            flags, name, descriptor = unpack('>HHH', read(6))
            method = ast.Method(
                name=pool[name].value,
                descriptor=pool[descriptor].value,
                # FIXME: Access flags
                access_flags=['temp']
            )

            for name, blob in _parse_attribute_table(pool, source):
                attr_parser = attributes.get(name.lower())
                if attr_parser:
                    method += attr_parser.from_binary(pool, source, blob)

            self.node += method

    @property
    def this(self):
        return self.node.descriptor

    @this.setter
    def this(self, value):
        self.node.descriptor = value

    @property
    def super_(self):
        return self.node.find_one(name='super').descriptor

    @super_.setter
    def super_(self, value):
        self.node.find_one(name='super').descriptor = value

    @property
    def methods(self):
        return self.node.find(name='method')

    @property
    def fields(self):
        return self.node.find(name='field')
