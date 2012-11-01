# -*- coding: utf8 -*-
__all__ = ('MethodTable', 'Method')

from struct import unpack, pack
from itertools import repeat

from jawa.util.flags import Flags
from jawa.attribute import AttributeTable


class Method(object):
    def __init__(self, cf):
        self._cf = cf
        self._access_flags = Flags('>H', {
            'acc_public': 0x0001,
            'acc_private': 0x0002,
            'acc_protected': 0x0004,
            'acc_static': 0x0008,
            'acc_final': 0x0010,
            'acc_synchronized': 0x0020,
            'acc_bridge': 0x0040,
            'acc_varargs': 0x0080,
            'acc_native': 0x0100,
            'acc_abstract': 0x0400,
            'acc_strict': 0x0800,
            'acc_synthetic': 0x1000
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


class MethodTable(object):
    def __init__(self, cf):
        self._cf = cf
        self._table = []

    def append(self, method):
        self._table.append(method)

    def find_and_remove(self, f):
        """
        Removes any and all methods for which `f(method)` returns `True`.
        """
        self._table = [fld for fld in self._table if not f(fld)]

    def remove(self, method):
        """
        Removes a `method` from the table by identity.
        """
        self._table = [fld for fld in self._table if fld is not method]

    def create(self, name, descriptor, flags=None, attribs=None):
        """
        Creates a new method from `name` and `descriptor`.
        """
        self._cf.constants.add()

    def __iter__(self):
        for method in self._table:
            yield method

    def _from_io(self, fio):
        method_count = unpack('>H', fio.read(2))[0]
        for _ in repeat(None, method_count):
            method = Method(self._cf)
            method._from_io(fio)
            self.append(method)

    def _to_io(self, fout):
        fout.write(pack('>H', self.count))
        for method in self._table:
            method._to_io(fout)

    @property
    def count(self):
        return len(self._table)
