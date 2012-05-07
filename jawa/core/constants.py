# -*- coding: utf8 -*-
from struct import unpack


class Constant(object):
    __slots__ = ()

    @property
    def pool(self):
        """
        Returns the :py:class:`jawa.core.constants.ConstantPool` that owns
        this `Constant`.
        """
        return self._p


class ConstantClass(Constant):
    __slots__ = ('_p', '_ni')

    def __init__(self, pool, name_index):
        self._p = pool
        self._ni = name_index

    @property
    def name(self):
        return self._p.get(self._ni)


class ConstantString(Constant):
    __slots__ = ('_p', '_si')

    def __init__(self, pool, string_index):
        self._p = pool
        self._si = string_index

    @property
    def string(self):
        return self._p.get(self._si)


class ConstantFieldRef(Constant):
    __slots__ = ('_p', '_ki', '_nti')

    def __init__(self, pool, klass_index, name_and_type_index):
        self._p = pool
        self._ki = klass_index
        self._nti = name_and_type_index

    @property
    def klass(self):
        return self._p.get(self._ki)

    @property
    def name_and_type(self):
        return self._p.get(self._nti)


class ConstantMethodRef(Constant):
    __slots__ = ('_p', '_ki', '_nti')

    def __init__(self, pool, klass_index, name_and_type_index):
        self._p = pool
        self._ki = klass_index
        self._nti = name_and_type_index

    @property
    def klass(self):
        return self._p.get(self._ki)

    @property
    def name_and_type(self):
        return self._p.get(self._nti)


class ConstantInterfaceMethodRef(Constant):
    __slots__ = ('_p', '_ki', '_nti')

    def __init__(self, pool, klass_index, name_and_type_index):
        self._p = pool
        self._ki = klass_index
        self._nti = name_and_type_index

    @property
    def klass(self):
        return self._p.get(self._ki)

    @property
    def name_and_type(self):
        return self._p.get(self._nti)


class ConstantInteger(Constant):
    __slots__ = ('_p', 'value')

    def __init__(self, pool, value):
        self._p = pool
        self.value = value


class ConstantFloat(Constant):
    __slots__ = ('_p', 'value')

    def __init__(self, pool, value):
        self._p = pool
        self.value = value


class ConstantLong(Constant):
    __slots__ = ('_p', 'value')

    def __init__(self, pool, value):
        self._p = pool
        self.value = value


class ConstantDouble(Constant):
    __slots__ = ('_p', 'value')

    def __init__(self, pool, value):
        self._p = pool
        self.value = value


class ConstantNameAndType(Constant):
    __slots__ = ('_p', '_ni', '_di')

    def __init__(self, pool, name_index, descriptor_index):
        self._p = pool
        self._ni = name_index
        self._di = descriptor_index

    @property
    def name(self):
        return self._p.get(self._ni)

    @property
    def descriptor(self):
        return self._p.get(self._di)


class ConstantUTF8(Constant):
    __slots__ = ('_p', 'value')

    def __init__(self, pool, value):
        self._p = pool
        self.value = value


class ConstantPool(object):
    def __init__(self):
        self._pool = {}

    def get(self, index):
        return self._pool.get(index, None)

    def _load_from_io(self, io):
        """
        A partly-optimized method to load a ConstantPool from a ClassFile. It
        should never be called manually.
        """
        read = io.read
        constants = self._pool

        count = unpack('>H', read(2))[0]
        iterable = xrange(1, count).__iter__()
        for index in iterable:
            tag = unpack('>B', read(1))[0]
            # CONSTANT_Class_info
            if tag == 7:
                constants[index] = ConstantClass(self,
                    *unpack('>H', read(2)))
            # CONSTANT_String_info
            elif tag == 8:
                constants[index] = ConstantString(self,
                    *unpack('>H', read(2)))
            # CONSTANT_Integer_info
            elif tag == 3:
                constants[index] = ConstantInteger(self,
                    *unpack('>i', read(4)))
            # CONSTANT_Float_info
            elif tag == 4:
                constants[index] = ConstantFloat(self,
                    *unpack('>f', read(4)))
            # CONSTANT_Long_info
            elif tag == 5:
                constants[index] = ConstantLong(self,
                    *unpack('>q', read(8)))
                next(iterable)
            # CONSTANT_Double_info
            elif tag == 6:
                constants[index] = ConstantDouble(self,
                    *unpack('>d', read(8)))
                next(iterable)
            # CONSTANT_NameAndType_info
            elif tag == 12:
                constants[index] = ConstantNameAndType(self,
                    *unpack('>HH', read(4)))
            # CONSTANT_Utf8_info
            elif tag == 1:
                # This is done this way for many reasons. In almost all cases,
                # this is the most common CONSTANT_* in any real application.
                # There is little point in a wrapper object for this type,
                # since the only way to get to it is through another CONSTANT_.
                constants[index] = read(unpack('>H', read(2))[0])
            # CONSTANT_Fieldref_info
            elif tag == 9:
                constants[index] = ConstantFieldRef(self,
                    *unpack('>HH', read(4)))
            # CONSTANT_Methodref_info
            elif tag == 10:
                constants[index] = ConstantMethodRef(self,
                    *unpack('>HH', read(4)))
            # CONSTANT_InterfaceMethodref_info
            elif tag == 11:
                constants[index] = ConstantInterfaceMethodRef(self,
                    *unpack('>HH', read(4)))
