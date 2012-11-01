# -*- coding: utf8 -*-
__all__ = ('FieldTable', 'Field')

from struct import unpack, pack
from itertools import repeat

from jawa.util.flags import Flags
from jawa.attribute import AttributeTable


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
        return self._attribs

    def _from_io(self, fio):
        self.access_flags.unpack(fio.read(2))
        self._name_index, self._descriptor_index = unpack('>HH', fio.read(4))
        self._attributes._from_io(fio)

    def _to_io(self, fout):
        fout.write(self.access_flags.pack())
        fout.write(pack('>HH',
            self._name_index,
            self._descriptor_index
        ))
        self._attributes._to_io(fout)


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

    def create(self, name, descriptor, flags=None, attribs=None):
        """
        Creates a new field from `name` and `descriptor`.
        """
        self._cf.constants.add()

    def __iter__(self):
        for field in self._table:
            yield field

    def _from_io(self, fio):
        field_count = unpack('>H', fio.read(2))[0]
        for _ in repeat(None, field_count):
            field = Field(self._cf)
            field._from_io(fio)
            self.append(field)

    def _to_io(self, fout):
        fout.write(pack('>H', self.count))
        for field in self._table:
            field._to_io(fout)

    @property
    def count(self):
        return len(self._table)
