# -*- coding: utf8 -*-
__all__ = ('FieldTable', 'Field')

from struct import unpack, pack
from itertools import repeat

from jawa.util.flags import Flags
from jawa.attribute import AttributeTable
from jawa.attributes.constant_value import ConstantValueAttribute


class Field(object):
    def __init__(self, cf):
        self._cf = cf
        self._access_flags = Flags('>H', {
            'acc_public': 0x0001,
            'acc_private': 0x0002,
            'acc_protected': 0x0004,
            'acc_static': 0x0008,
            'acc_final': 0x0010,
            'acc_volatile': 0x0040,
            'acc_transient': 0x0080,
            'acc_synthetic': 0x1000,
            'acc_enum': 0x4000
        })
        self._name_index = 0
        self._descriptor_index = 0
        self._attributes = AttributeTable(cf)

    @property
    def descriptor(self):
        return self._cf.constants[self._descriptor_index]

    @property
    def name(self):
        return self._cf.constants[self._name_index]

    @property
    def access_flags(self):
        return self._access_flags

    @property
    def attributes(self):
        return self._attributes

    @property
    def value(self):
        """
        A shortcut for the field's ConstantValue attribute, should one exist.
        """
        constant_value = self.attributes.find_one(name='ConstantValue')
        return constant_value

    def unpack(self, fio):
        """
        Read the Field from the file-like object `fio`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param fio: Any file-like object providing `read()`
        """
        self.access_flags.unpack(fio.read(2))
        self._name_index, self._descriptor_index = unpack('>HH', fio.read(4))
        self._attributes.unpack(fio)

    def pack(self, fout):
        """
        Write the Field to the file-like object `fout`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be calle=d for you when saving a ClassFile.

        :param fout: Any file-like object providing `write()`
        """
        fout.write(self.access_flags.pack())
        fout.write(pack('>HH', self._name_index, self._descriptor_index))
        self._attributes.pack(fout)


class FieldTable(object):
    def __init__(self, cf):
        self._cf = cf
        self._table = []

    def append(self, field):
        self._table.append(field)

    def find_and_remove(self, f):
        """
        Removes any and all fields for which `f(field)` returns `True`.
        """
        self._table = [fld for fld in self._table if not f(fld)]

    def remove(self, field):
        """
        Removes a `Field` from the table by identity.
        """
        self._table = [fld for fld in self._table if fld is not field]

    def create(self, name, descriptor):
        """
        Creates a new field from `name` and `descriptor`. For example::

            >>> from jawa import ClassFile
            >>> cf = ClassFile.create('BeerCounter')
            >>> field = cf.fields.create('BeerCount', 'I')

        """
        field = Field(self._cf)
        name = self._cf.constants.create_utf8(name)
        descriptor = self._cf.constants.create_utf8(descriptor)
        field._name_index = name.index
        field._descriptor_index = descriptor.index
        field.access_flags.acc_public = True
        self.append(field)
        return field

    def create_static(self, name, descriptor, value):
        """
        A shortcut for creating a static field with a
        :class:`~jawa.attributes.constant_value.ConstantValueAttribute`
        set to the :class:`~jawa.constants.Constant` `value`. For example,
        to create a string with the classic "Hello World!"::

            >>> from jawa import ClassFile
            >>> cf = ClassFile.create('BeerCounter')
            >>> field = cf.fields.create_static(
            ...    'HelloWorld',
            ...    'Ljava/lang/String;',
            ...    cf.constants.create_string('Hello World!')
            ... )
        """
        field = self.create(name, descriptor)
        field.attributes.create(ConstantValueAttribute, value)
        field.access_flags.acc_static = True
        return field

    def __iter__(self):
        for field in self._table:
            yield field

    def unpack(self, fio):
        """
        Read the FieldTable from the file-like object `fio`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param fio: Any file-like object providing `read()`
        """
        field_count = unpack('>H', fio.read(2))[0]
        for _ in repeat(None, field_count):
            field = Field(self._cf)
            field.unpack(fio)
            self.append(field)

    def pack(self, fout):
        """
        Write the FieldTable to the file-like object `fout`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be calle=d for you when saving a ClassFile.

        :param fout: Any file-like object providing `write()`
        """
        fout.write(pack('>H', len(self)))
        for field in self._table:
            field.pack(fout)

    def __len__(self):
        return len(self._table)

    def find(self, name=None, type_=None, f=None):
        """
        Iterates over the fields table, yielding each matching method. Calling
        without any arguments is equivelent to iterating over the table.

        :param name: The name of the field(s) to find.
        :param type_: The field descriptor (Ex: 'I')
        :param f: Any callable which takes one argument (the field).
        """
        for field in self._table:
            if name is not None and field.name.value != name:
                continue

            descriptor = field.descriptor.value
            if type_ is not None and type_ != descriptor:
                continue

            if f is not None and not f(field):
                continue

            yield field

    def find_one(self, *args, **kwargs):
        """
        Same as ``find()`` but returns only the first result, or `None` if
        nothing was found.
        """
        try:
            return next(self.find(*args, **kwargs))
        except StopIteration:
            return None
