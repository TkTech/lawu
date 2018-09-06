import typing
from struct import unpack, pack

from jawa.util.utf import decode_modified_utf8, encode_modified_utf8


class Constant(object):
    """
    The base class for all ``Constant*`` types.
    """
    __slots__ = ('pool', 'index')
    TAG = None

    def __init__(self, *, pool=None):
        self.pool = None
        self.index = 0

        if pool is not None:
            pool.append(self)

    def pack(self):
        raise NotImplementedError()

    def unpack(self, source: typing.BinaryIO):
        raise NotImplementedError()


class Number(Constant):
    """
    The base class for all numeric constant types.
    """
    __slots__ = ('value',)

    def __init__(self, *, pool=None, value=0):
        super().__init__(pool=pool)
        self.value = value

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'index={self.index}, value={self.value!r})'
        )

    def __eq__(self, other):
        return other == self.value

    def pack(self):
        raise NotImplementedError()

    def unpack(self, source: typing.BinaryIO):
        raise NotImplementedError()


class UTF8(Constant):
    __slots__ = ('value',)
    TAG = 1

    def __init__(self, *, pool=None, value=None):
        super().__init__(pool=pool)
        self.value = value

    def pack(self):
        encoded_value = encode_modified_utf8(self.value)
        return pack('>H', len(encoded_value)) + encoded_value

    def unpack(self, source: typing.BinaryIO):
        self.value = decode_modified_utf8(
            source.read(unpack('>H', source.read(2))[0])
        )

    def __repr__(self):
        return f'<UTF8(index={self.index}, value={self.value!r}>)'


class Integer(Number):
    TAG = 3

    def pack(self):
        return pack('>i', self.value)

    def unpack(self, source: typing.BinaryIO):
        self.value = unpack('>i', source.read(4))[0]


class Float(Number):
    TAG = 4

    def pack(self):
        return pack('>f', self.value)

    def unpack(self, source: typing.BinaryIO):
        self.value = unpack('>f', source.read(4))[0]


class Long(Number):
    TAG = 5

    def pack(self):
        return pack('>q', self.value)

    def unpack(self, source: typing.BinaryIO):
        self.value = unpack('>q', source.read(8))[0]


class Double(Number):
    TAG = 6

    def pack(self):
        return pack('>d', self.value)

    def unpack(self, source: typing.BinaryIO):
        self.value = unpack('>d', source.read(8))[0]


class ConstantClass(Constant):
    __slots__ = ('name_index',)
    TAG = 7

    def __init__(self, *, pool=None, name=None):
        super().__init__(pool=pool)
        self.name_index = 0
        if name is not None:
            self.name = name

    @property
    def name(self):
        return self.pool[self.name_index]

    @name.setter
    def name(self, value: typing.Union[str, UTF8]):
        if isinstance(value, UTF8):
            self.pool.append(value)
            self.name_index = value.index
        else:
            utf8 = UTF8(pool=self.pool)
            utf8.value = value
            self.name_index = utf8.index

    def pack(self):
        return pack('>H', self.name_index)

    def unpack(self, source: typing.BinaryIO):
        self.name_index = unpack('>H', source.read(2))[0]

    def __repr__(self):
        return f'<ConstantClass(index={self.index}, name={self.name!r})>'


class String(Constant):
    __slots__ = ('string_index',)
    TAG = 8

    def __init__(self, *, pool=None):
        super().__init__(pool=pool)
        self.string_index = 0

    @property
    def string(self):
        return self.pool[self.string_index]

    def pack(self):
        return pack('>H', self.string_index)

    def unpack(self, source: typing.BinaryIO):
        return unpack('>H', source.read(2))[0]

    def __repr__(self):
        return f'<String(index={self.index}, string={self.string!r})>'


class Reference(Constant):
    __slots__ = ('class_index', 'name_and_type_index')
    TAG = None

    def __init__(self, *, pool=None):
        super().__init__(pool=pool)
        self.class_index = 0
        self.name_and_type_index = 0

    @property
    def class_(self):
        return self.pool[self.class_index]

    @property
    def name_and_type(self):
        return self.pool[self.name_and_type_index]

    def pack(self):
        return pack('>HH', self.class_index, self.name_and_type_index)

    def unpack(self, source: typing.BinaryIO):
        self.class_index, self.name_and_type_index = unpack(
            '>HH',
            source.read(4)
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

    def __init__(self, *, pool=None):
        super().__init__(pool=pool)
        self.name_index = 0
        self.descriptor_index = 0

    @property
    def name(self):
        return self.pool[self.name_index]

    @property
    def descriptor(self):
        return self.pool[self.descriptor_index]

    def pack(self):
        return pack('>HH', self.name_index, self.descriptor_index)

    def unpack(self, source: typing.BinaryIO):
        self.name_index, self.descriptor_index = unpack(
            '>HH',
            source.read(4)
        )

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

    def __init__(self, *, pool=None):
        super().__init__(pool=pool)
        self.reference_kind = None
        self.reference_index = 0

    @property
    def reference(self):
        return self.pool.get(self.reference_index)

    def pack(self):
        return pack('>BH', self.reference_kind, self.reference_index)

    def unpack(self, source: typing.BinaryIO):
        self.reference_kind, self.reference_index = unpack(
            '>BH',
            source.read(3)
        )

    def __repr__(self):
        return (
            f'<MethodHandle(index={self.index}, reference={self.reference!r})>'
        )


class MethodType(Constant):
    __slots__ = ('descriptor_index',)
    TAG = 16

    def __init__(self, *, pool=None):
        super().__init__(pool=pool)
        self.descriptor_index = 0

    @property
    def descriptor(self):
        return self.pool.get(self.descriptor_index)

    def pack(self):
        return pack('>H', self.descriptor_index)

    def unpack(self, source: typing.BinaryIO):
        self.descriptor_index = unpack('>H', source.read(2))[0]

    def __repr__(self):
        return f'<MethodType(index={self.index},descriptor={self.descriptor})>'


class InvokeDynamic(Constant):
    __slots__ = ('bootstrap_method_attr_index', 'name_and_type_index')
    TAG = 18

    def __init__(self, *, pool=None):
        super().__init__(pool=pool)
        self.bootstrap_method_attr_index = 0
        self.name_and_type_index = 0

    @property
    def method_attr_index(self):
        return self.bootstrap_method_attr_index

    @property
    def name_and_type(self):
        return self.pool[self.name_and_type_index]

    def pack(self):
        return pack(
            '>HH',
            self.bootstrap_method_attr_index,
            self.name_and_type_index
        )

    def unpack(self, source: typing.BinaryIO):
        self.bootstrap_method_attr_index, self.name_and_type_index = unpack(
            '>HH',
            source.read(4)
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


CONSTANTS = {
    1: UTF8,
    3: Integer,
    4: Float,
    5: Long,
    6: Double,
    7: ConstantClass,
    8: String,
    9: FieldReference,
    10: MethodReference,
    11: InterfaceMethodRef,
    12: NameAndType,
    15: MethodHandle,
    16: MethodType,
    18: InvokeDynamic,
    19: Module,
    20: PackageInfo
}


class ConstantPool(object):
    def __init__(self):
        self._pool = {}

    def __iter__(self):
        yield from self._pool.values()

    def __getitem__(self, item: int):
        return self._pool[item]

    def __setitem__(self, key: int, value: Constant):
        value.pool = self
        value.index = key
        self._pool[key] = value

    def append(self, value: Constant):
        if value.pool is not self or value.index == 0:
            self[len(self._pool) + 1] = value

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

    def unpack(self, source):
        """
        Read the ConstantPool from the file-like object `source`.

        :param source: Any file-like object providing `read()`
        """
        constant_pool_count = unpack('>H', source.read(2))[0]
        read = source.read

        index_iter = range(1, constant_pool_count)
        for index in index_iter:
            tag = ord(read(1))
            c = CONSTANTS[tag]()
            c.unpack(source)
            self[index] = c
            if tag == 5 or tag == 6:
                next(index_iter)

    def pack(self, out: typing.BinaryIO):
        """
        Write the ConstantPool to the file-like object `out`.

        :param out: Any file-like object providing `write()`
        """
        write = out.write
        write(pack('>H', len(self) + 1))

        for index, constant in sorted(self._pool.items()):
            write(constant.TAG.to_bytes(1, byteorder='big'))
            write(constant.pack())

    def __len__(self) -> int:
        return sum(
            2 if c.TAG == 5 or c.TAG == 6 else 1
            for c in self._pool.values()
        )
