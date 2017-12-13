# -*- coding: utf8 -*-
import inspect
import pkgutil
import importlib
from struct import unpack, pack
from itertools import repeat

from jawa.util.stream import BufferStreamReader


class Attribute(object):
    def __init__(self, parent, name_index):
        self.parent = parent
        self.name_index = name_index

    @property
    def name(self):
        """
        The :class:`~jawa.constants.ConstantUtf8` with the name of this
        attribute.
        """
        return self.cf.constants[self.name_index]

    @property
    def cf(self):
        """
        The ClassFile that owns this attribute, if any.
        """
        return self.parent.cf

    def unpack(self, info):
        """
        Parses an instance of this attribute from the blob `info`.
        """
        raise NotImplementedError()

    def pack(self):
        """
        This attribute packed into its on-disk representation.
        """
        raise NotImplementedError()


class UnknownAttribute(Attribute):
    def __init__(self, parent, name_index):
        super(UnknownAttribute, self).__init__(parent, name_index)
        self.info = None

    def unpack(self, info):
        self.info = info

    def pack(self):
        return self.info


class AttributeTable(object):
    def __init__(self, cf, parent=None):
        super(AttributeTable, self).__init__()
        #: The ClassFile that ultimately owns this AttributeTable.
        self.cf = cf
        #: The parent AttributeTable, if one exists.
        self.parent = parent
        self._table = []

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
            info_blob = fio.read(length)
            self._table.append((name_index, info_blob))

    def __getitem__(self, key):
        attr = self._table[key]

        if not isinstance(attr, Attribute):
            name_index, info = attr[0], attr[1]
            name = self.cf.constants[name_index].value

            attribute_type = ATTRIBUTE_CLASSES.get(name, UnknownAttribute)
            self._table[key] = attr = attribute_type(self, name_index)
            if attribute_type is UnknownAttribute:
                attr.unpack(info)
            else:
                attr.unpack(BufferStreamReader(info))

        return attr

    def __len__(self):
        return len(self._table)

    def pack(self, fout):
        """
        Write the AttributeTable to the file-like object `fout`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when saving a ClassFile.

        :param fout: Any file-like object providing `write()`
        """
        fout.write(pack('>H', len(self._table)))
        for attribute in self:
            info = attribute.pack()
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
        self._table.append(attribute)
        return attribute

    def find(self, name=None, f=None):
        for idx, attribute in enumerate(self._table):
            if name is not None:
                # Optimization to filter solely on name without causing
                # a full attribute load.
                if not isinstance(attribute, Attribute) and f is None:
                    attr_name = self.cf.constants[attribute[0]].value
                    if attr_name != name:
                        continue
                elif name != attribute.name.value:
                    continue

            # Force an attribute load.
            if not isinstance(attribute, Attribute):
                attribute = self[idx]

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


#: A dictionary of known attribute subclasses at the time this module
#: was loaded.
ATTRIBUTE_CLASSES = get_attribute_classes()
