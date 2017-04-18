# -*- coding: utf8 -*-
__all__ = (
    'ConstantPool',
    'Constant',
    'ConstantUTF8',
    'ConstantClass',
    'ConstantString',
    'ConstantRef',
    'ConstantFieldRef',
    'ConstantMethodRef',
    'ConstantInterfaceMethodRef',
    'ConstantInteger',
    'ConstantFloat',
    'ConstantLong',
    'ConstantDouble',
    'ConstantNameAndType',
    'ConstantMethodHandle',
    'ConstantMethodType',
    'ConstantInvokeDynamic',
)

from struct import unpack, pack

from jawa.util.utf import decode_modified_utf8, encode_modified_utf8


class Constant(object):
    """
    The base class for all ``Constant*`` types.
    """
    def __init__(self, pool, index):
        self._pool = pool
        self._index = index

    @property
    def pool(self):
        """
        The constant pool this constant belongs to.
        """
        return self._pool

    @property
    def index(self):
        """
        The index of this constant in the constant pool.
        """
        return self._index


class ConstantNumber(Constant):
    def __init__(self, pool, index, value):
        super(ConstantNumber, self).__init__(pool, index)
        self.value = value

    def __repr__(self):
        return '{0}(value={1!r})'.format(self.__class__.__name__, self.value)


class ConstantUTF8(Constant):
    TAG = 1

    def __init__(self, pool, index, value):
        super(ConstantUTF8, self).__init__(pool, index)
        self.value = value

    def __repr__(self):
        return 'ConstantUTF8(value={0!r})'.format(self.value)


class ConstantInteger(ConstantNumber):
    TAG = 3


class ConstantFloat(ConstantNumber):
    TAG = 4


class ConstantLong(ConstantNumber):
    TAG = 5


class ConstantDouble(ConstantNumber):
    TAG = 6


class ConstantClass(Constant):
    TAG = 7

    def __init__(self, pool, index, name_index):
        super(ConstantClass, self).__init__(pool, index)
        self._name_index = name_index

    @property
    def name(self):
        return self.pool.get(self._name_index)

    def __repr__(self):
        return 'ConstantClass(name={0!r})'.format(self.name)


class ConstantString(Constant):
    TAG = 8

    def __init__(self, pool, index, string_index):
        super(ConstantString, self).__init__(pool, index)
        self._string_index = string_index

    @property
    def string(self):
        return self.pool.get(self._string_index)

    def __repr__(self):
        return 'ConstantString(string={0!r})'.format(self.string)


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

    def __repr__(self):
        return '{0}(class_={1!r}, name_and_type={2!r})'.format(
            self.__class__.__name__, self.class_, self.name_and_type)


class ConstantFieldRef(ConstantRef):
    TAG = 9


class ConstantMethodRef(ConstantRef):
    TAG = 10


class ConstantInterfaceMethodRef(ConstantRef):
    TAG = 11


class ConstantNameAndType(Constant):
    TAG = 12

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

    def __repr__(self):
        return 'ConstantNameAndType(name={0!r}, descriptor={1!r})'.format(
            self.name, self.descriptor)

class ConstantMethodHandle(Constant):
    TAG = 15

    def __init__(self, pool, index, reference_kind, reference_index):
        super(ConstantMethodHandle, self).__init__(pool, index)
        self._reference_kind = reference_kind
        self._reference_index = reference_index

    @property
    def kind(self):
        return self.pool.get(self._reference_kind)

    @property
    def reference(self):
        return self.pool.get(self._reference_index)

    def __repr__(self):
        return 'ConstantMethodHandle(kind={0!r}, index={1!r})'.format(
            self.kind, self.reference)

class ConstantMethodType(Constant):
    TAG = 16

    def __init__(self, pool, index, descriptor_index):
        super(ConstantMethodType, self).__init__(pool, index)
        self._descriptor_index = descriptor_index

    @property
    def descriptor(self):
        return self.pool.get(self._descriptor_index)

    def __repr__(self):
        return 'ConstantMethodType(descriptor={0!r})'.format(
            self.descriptor)

class ConstantInvokeDynamic(Constant):
    TAG = 18

    def __init__(self, pool, index, bootstrap_method_attr_index, name_and_type_index):
        super(ConstantInvokeDynamic, self).__init__(pool, index)
        self._bootstrap_method_attr_index = bootstrap_method_attr_index
        self._name_and_type_index = name_and_type_index

    @property
    def methodAttr(self):
        return self.pool.get(self._bootstrap_method_attr_index)

    @property
    def nameAndType(self):
        return self.pool.get(self._name_and_type_index)

    def __repr__(self):
        return 'ConstantInvokeDynamic(methodAttr={0!r}, nameAndType={1!r})'.format(
            self.methodAttr, self.nameAndType)

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
    ConstantNameAndType,
    None,
    None,
    ConstantMethodHandle,
    ConstantMethodType,
    None,
    ConstantInvokeDynamic
)


# The format and size-on-disk of each type of constant
# in the constant pool.
_constant_fmts = (
    None, None, None,
    ('>i', 4),
    ('>f', 4),
    ('>q', 8),
    ('>d', 8),
    ('>H', 2),
    ('>H', 2),
    ('>HH', 4),
    ('>HH', 4),
    ('>HH', 4),
    ('>HH', 4),
    None,
    None,
    ('>BH', 3),
    ('>H', 2),
    None,
    ('>HH', 4)
)


class ConstantPool(object):
    def __init__(self):
        self._pool = [None]

    def append(self, constant):
        """
        Appends a new constant to the end of the pool.
        """
        self._pool.append(constant)

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
        if not isinstance(constant, Constant):
            constant = _constant_types[constant[0]](self, index, *constant[1:])
            self._pool[index] = constant
        return constant

    def __getitem__(self, idx):
        return self.get(idx)

    def __setitem__(self, idx, value):
        self._pool[idx] = value

    def find(self, type_=None, f=None):
        """
        Iterates over the pool, yielding each matching ``Constant``. Calling
        without any arguments is equivelent to iterating over the pool.

        :param type_: Any subclass of :class:`Constant` or ``None``.
        :param f: Any callable which takes one argument (the constant).
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
        """
        Creates a new :class:`ConstantUTF8`, adding it to the pool and
        returning it.

        :param value: The value of the new UTF8 string.
        """
        self.append((1, unicode(value)))
        return self.get(self.raw_count - 1)

    def create_integer(self, value):
        """
        Creates a new :class:`ConstantInteger`, adding it to the pool and
        returning it.

        :param value: The value of the new integer.
        """
        self.append((3, value))
        return self.get(self.raw_count - 1)

    def create_float(self, value):
        """
        Creates a new :class:`ConstantFloat`, adding it to the pool and
        returning it.

        :param value: The value of the new float.
        """
        self.append((4, value))
        return self.get(self.raw_count - 1)

    def create_long(self, value):
        """
        Creates a new :class:`ConstantLong`, adding it to the pool and
        returning it.

        :param value: The value of the new long.
        """
        self.append((5, value))
        self.append(None)
        return self.get(self.raw_count - 2)

    def create_double(self, value):
        """
        Creates a new :class:`ConstantDouble`, adding it to the pool and
        returning it.

        :param value: The value of the new Double.
        """
        self.append((6, value))
        self.append(None)
        return self.get(self.raw_count - 2)

    def create_class(self, name):
        """
        Creates a new :class:`ConstantClass`, adding it to the pool and
        returning it.

        :param name: The name of the new class.
        """
        self.append((
            7,
            self.create_utf8(name).index
        ))
        return self.get(self.raw_count - 1)

    def create_string(self, value):
        """
        Creates a new :class:`ConstantString`, adding it to the pool and
        returning it.

        :param value: The value of the new string as a UTF8 string.
        """
        self.append((
            8,
            self.create_utf8(value).index
        ))
        return self.get(self.raw_count - 1)

    def create_name_and_type(self, name, descriptor):
        """
        Creates a new :class:`ConstantNameAndType`, adding it to the pool and
        returning it.

        :param name: The name of the class.
        :param descriptor: The descriptor for `name`.
        """
        self.append((
            12,
            self.create_utf8(name).index,
            self.create_utf8(descriptor).index
        ))
        return self.get(self.raw_count - 1)

    def create_field_ref(self, class_, field, descriptor):
        """
        Creates a new :class:`ConstantFieldRef`, adding it to the pool and
        returning it.

        :param class_: The name of the class to which `field` belongs.
        :param field: The name of the field.
        :param descriptor: The descriptor for `field`.
        """
        self.append((
            9,
            self.create_class(class_).index,
            self.create_name_and_type(field, descriptor).index
        ))
        return self.get(self.raw_count - 1)

    def create_method_ref(self, class_, method, descriptor):
        """
        Creates a new :class:`ConstantMethodRef`, adding it to the pool and
        returning it.

        :param class_: The name of the class to which `method` belongs.
        :param method: The name of the method.
        :param descriptor: The descriptor for `method`.
        """
        self.append((
            10,
            self.create_class(class_).index,
            self.create_name_and_type(method, descriptor).index
        ))
        return self.get(self.raw_count - 1)

    def create_interface_method_ref(self, class_, if_method, descriptor):
        """
        Creates a new :class:`ConstantInterfaceMethodRef`, adding it to the
        pool and returning it.

        :param class_: The name of the class to which `if_method` belongs.
        :param if_method: The name of the interface method.
        :param descriptor: The descriptor for `if_method`.
        """
        self.append((
            11,
            self.create_class(class_).index,
            self.create_name_and_type(if_method, descriptor).index
        ))
        return self.get(self.raw_count - 1)

    def unpack(self, fio):
        """
        Read the ConstantPool from the file-like object `fio`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param fio: Any file-like object providing `read()`
        """
        # Reads in the ConstantPool (constant_pool in the JVM Spec)
        constant_pool_count = unpack('>H', fio.read(2))[0]

        # Pull this locally so CPython doesn't do a lookup each time.
        read = fio.read

        while constant_pool_count > 1:
            constant_pool_count -= 1
            # The 1-byte prefix identifies the type of constant.
            tag = unpack('>B', read(1))[0]

            if tag == 1:
                # CONSTANT_Utf8_info, a length prefixed UTF-8-ish string.
                length = unpack('>H', read(2))[0]
                self.append((tag, decode_modified_utf8(read(length))))
            else:
                # Every other constant type is trivial.
                fmt, size = _constant_fmts[tag]
                self.append((tag,) + unpack(fmt, read(size)))
                if tag in (5, 6):
                    # LONG (5) and DOUBLE (6) count as two entries in the
                    # pool.
                    self.append(None)
                    constant_pool_count -= 1

    def pack(self, fout):
        """
        Write the ConstantPool to the file-like object `fout`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be calle=d for you when saving a ClassFile.

        :param fout: Any file-like object providing `write()`
        """
        write = fout.write
        write(pack('>H', self.raw_count))

        for constant in self:
            if isinstance(constant, ConstantUTF8):
                encoded_value = encode_modified_utf8(constant.value)
                length = len(encoded_value)
                write(pack(
                    '>BH',
                    constant.TAG,
                    length
                ))
                write(encoded_value)
            elif isinstance(constant, ConstantInteger):
                write(pack(
                    '>Bi',
                    constant.TAG,
                    constant.value
                ))
            elif isinstance(constant, ConstantFloat):
                write(pack(
                    '>Bf',
                    constant.TAG,
                    constant.value
                ))
            elif isinstance(constant, ConstantLong):
                write(pack(
                    '>Bq',
                    constant.TAG,
                    constant.value
                ))
            elif isinstance(constant, ConstantDouble):
                write(pack(
                    '>Bd',
                    constant.TAG,
                    constant.value
                ))
            elif isinstance(constant, ConstantClass):
                write(pack(
                    '>BH',
                    constant.TAG,
                    constant._name_index
                ))
            elif isinstance(constant, ConstantString):
                write(pack(
                    '>BH',
                    constant.TAG,
                    constant._string_index
                ))
            elif isinstance(constant, ConstantRef):
                write(pack(
                    '>BHH',
                    constant.TAG,
                    constant._class_index,
                    constant._name_and_type_index
                ))
            elif isinstance(constant, ConstantNameAndType):
                write(pack(
                    '>BHH',
                    constant.TAG,
                    constant._name_index,
                    constant._descriptor_index
                ))
            elif isinstance(constant, ConstantMethodHandle):
                write(pack(
                    '>BBH',
                    constant.TAG,
                    constant._reference_kind,
                    constant._reference_index
                ))
            elif isinstance(constant, ConstantMethodType):
                write(pack(
                    '>BH',
                    constant.TAG,
                    constant._descriptor_index
                ))
            elif isinstance(constant, ConstantInvokeDynamic):
                write(pack(
                    '>BHH',
                    constant.TAG,
                    constant._bootstrap_method_attr_index,
                    constant._name_and_type_index
                ))

    def __len__(self):
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
