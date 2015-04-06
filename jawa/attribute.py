# -*- coding: utf8 -*-
__all__ = (
    'AttributeTable',
    'Attribute',
    'UnknownAttribute'
)
from struct import unpack, pack
from itertools import repeat


class Attribute(object):
    def __init__(self, cf, name_index):
        self._cf = cf
        self._name_index = name_index

    @property
    def info(self):
        """
        This attribute packed into its on-disk representation.
        """
        raise NotImplementedError()

    @property
    def name(self):
        """
        The :class:`~jawa.constants.ConstantUtf8` with the name of this
        attribute.
        """
        return self._cf.constants[self._name_index]

    def unpack(self, info):
        """
        Parses an instance of this attribute from the blob `info`.
        """
        raise NotImplementedError()

    def pack(self):
        """
        This attribute packed into its on-disk representation.
        """
        return self.info

    @classmethod
    def create(cls, name):
        raise NotImplementedError()


class UnknownAttribute(Attribute):
    def unpack(self, info):
        self._info = info

    @property
    def info(self):
        return self._info


class AttributeTable(object):
    def __init__(self, cf):
        self._cf = cf
        self._table = []

    def _get_type(self, name):
        """
        Returns a `Attribute` subclass that can handle the attribute
        of type `name`, or :class:~jawa.attribute.UnknownAttribute if
        none is found.
        """
        return default_parsers.get(name, UnknownAttribute)

    def _from_io(self, fio):
        """
        Loads an existing `AttributeTable` from the file-like object
        `fio`.
        """
        count = unpack('>H', fio.read(2))[0]
        for _ in repeat(None, count):
            name_index, length = unpack('>HI', fio.read(6))
            name = self._cf.constants[name_index].value

            type_ = self._get_type(name)
            attribute = type_(self._cf, name_index)

            attribute.unpack(fio.read(length))
            self._table.append(attribute)

    def _to_io(self, fout):
        fout.write(pack('>H', self.count))
        for attribute in self._table:
            info = attribute.info
            fout.write(pack(
                '>HI',
                attribute.name.index,
                len(info)
            ))
            fout.write(info)

    def create(self, type_, *args, **kwargs):
        """
        Creates a new attribute of `type_`, appending it to the attribute
        table and returning it.
        """
        attribute = type_.create(self._cf, *args, **kwargs)
        self.append(attribute)
        return attribute

    @property
    def count(self):
        return len(self._table)

    def append(self, attribute):
        self._table.append(attribute)

    def find(self, name=None, f=None):
        for attribute in self._table:
            if name is not None and not attribute.name.value == name:
                continue

            if f is not None and not f(attribute):
                continue

            yield attribute

    def find_one(self, *args, **kwargs):
        """
        Same as ``find()`` but returns only the first result, or `None` if
        nothing was found.
        """
        try:
            return next(self.find(*args, **kwargs))
        except StopIteration:
            return None


# Attributes can contain other attributes and AttributeTable's,
# thus we have to do our import here.
# pylint: disable=cyclic-import
from jawa.attributes.code import CodeAttribute
from jawa.attributes.source_file import SourceFileAttribute
from jawa.attributes.constant_value import ConstantValueAttribute

default_parsers = {
    'Code': CodeAttribute,
    'SourceFile': SourceFileAttribute,
    'ConstantValue': ConstantValueAttribute
}
