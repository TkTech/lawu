# -*- coding: utf8 -*-
__all__ = (
    'AttributeTable',
    'Attribute',
    'UnknownAttribute',
    'ConstantValueAttribute',
    'SourceFileAttribute'
)
from struct import unpack_from, unpack, pack
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


class UnknownAttribute(Attribute):
    def unpack(self, info):
        self._info = info

    @property
    def info(self):
        return self._info


class ConstantValueAttribute(Attribute):
    def unpack(self, info):
        self._constantvalue_index = unpack_from('>H', info)[0]

    @property
    def info(self):
        return pack('>H', self._constantvalue_index)

    @property
    def constantvalue(self):
        return self._cf.constants[self._constantvalue_index]


class SourceFileAttribute(Attribute):
    def unpack(self, info):
        self._sourcefile_index = unpack_from('>H', info)[0]

    @property
    def info(self):
        return pack('>H', self._sourcefile_index)

    @property
    def sourcefile(self):
        return self._cf.constants[self._sourcefile_index]


_default_parsers = {
    'ConstantValue': ConstantValueAttribute,
    'SourceFile': SourceFileAttribute
}


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
        return _default_parsers.get(name, UnknownAttribute)

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
            fout.write(pack('>HI',
                attribute.name.index,
                len(info)
            ))
            fout.write(info)

    @property
    def count(self):
        return len(self._table)
