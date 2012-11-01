# -*- coding: utf8 -*-
__all__ = (
    'ConstantPool',
    'Constant',
    'ConstantUTF8',
    'ConstantClass',
    'ConstantString',
    'ConstantFieldRef',
    'ConstantMethodRef',
    'ConstantFieldRef',
    'ConstantInterfaceMethodRef',
    'ConstantInteger',
    'ConstantFloat',
    'ConstantLong',
    'ConstantDouble',
    'ConstantNameAndType'
)


class Constant(object):
    def __init__(self, pool, index):
        self._pool = pool
        self._index = index

    @property
    def pool(self):
        return self._pool

    @property
    def index(self):
        return self._index

    def raw(self):
        raise NotImplementedError()

    def commit(self):
        self.pool.raw_set(self.index, self.raw())

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.commit()


class ConstantNumber(Constant):
    def __init__(self, pool, index, value):
        super(ConstantNumber, self).__init__(pool, index)
        self.value = value


class ConstantUTF8(Constant):
    def __init__(self, pool, index, value):
        super(ConstantUTF8, self).__init__(pool, index)
        self.value = value

    def raw(self):
        return (1, self.value)


class ConstantInteger(ConstantNumber):
    def raw(self):
        return (3, self.value)


class ConstantFloat(ConstantNumber):
    def raw(self):
        return (4, self.value)


class ConstantLong(ConstantNumber):
    def raw(self):
        return (5, self.value)


class ConstantDouble(ConstantNumber):
    def raw(self):
        return (6, self.value)


class ConstantClass(Constant):
    def __init__(self, pool, index, name_index):
        super(ConstantClass, self).__init__(pool, index)
        self._name_index = name_index

    @property
    def name(self):
        return self.pool.get(self._name_index)

    def raw(self):
        return (7, self._name_index)


class ConstantString(Constant):
    def __init__(self, pool, index, string_index):
        super(ConstantString, self).__init__(pool, index)
        self._string_index = string_index

    @property
    def string(self):
        return self.pool.get(self._string_index)

    def raw(self):
        return (8, self._string_index)


class ConstantRef(Constant):
    def __init__(self, pool, index, class_index, name_and_type_index):
        super(ConstantRef, self).__init__(pool, index)
        self._class_index = class_index
        self._name_and_type_index = name_and_type_index

    @property
    def class_(self):
        return self.pool.get(self._class_index)

    @property
    def name_and_type(self):
        return self.pool.get(self._name_and_type_index)


class ConstantFieldRef(ConstantRef):
    def raw(self):
        return (9, self._class_index, self._name_and_type_index)


class ConstantMethodRef(ConstantRef):
    def raw(self):
        return (10, self._class_index, self._name_and_type_index)


class ConstantInterfaceMethodRef(ConstantRef):
    def raw(self):
        return (11, self._class_index, self._name_and_type_index)


class ConstantNameAndType(Constant):
    def __init__(self, pool, index, name_index, descriptor_index):
        super(ConstantNameAndType, self).__init__(pool, index)
        self._name_index = name_index
        self._descriptor_index = descriptor_index

    @property
    def name(self):
        return self.pool.get(self._name_index)

    @property
    def descriptor(self):
        return self.pool.get(self._descriptor_index)

    def raw(self):
        return (12, self._name_index, self._descriptor_index)


_constant_types = (
    None,
    ConstantUTF8,
    None,
    ConstantInteger,
    ConstantFloat,
    ConstantLong,
    ConstantDouble,
    ConstantClass,
    ConstantString,
    ConstantFieldRef,
    ConstantMethodRef,
    ConstantInterfaceMethodRef,
    ConstantNameAndType
)


class ConstantPool(object):
    def __init__(self):
        self._pool = [None]

    def append(self, constant):
        """
        Appends a new constant to the end of the pool.
        """
        self._pool.append(constant)

    def raw(self, index):
        """
        Returns the "raw" constant for `index`. Typically only useful for
        calculating size-on-disk and for saving.
        """
        return self._pool[index]

    def __iter__(self):
        for index, constant in enumerate(self._pool):
            if constant is not None:
                yield self.get(index)

    def get(self, index):
        """
        Returns the `Constant` at `index`, raising a KeyError if it
        does not exist.
        """
        constant = self._pool[index]
        return _constant_types[constant[0]](self, index, *constant[1:])

    def __getitem__(self, idx):
        return self.get(idx)

    def raw_set(self, idx, value):
        """
        Overwrites the 'raw' constant at `idx` with `value`.
        """
        self._pool[idx] = value

    def find(self, type_=None, f=None):
        """
        Iterates over the pool, yielding each matching ``Constant``. Calling
        without any arguments is equivelent to iterating over the pool.

         * `type_` must be a subclass of ``Constant``.
         * `f` must be callable which takes one value (the constant)
        """
        for constant in self:
            if type_ is not None and not isinstance(constant, type_):
                continue

            if f is not None and not f(constant):
                continue

            yield constant

    def find_one(self, *args, **kwargs):
        """
        Same as ``find()`` but returns only the first result, or `None` if
        nothing was found.
        """
        try:
            return next(self.find(*args, **kwargs))
        except StopIteration:
            return None

    def create_utf8(self, value):
        self.append((1, value))
        return self.get(-1)

    # -------------
    # Properties
    # -------------

    @property
    def count(self):
        """
        The number of `Constants` in the `ConstantPool`, excluding padding.
        """
        count = 0
        for constant in self._pool:
            if constant is not None:
                count += 1
        return count

    @property
    def raw_count(self):
        """
        The number of `Constants` in the `ConstantPool`, including padding.
        """
        return len(self._pool)
