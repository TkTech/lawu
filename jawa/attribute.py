# -*- coding: utf8 -*-
__all__ = (
    'AttributeTable',
    'Attribute',
    'UnknownAttribute'
)
from struct import unpack, pack
from itertools import repeat


class Attribute(object):
    def __init__(self, table, name_index=None):
        self._table = table
        self._cf = table.cf
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

    @property
    def table(self):
        """
        The AttributeTable that owns this attribute, if any.
        """
        return self._table

    @property
    def cf(self):
        """
        The ClassFile that owns this attribute, if any.
        """
        return self._cf

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


class AttributeTable(object):
    def __init__(self, cf, parent=None):
        self._cf = cf
        self._table = []
        self._parent = parent

    def _get_type(self, name):
        """
        Returns a `Attribute` subclass that can handle the attribute
        of type `name`, or :class:~jawa.attribute.UnknownAttribute if
        none is found.
        """
        return default_parsers.get(name, UnknownAttribute)

    def unpack(self, fio):
        """
        Read the ConstantPool from the file-like object `fio`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param fio: Any file-like object providing `read()`
        """
        count = unpack('>H', fio.read(2))[0]
        for _ in repeat(None, count):
            name_index, length = unpack('>HI', fio.read(6))
            name = self._cf.constants[name_index].value

            type_ = self._get_type(name)
            attribute = type_(self, name_index=name_index)

            attribute.unpack(fio.read(length))
            self._table.append(attribute)

    def pack(self, fout):
        """
        Write the AttributeTable to the file-like object `fout`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be calle=d for you when saving a ClassFile.

        :param fout: Any file-like object providing `write()`
        """
        fout.write(pack('>H', len(self)))
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
        attribute = type_(self, *args, **kwargs)
        self.append(attribute)
        return attribute

    def __len__(self):
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

    @property
    def cf(self):
        """
        The ClassFile that owns this Attribute, if any.
        """
        return self._cf

    @property
    def parent(self):
        """
        The parent attribute, if any.

        If this AttributeTable belongs to another Attribute, this will
        reference that attribute. For example, when parsing a StackMapTable
        attribute, this would point to the owning Code attribute.
        """
        return self._parent


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
