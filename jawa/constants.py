from struct import unpack, pack

from jawa.util.utf import decode_modified_utf8, encode_modified_utf8


class Constant(object):
    """
    The base class for all ``Constant*`` types.
    """
    __slots__ = ('pool', 'index')

    def __init__(self, pool, index):
        self.pool = pool
        self.index = index


class Number(Constant):
    __slots__ = ('value',)

    def __init__(self, pool, index, value):
        super().__init__(pool, index)
        self.value = value

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'index={self.index}, value={self.value!r})'
        )


class UTF8(Constant):
    __slots__ = ('value',)
    TAG = 1

    def __init__(self, pool, index, value):
        super().__init__(pool, index)
        self.value = value

    def pack(self):
        encoded_value = encode_modified_utf8(self.value)
        return pack('>BH', self.TAG, len(encoded_value)) + encoded_value

    def __repr__(self):
        return f'<UTF8(index={self.index}, value={self.value!r}>)'


class Integer(Number):
    TAG = 3

    def pack(self):
        return pack('>Bi', self.TAG, self.value)


class Float(Number):
    TAG = 4

    def pack(self):
        return pack('>Bf', self.TAG, self.value)


class Long(Number):
    TAG = 5

    def pack(self):
        return pack('>Bq', self.TAG, self.value)


class Double(Number):
    TAG = 6

    def pack(self):
        return pack('>Bd', self.TAG, self.value)


class ConstantClass(Constant):
    __slots__ = ('name_index',)
    TAG = 7

    def __init__(self, pool, index, name_index):
        super().__init__(pool, index)
        self.name_index = name_index

    @property
    def name(self):
        return self.pool.get(self.name_index)

    def pack(self):
        return pack('>BH', self.TAG, self.name_index)

    def __repr__(self):
        return f'<ConstantClass(index={self.index}, name={self.name!r})>'


class String(Constant):
    __slots__ = ('string_index',)
    TAG = 8

    def __init__(self, pool, index, string_index):
        super().__init__(pool, index)
        self.string_index = string_index

    @property
    def string(self):
        return self.pool.get(self.string_index)

    def pack(self):
        return pack('>BH', self.TAG, self.string_index)

    def __repr__(self):
        return f'<String(index={self.index}, string={self.string!r})>'


class Reference(Constant):
    __slots__ = ('class_index', 'name_and_type_index')
    TAG = None

    def __init__(self, pool, index, class_index, name_and_type_index):
        super().__init__(pool, index)
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    @property
    def class_(self):
        return self.pool.get(self.class_index)

    @property
    def name_and_type(self):
        return self.pool.get(self.name_and_type_index)

    def pack(self):
        return pack(
            '>BHH',
            self.TAG,
            self.class_index,
            self.name_and_type_index
        )

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}('
            f'index={self.index},'
            f'class_={self.class_!r},'
            f'name_and_type={self.name_and_type!r})>'
        )


class FieldReference(Reference):
    TAG = 9


class MethodReference(Reference):
    TAG = 10


class InterfaceMethodRef(Reference):
    TAG = 11


class NameAndType(Constant):
    __slots__ = ('name_index', 'descriptor_index')
    TAG = 12

    def __init__(self, pool, index, name_index, descriptor_index):
        super().__init__(pool, index)
        self.name_index = name_index
        self.descriptor_index = descriptor_index

    @property
    def name(self):
        return self.pool.get(self.name_index)

    @property
    def descriptor(self):
        return self.pool.get(self.descriptor_index)

    def pack(self):
        return pack('>BHH', self.TAG, self.name_index, self.descriptor_index)

    def __repr__(self):
        return (
            f'<NameAndType('
            f'index={self.index},'
            f'name={self.name!r},'
            f'descriptor={self.descriptor!r})>'
        )


class MethodHandle(Constant):
    __slots__ = ('reference_kind', 'reference_index')
    TAG = 15

    def __init__(self, pool, index, reference_kind, reference_index):
        super().__init__(pool, index)
        self.reference_kind = reference_kind
        self.reference_index = reference_index

    @property
    def reference(self):
        return self.pool.get(self.reference_index)

    def pack(self):
        return pack('>BBH', self.TAG, self.reference_kind, self.reference_index)

    def __repr__(self):
        return (
            f'<MethodHandle(index={self.index}, reference={self.reference!r})>'
        )


class MethodType(Constant):
    __slots__ = ('descriptor_index',)
    TAG = 16

    def __init__(self, pool, index, descriptor_index):
        super().__init__(pool, index)
        self.descriptor_index = descriptor_index

    @property
    def descriptor(self):
        return self.pool.get(self.descriptor_index)

    def pack(self):
        return pack('>BH', self.TAG, self.descriptor_index)

    def __repr__(self):
        return f'<MethodType(index={self.index},descriptor={self.descriptor})>'


class InvokeDynamic(Constant):
    __slots__ = ('bootstrap_method_attr_index', 'name_and_type_index')
    TAG = 18

    def __init__(self, pool, index, bootstrap_method_attr_index,
                 name_and_type_index):
        super().__init__(pool, index)
        self.bootstrap_method_attr_index = bootstrap_method_attr_index
        self.name_and_type_index = name_and_type_index

    @property
    def method_attr_index(self):
        return self.bootstrap_method_attr_index

    @property
    def name_and_type(self):
        return self.pool[self.name_and_type_index]

    def pack(self):
        return pack(
            '>BHH',
            self.TAG,
            self.bootstrap_method_attr_index,
            self.name_and_type_index
        )

    def __repr__(self):
        return (
            f'<InvokeDynamic('
            f'index={self.index},'
            f'method_attr_index={self.method_attr_index},'
            f'name_and_type={self.name_and_type!r})>'
        )


class Module(ConstantClass):
    __slots__ = ('name_index',)
    TAG = 19

    def __repr__(self):
        return f'<Module(index={self.index}, name={self.name!r})>'


class PackageInfo(ConstantClass):
    __slots__ = ('name_index',)
    TAG = 20

    def __repr__(self):
        return f'<PackageInfo(index={self.index}, name={self.name!r})>'


_constant_types = (
    None,
    UTF8,
    None,
    Integer,
    Float,
    Long,
    Double,
    ConstantClass,
    String,
    FieldReference,
    MethodReference,
    InterfaceMethodRef,
    NameAndType,
    None,
    None,
    MethodHandle,
    MethodType,
    None,
    InvokeDynamic,
    Module,
    PackageInfo
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
        without any arguments is equivalent to iterating over the pool.

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
        self.append((1, value))
        return self.get(self.raw_count - 1)

    def create_integer(self, value: int) -> Integer:
        """
        Creates a new :class:`ConstantInteger`, adding it to the pool and
        returning it.

        :param value: The value of the new integer.
        """
        self.append((3, value))
        return self.get(self.raw_count - 1)

    def create_float(self, value: float) -> Float:
        """
        Creates a new :class:`ConstantFloat`, adding it to the pool and
        returning it.

        :param value: The value of the new float.
        """
        self.append((4, value))
        return self.get(self.raw_count - 1)

    def create_long(self, value: int) -> Long:
        """
        Creates a new :class:`ConstantLong`, adding it to the pool and
        returning it.

        :param value: The value of the new long.
        """
        self.append((5, value))
        self.append(None)
        return self.get(self.raw_count - 2)

    def create_double(self, value: float) -> Double:
        """
        Creates a new :class:`ConstantDouble`, adding it to the pool and
        returning it.

        :param value: The value of the new Double.
        """
        self.append((6, value))
        self.append(None)
        return self.get(self.raw_count - 2)

    def create_class(self, name: str) -> ConstantClass:
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

    def create_string(self, value: str) -> String:
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

    def create_name_and_type(self, name: str, descriptor: str) -> NameAndType:
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

    def create_field_ref(self, class_: str, field: str, descriptor: str) \
            -> FieldReference:
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

    def create_method_ref(self, class_: str, method: str, descriptor: str) \
            -> MethodReference:
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

    def create_interface_method_ref(self, class_: str, if_method: str,
                                    descriptor: str) -> InterfaceMethodRef:
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
            tag = ord(read(1))

            if tag == 1:
                # CONSTANT_Utf8_info, a length prefixed UTF-8-ish string.
                # Only attempt to properly decode the MUTF8 if it fails
                # regular UTF8 decoding, which overs huge time savings over
                # large JARs.
                utf8_str = read(unpack('>H', read(2))[0])
                try:
                    utf8_str = utf8_str.decode('utf8')
                except UnicodeDecodeError:
                    utf8_str = decode_modified_utf8(utf8_str)
                self.append((tag, utf8_str))
            else:
                # Every other constant type is trivial.
                fmt, size = _constant_fmts[tag]
                self.append((tag, *unpack(fmt, read(size))))
                if tag == 5 or tag == 6:
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
            write(constant.pack())

    def __len__(self) -> int:
        """
        The number of `Constants` in the `ConstantPool`, excluding padding.
        """
        count = 0
        for constant in self._pool:
            if constant is not None:
                count += 1
        return count

    @property
    def raw_count(self) -> int:
        """
        The number of `Constants` in the `ConstantPool`, including padding.
        """
        return len(self._pool)
