# -*- coding: utf8 -*-
from struct import unpack


from jawa.core.descriptor import method_descriptor, field_descriptor


class Constant(object):
    """
    The base type for all other ``Constant*`` types. Its primary purpose is
    to enable `isinstance(x, Constant)`.

    .. note::
        There is no ``Constant*`` type for CONSTANT_Utf8_info due to
        performance constraints.
    """
    __slots__ = ()

    @property
    def pool(self):
        """
        Returns the :py:class:`jawa.core.constants.ConstantPool` that owns
        this ``Constant``.
        """
        return self._p


class ConstantClass(Constant):
    """
    Represents the `CONSTANT_Class_info` structure from the
    ClassFile specification.
    """
    __slots__ = ('_p', '_ni')

    def __init__(self, pool, name_index):
        self._p = pool
        self._ni = name_index

    @property
    def name(self):
        return self._p.get(self._ni)

    def __repr__(self):
        return '<ConstantClass(name=%r)>' % self.name


class ConstantString(Constant):
    """
    Represents the `CONSTANT_String_info` structure from the
    ClassFile specification.
    """
    __slots__ = ('_p', '_si')

    def __init__(self, pool, string_index):
        self._p = pool
        self._si = string_index

    @property
    def string(self):
        return self._p.get(self._si)

    def __repr__(self):
        return '<ConstantString(string=%r)>' % self.string


class ConstantFieldRef(Constant):
    """
    Represents the `CONSTANT_FieldRef_info` structure from the ClassFile
    specification.
    """
    __slots__ = ('_p', '_ki', '_nti')

    def __init__(self, pool, class_index, name_and_type_index):
        self._p = pool
        self._ki = class_index
        self._nti = name_and_type_index

    @property
    def class_(self):
        """
        Resolves this constants `class_index` and returns the associated
        :py:class:`jawa.core.constants.ConstantClass`.

        .. note::
            Resolved on each access, caching of the result is recommended.
        """
        return self._p.get(self._ki)

    @property
    def name_and_type(self):
        """
        Resolves this constants `name_and_type_index` and returns the
        associated :py:class:`jawa.core.constants.ConstantNameAndType`.

        .. note::
            Resolved on each access, caching of the result is recommended.
        """
        return self._p.get(self._nti)

    def __repr__(self):
        return '<ConstantFieldRef(class_=%r, name_and_type=%r)>' % (
            self.class_, self.name_and_type)


class ConstantMethodRef(Constant):
    """
    Represents the `CONSTANT_MethodRef_info` structure from the ClassFile
    specification.
    """
    __slots__ = ('_p', '_ki', '_nti')

    def __init__(self, pool, class_index, name_and_type_index):
        self._p = pool
        self._ki = class_index
        self._nti = name_and_type_index

    @property
    def class_(self):
        """
        Resolves this constants `class_index` and returns the associated
        :py:class:`jawa.core.constants.ConstantClass`.

        .. note::
            Resolved on each access, caching of the result is recommended.
        """
        return self._p.get(self._ki)

    @property
    def name_and_type(self):
        """
        Resolves this constants `name_and_type_index` and returns the
        associated :py:class:`jawa.core.constants.ConstantNameAndType`.

        .. note::
            Resolved on each access, caching of the result is recommended.
        """
        return self._p.get(self._nti)

    def __repr__(self):
        return '<ConstantMethodRef(class_=%r, name_and_type=%r)>' % (
            self.class_, self.name_and_type)


class ConstantInterfaceMethodRef(Constant):
    """
    Represents the `CONSTANT_InterfaceMethodRef_info` structure from the
    ClassFile specification.
    """
    __slots__ = ('_p', '_ki', '_nti')

    def __init__(self, pool, class_index, name_and_type_index):
        self._p = pool
        self._ki = class_index
        self._nti = name_and_type_index

    @property
    def class_(self):
        """
        Resolves this constants `class_index` and returns the associated
        :py:class:`jawa.core.constants.ConstantClass`.

        .. note::
            Resolved on each access, caching of the result is recommended.
        """
        return self._p.get(self._ki)

    @property
    def name_and_type(self):
        """
        Resolves this constants `name_and_type_index` and returns the
        associated :py:class:`jawa.core.constants.ConstantNameAndType`.

        .. note::
            Resolved on each access, caching of the result is recommended.
        """
        return self._p.get(self._nti)

    def __repr__(self):
        return '<ConstantInterfaceMethodRef(class_=%r, name_and_type=%r)>' % (
            self.class_, self.name_and_type)


class ConstantInteger(Constant):
    """
    Represents the `CONSTANT_Integer_info` structure from the ClassFile
    specification.

    :ivar value: The value of this constant.
    """
    __slots__ = ('_p', 'value')

    def __init__(self, pool, value):
        self._p = pool
        self.value = value

    def __repr__(self):
        return '<ConstantInteger(value=%r)>' % self.value


class ConstantFloat(Constant):
    """
    Represents the `CONSTANT_Float_info` structure from the ClassFile
    specification.

    :ivar value: The value of this constant.
    """
    __slots__ = ('_p', 'value')

    def __init__(self, pool, value):
        self._p = pool
        self.value = value

    def __repr__(self):
        return '<ConstantFloat(value=%r)>' % self.value


class ConstantLong(Constant):
    """
    Represents the `CONSTANT_Long_info` structure from the ClassFile
    specification.

    :ivar value: The value of this constant.
    """
    __slots__ = ('_p', 'value')

    def __init__(self, pool, value):
        self._p = pool
        self.value = value

    def __repr__(self):
        return '<ConstantLong(value=%r)>' % self.value


class ConstantDouble(Constant):
    """
    Represents the `CONSTANT_Double_info` structure from the ClassFile
    specification.

    :ivar value: The value of this constant.
    """
    __slots__ = ('_p', 'value')

    def __init__(self, pool, value):
        self._p = pool
        self.value = value

    def __repr__(self):
        return '<ConstantDouble(value=%r)>' % self.value


class ConstantNameAndType(Constant):
    """
    Represents the `CONSTANT_NameAndType_info` structure from the ClassFile
    specification.
    """
    __slots__ = ('_p', '_ni', '_di')

    def __init__(self, pool, name_index, descriptor_index):
        self._p = pool
        self._ni = name_index
        self._di = descriptor_index

    @property
    def name(self):
        """
        Resolves this constants `name_index` and returns the name of the type.

        .. note::
            Resolved on each access, caching of the result is recommended.
        """
        return self._p.get(self._ni)

    @property
    def descriptor(self):
        """
        Resolves this constants `descriptor_index` and returns the descriptor
        for this type.

        .. note::
            Resolved on each access, caching of the result is recommended.
        """
        return self._p.get(self._di)

    @property
    def type_(self):
        """
        Returns a human-readable type for this ``ConstantNameAndType`` as
        parsed from the descriptor. If this descriptor is not for a ``Field``
        ``None`` will be returned instead.
        """
        descriptor = self.descriptor
        # Try to make sure this is actually a field descriptor.
        if ')' in descriptor:
            return None
        return field_descriptor(descriptor)

    @property
    def args(self):
        """
        Returns a tuple of human-readable method argument types for this
        ``ConstantNameAndType`` as parsed from the descriptor. If this
        descriptor is not for a ``Method`` ``None`` will be returned instead.
        """
        descriptor = self.descriptor
        if '(' not in descriptor:
            return None
        return method_descriptor(descriptor)[0]

    @property
    def returns(self):
        """
        Returns a the human-readable method return type for this
        ``ConstantNameAndType`` as parsed from the descriptor. If this
        descriptor is not for a ``Method`` ``None`` will be returned instead.
        """
        descriptor = self.descriptor
        if '(' not in  descriptor:
            return None
        return method_descriptor(descriptor)[1]

    def __repr__(self):
        return '<ConstantNameAndType(name=%r, descriptor=%r)>' % (
            self.name, self.descriptor)


class ConstantPool(object):
    """
    Implements a container around the Constant Pool as described in the JVM
    ClassFile specification.
    """
    def __init__(self):
        self._pool = {}

    def get(self, index, default=None):
        """
        Returns the ``Constant`` at `index`, or `default` if it does not exist.
        """
        return self._pool.get(index, default)

    def insert(self, constant, index=None):
        """
        Inserts the value of `constant` to `index`, potentially overwritting an
        existing value. If `index` is ``None``, the first free index is used.
        Returns the final `index`.

        .. warning::
            This does *not* invalidate a ``Constant`` whose indexes point to
            the overwritten value. They will instead resolve to the newly
            inserted value.
        """
        if index is not None:
            if index < 1:
                raise ValueError('index must be greater than 0.')
            self._pool[index] = constant
            return index

        if not self._pool:
            self._pool[1] = constant
            return 1

        existing = self._pool.keys()
        existing.sort()
        last = existing[0]
        for i in existing:
            if i > last + 1:
                break
            last = i
        self._pool[last + 1] = constant
        return last + 1

    __getitem__ = get
    __setitem__ = insert

    def remove(self, obj_or_index):
        """
        Removes `obj_or_index` from the pool. If `obj_or_index` is a subclass
        of :py:class:`jawa.core.constants.Constant` then it is removed by
        identity, otherwise it is deleted by index.
        """
        if isinstance(obj_or_index, (Constant, basestring)):
            for k, v in self._pool.items():
                if v is obj_or_index:
                    del self._pool[k]
                    break
            else:
                raise KeyError('constant not in pool.')
        else:
            del self._pool[obj_or_index]

    def find_index(self, constant):
        """
        Returns the index for `constant` in the pool, or ``None`` if it is
        not in the pool.
        """
        for k, v in self._pool.items():
            if v is constant:
                return k
        return None

    def find(self, type_=None, f=None):
        """
        Iterates over the pool, yielding each matching ``Constant``. Calling
        without any arguments is equivelent to iterating over the pool.

         * `type_` must be a subclass of ``Constant``.
         * `f` must be callable which takes one value (the constant)
        """
        for v in self._pool.itervalues():
            if type_ is not None and not isinstance(v, type_):
                continue

            if f is not None and not f(v):
                continue

            yield v

    def build_class(self, class_name):
        """
        Builds a new :py:class:`jawa.core.constants.ConstantClass` with
        the name `class_name` in the pool and returns a tuple of the index
        it was inserted at and the ``ConstantClass`` itself.
        """
        class_ = ConstantClass(self, self.insert(class_name))
        return self.insert(class_), class_

    def _load_from_io(self, io):
        """
        A partly-optimized method to load a ConstantPool from a ClassFile. It
        should never be called manually.
        """
        read = io.read
        constants = self._pool

        count = unpack('>H', read(2))[0]
        iterable = iter(xrange(1, count))
        for index in iterable:
            tag = ord(read(1))
            # CONSTANT_Utf8_info
            if tag == 1:
                # This is done this way for many reasons. In almost all cases,
                # this is the most common CONSTANT_* in any real application.
                # There is little point in a wrapper object for this type,
                # since the only way to get to it is through another CONSTANT_.
                constants[index] = read(unpack('>H', read(2))[0])
            # CONSTANT_Class_info
            elif tag == 7:
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
