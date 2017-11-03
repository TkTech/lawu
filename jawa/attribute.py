# -*- coding: utf8 -*-
import inspect
import pkgutil
import importlib
from struct import unpack, pack
from itertools import repeat

from jawa.util.stream import BufferStreamReader


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
        return get_attribute_classes().get(name, UnknownAttribute)

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
            attribute_info = fio.read(length)

            if isinstance(attribute, UnknownAttribute):
                attribute.unpack(attribute_info)
            else:
                attribute.unpack(BufferStreamReader(attribute_info))
            self._table.append(attribute)

    def pack(self, fout):
        """
        Write the AttributeTable to the file-like object `fout`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when saving a ClassFile.

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


def get_attribute_classes():
    """
    Lookup all builtin Attribute subclasses, load them, and return a dict
    of attribute name to class.

    :rtype: dict
    """
    attribute_children = pkgutil.iter_modules(
        importlib.import_module('jawa.attributes').__path__,
        prefix='jawa.attributes.'
    )

    result = {}
    for _, name, _ in attribute_children:
        classes = inspect.getmembers(
            importlib.import_module(name),
            lambda c: (
                inspect.isclass(c) and issubclass(c, Attribute) and
                c is not Attribute
            )
        )

        for class_name, class_ in classes:
            attribute_name = getattr(class_, 'ATTRIBUTE_NAME', class_name[:-9])
            result[attribute_name] = class_

    return result
