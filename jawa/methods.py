# -*- coding: utf8 -*-
__all__ = ('MethodTable', 'Method')

from struct import unpack, pack
from itertools import repeat

from jawa.util.flags import Flags
from jawa.util.descriptor import method_descriptor
from jawa.attribute import AttributeTable
from jawa.attributes.code import CodeAttribute


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
        return self._attributes

    @property
    def returns(self):
        return method_descriptor(self.descriptor.value).returns

    @property
    def args(self):
        return method_descriptor(self.descriptor.value).args

    @property
    def code(self):
        """
        A shortcut for::

            method.attributes.find_one(name='Code')
        """
        return self.attributes.find_one(name='Code')

    def unpack(self, fio):
        """
        Read the Method from the file-like object `fio`.

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
        Write the Method to the file-like object `fout`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be calle=d for you when saving a ClassFile.

        :param fout: Any file-like object providing `write()`
        """
        fout.write(self.access_flags.pack())
        fout.write(pack(
            '>HH',
            self._name_index,
            self._descriptor_index
        ))
        self._attributes.pack(fout)


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

    def create(self, name, descriptor, code=None):
        """
        Creates a new method from `name` and `descriptor`. If `code` is not
        ``None``, add a `Code` attribute to this method.
        """
        method = Method(self._cf)
        name = self._cf.constants.create_utf8(name)
        descriptor = self._cf.constants.create_utf8(descriptor)
        method._name_index = name.index
        method._descriptor_index = descriptor.index
        method.access_flags.acc_public = True

        if code is not None:
            method.attributes.create(CodeAttribute)

        self.append(method)
        return method

    def __iter__(self):
        for method in self._table:
            yield method

    def unpack(self, fio):
        """
        Read the MethodTable from the file-like object `fio`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param fio: Any file-like object providing `read()`
        """
        method_count = unpack('>H', fio.read(2))[0]
        for _ in repeat(None, method_count):
            method = Method(self._cf)
            method.unpack(fio)
            self.append(method)

    def pack(self, fout):
        """
        Write the MethodTable to the file-like object `fout`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be calle=d for you when saving a ClassFile.

        :param fout: Any file-like object providing `write()`
        """
        fout.write(pack('>H', len(self)))
        for method in self._table:
            method.pack(fout)

    def find(self, name=None, args=None, returns=None, f=None):
        """
        Iterates over the methods table, yielding each matching method. Calling
        without any arguments is equivelent to iterating over the table. For
        example, to get all methods that take three integers and return void::

            for method in cf.methods.find(args='III', returns='V'):
                print(method.name.value)

        Or to get all private methods::

            is_private = lambda m: m.access_flags.acc_private
            for method in cf.methods.find(f=is_private):
                print method.name.value

        :param name: The name of the method(s) to find.
        :param args: The arguments descriptor (ex: ``III``)
        :param returns: The returns descriptor (Ex: ``V``)
        :param f: Any callable which takes one argument (the method).
        """
        for method in self._table:
            if name is not None and method.name.value != name:
                continue

            descriptor = method.descriptor.value
            end_para = descriptor.find(')')

            m_args = descriptor[1:end_para]
            if args is not None and args != m_args:
                continue

            m_returns = descriptor[end_para + 1:]
            if returns is not None and returns != m_returns:
                continue

            if f is not None and not f(method):
                continue

            yield method

    def find_one(self, *args, **kwargs):
        """
        Same as ``find()`` but returns only the first result, or `None` if
        nothing was found.
        """
        try:
            return next(self.find(*args, **kwargs))
        except StopIteration:
            return None

    def __len__(self):
        return len(self._table)
