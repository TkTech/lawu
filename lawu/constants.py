"""
Utilities for working with the ConstantPool found in JVM ClassFiles.
"""
from typing import Dict, Any, Deque, BinaryIO, Union
from collections import deque
from struct import unpack, pack

from lawu import ast
from lawu.util.utf import decode_modified_utf8, encode_modified_utf8


def _missing_elements(L, start, end):
    """Sub-linear solution for finding gaps in a list of integers."""
    # From Lie Ryan, Stackoverflow.
    if end - start <= 1:
        if L[end] - L[start] > 1:
            yield from range(L[start] + 1, L[end])
        return

    index = start + (end - start) // 2

    # is the lower half consecutive?
    consecutive_low = L[index] == L[start] + (index - start)
    if not consecutive_low:
        yield from _missing_elements(L, start, index)

    # is the upper part consecutive?
    consecutive_high = L[index] == L[end] - (end - index)
    if not consecutive_high:
        yield from _missing_elements(L, index, end)


class Constant(object):
    """
    The base class for all ``Constant*`` types.
    """
    __slots__ = ('pool', 'index')

    #: The "tag" or leading byte of a constant that identifies its type.
    TAG: int = None

    def __init__(self, *, pool=None, index=None):
        #: The ConstantPool that owns this constant.
        self.pool = None
        #: The constants index in the pool that owns it.
        self.index = None

        if pool is not None:
            pool.add(self, index=index)

    def pack(self) -> bytes:
        """
        Pack the constant into a binary string, minus the tag.
        """
        raise NotImplementedError()

    def unpack(self, source: BinaryIO):
        """
        Unpack the constant from `source`, minus the tag.
        """
        raise NotImplementedError()

    @property
    def as_ast(self):
        """
        Return an AST node for the constant.
        """
        raise NotImplementedError()


class Number(Constant):
    """
    The base class for all numeric constant types.
    """
    __slots__ = ('value',)

    def __init__(self, *, pool=None, index=None, value=0):
        super().__init__(pool=pool, index=index)
        self.value = value

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'index={self.index}, value={self.value!r})'
        )

    def __eq__(self, other):
        if isinstance(other, Number):
            return other.value == self.value
        return other == self.value

    def pack(self):
        raise NotImplementedError()

    def unpack(self, source: BinaryIO):
        raise NotImplementedError()

    @property
    def as_ast(self):
        return ast.Number(value=self.value)


class UTF8(Constant):
    __slots__ = ('value',)
    TAG = 1

    def __init__(self, *, pool=None, index=None, value=None):
        super().__init__(pool=pool, index=index)
        self.value = value

    def pack(self):
        encoded_value = encode_modified_utf8(self.value)
        return pack('>H', len(encoded_value)) + encoded_value

    def unpack(self, source: BinaryIO):
        self.value = decode_modified_utf8(
            source.read(unpack('>H', source.read(2))[0])
        )

    def __repr__(self):
        return f'<UTF8(index={self.index}, value={self.value!r}>)'

    def __eq__(self, other):
        if isinstance(other, UTF8):
            return other.value == self.value
        return other == self.value

    @property
    def as_ast(self):
        return ast.String(value=self.value)


class Integer(Number):
    TAG = 3

    def pack(self):
        return pack('>i', self.value)

    def unpack(self, source: BinaryIO):
        self.value = unpack('>i', source.read(4))[0]


class Float(Number):
    TAG = 4

    def pack(self):
        return pack('>f', self.value)

    def unpack(self, source: BinaryIO):
        self.value = unpack('>f', source.read(4))[0]


class Long(Number):
    TAG = 5

    def pack(self):
        return pack('>q', self.value)

    def unpack(self, source: BinaryIO):
        self.value = unpack('>q', source.read(8))[0]


class Double(Number):
    TAG = 6

    def pack(self):
        return pack('>d', self.value)

    def unpack(self, source: BinaryIO):
        self.value = unpack('>d', source.read(8))[0]


class ConstantClass(Constant):
    __slots__ = ('name_index',)
    TAG = 7

    def __init__(self, *, pool=None, index=None, name=None):
        super().__init__(pool=pool, index=index)
        self.name_index = 0
        if name is not None:
            self.name = name

    @property
    def name(self):
        return self.pool[self.name_index]

    @name.setter
    def name(self, value: Union[str, UTF8]):
        if isinstance(value, UTF8):
            self.pool.append(value)
            self.name_index = value.index
        else:
            utf8 = UTF8(pool=self.pool)
            utf8.value = value
            self.name_index = utf8.index

    def pack(self):
        return pack('>H', self.name_index)

    def unpack(self, source: BinaryIO):
        self.name_index = unpack('>H', source.read(2))[0]

    def __repr__(self):
        return f'<ConstantClass(index={self.index}, name={self.name!r})>'

    @property
    def as_ast(self):
        return ast.ClassReference(descriptor=self.name)


class String(Constant):
    __slots__ = ('string_index',)
    TAG = 8

    def __init__(self, *, pool=None, index=None):
        super().__init__(pool=pool, index=index)
        self.string_index = None

    @property
    def string(self):
        return self.pool[self.string_index]

    def pack(self):
        return pack('>H', self.string_index)

    def unpack(self, source: BinaryIO):
        self.string_index = unpack('>H', source.read(2))[0]

    def __repr__(self):
        return f'<String(index={self.index}, string={self.string!r})>'

    def __eq__(self, other):
        if isinstance(other, String):
            return other.string.value == self.string.value
        return other == self.string.value

    @property
    def as_ast(self):
        return ast.String(value=self.string.value)


class Reference(Constant):
    __slots__ = ('class_index', 'name_and_type_index')
    TAG = None

    def __init__(self, *, pool=None, index=None):
        super().__init__(pool=pool, index=index)
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

    def unpack(self, source: BinaryIO):
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

    @property
    def as_ast(self):
        return ast.FieldReference(
            class_=self.class_.name.value,
            target=self.name_and_type.name.value,
            is_type=self.name_and_type.descriptor.value
        )


class MethodReference(Reference):
    TAG = 10

    @property
    def as_ast(self):
        return ast.MethodReference(
            class_=self.class_.name.value,
            target=self.name_and_type.name.value,
            is_type=self.name_and_type.descriptor.value
        )


class InterfaceMethodRef(Reference):
    TAG = 11

    @property
    def as_ast(self):
        return ast.InterfaceMethodRef(
            class_=self.class_.name.value,
            target=self.name_and_type.name.value,
            is_type=self.name_and_type.descriptor.value
        )


class NameAndType(Constant):
    __slots__ = ('name_index', 'descriptor_index')
    TAG = 12

    def __init__(self, *, pool=None, index=None):
        super().__init__(pool=pool, index=index)
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

    def unpack(self, source: BinaryIO):
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

    def __init__(self, *, pool=None, index=None):
        super().__init__(pool=pool, index=index)
        self.reference_kind = None
        self.reference_index = 0

    @property
    def reference(self):
        return self.pool.get(self.reference_index)

    def pack(self):
        return pack('>BH', self.reference_kind, self.reference_index)

    def unpack(self, source: BinaryIO):
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

    def __init__(self, *, pool=None, index=None):
        super().__init__(pool=pool, index=index)
        self.descriptor_index = 0

    @property
    def descriptor(self):
        return self.pool.get(self.descriptor_index)

    def pack(self):
        return pack('>H', self.descriptor_index)

    def unpack(self, source: BinaryIO):
        self.descriptor_index = unpack('>H', source.read(2))[0]

    def __repr__(self):
        return f'<MethodType(index={self.index},descriptor={self.descriptor})>'


class Dynamic(Constant):
    __slots__ = ('bootstrap_method_attr_index', 'name_and_type_index')
    TAG = 17

    def __init__(self, *, pool=None, index=None):
        super().__init__(pool=pool, index=index)
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

    def unpack(self, source: BinaryIO):
        self.bootstrap_method_attr_index, self.name_and_type_index = unpack(
            '>HH',
            source.read(4)
        )

    def __repr__(self):
        return (
            f'<Dynamic('
            f'index={self.index},'
            f'method_attr_index={self.method_attr_index},'
            f'name_and_type={self.name_and_type!r})>'
        )


class InvokeDynamic(Dynamic):
    __slots__ = ('bootstrap_method_attr_index', 'name_and_type_index')
    TAG = 18

    def __repr__(self):
        return (
            f'<InvokeDynamic('
            f'index={self.index},'
            f'method_attr_index={self.method_attr_index},'
            f'name_and_type={self.name_and_type!r})>'
        )

    @property
    def as_ast(self):
        return ast.InvokeDynamic(
            bootstrap_index=self.bootstrap_method_attr_index,
            name=self.name_and_type.name.value,
            is_type=self.name_and_type.descriptor.value
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
    17: Dynamic,
    18: InvokeDynamic,
    19: Module,
    20: PackageInfo
}


class ConstantPool(object):
    """
    This class can be used to read, modify, and write the JVM ClassFile
    constant pool with a high-level interface.
    """
    def __init__(self, *, source: BinaryIO = None):
        # We use a dict as our basic pool container because the pool can be
        # built out-of-order. For example when loading a Jasmin file, it's
        # possible to explicitly set the position of constants in the pool,
        # even if earlier elements don't exist yet. In general pool operations
        # are not thread-safe.

        #: The internal constant pool. It's not recommended to use this
        #: directly.
        self.pool: Dict[int, Any] = {}
        #: A list of free indexes in the constant pool where gaps occur.
        self.sparse_map: Deque[int] = deque()

        if source is not None:
            self.unpack(source)

    def unpack(self, source: BinaryIO):
        """Unpack a constant pool from a ClassFile."""
        read = source.read
        constant_pool_count = unpack('>H', read(2))[0]

        index_iter = range(1, constant_pool_count)
        for index in index_iter:
            tag = ord(read(1))
            c = CONSTANTS[tag]()
            c.unpack(source)
            c.index = index
            c.pool = self
            self.pool[index] = c
            if tag == 5 or tag == 6:
                self.pool[index + 1] = None
                next(index_iter)

    def pack(self, out: BinaryIO):
        """Write the ConstantPool to the file-like object `out`."""
        write = out.write
        write(pack('>H', len(self)))

        for index, constant in sorted(self._pool.items()):
            # Skip over double-width padding (Doubles & Longs)
            if constant is None:
                continue
            write(constant.TAG.to_bytes(1, byteorder='big'))
            write(constant.pack())

    def update_trackers(self):
        """Update the internal tracking lists and counters to update free
        indexes.

        .. note::

            This is a fairly expensive operation, you should avoid calling it
            except when necessary. If you are not updating the pool manually
            you should never need to use this method.
        """
        if not self.pool:
            self.sparse_map = deque()
            return

        self.sparse_map = deque(
            _missing_elements(
                sorted(self.pool.keys()),
                0,
                len(self.pool) - 1
            )
        )

    @property
    def highest_unused_index(self) -> int:
        return max(self.pool.keys(), default=0) + 1

    def add(self, constant, index: int = None) -> int:
        """Add a new entry to the constant pool.

        If no index is provided, this method will first attempt to fill in any
        gaps in the constant pool. If no room is found, it'll instead apped to
        the end of the pool.

        :param constant: The constant to be added to the pool.
        :param index: Optionally, an explicit index to use for the
                      new constant. [default: None]
        :returns: The index used for the constant.
        """
        if index is None and self.sparse_map:
            # No explicit spot in the pool was requested, so lets try to find
            # room for it.
            desired_index = self.sparse_map.popleft()
            if constant.TAG in (5, 6):
                # ... however, we want to add a LONG or DOUBLE, so we
                # really need two adjacent slots.
                if desired_index + 1 not in self.pool:
                    index = desired_index
                    # Make sure it's removed from the sparse map if the
                    # neighbouring index happened to also be free.
                    try:
                        self.sparse_map.remove(desired_index + 1)
                    except ValueError:
                        pass
                else:
                    # We can't use this slot, add it back to the sparse map
                    # so it can be reused.
                    self.sparse_map.appendleft(desired_index)
            else:
                # Single-slot constant, we can put it anywhere.
                index = desired_index

        # Still no usable index, append it to the pool instead.
        if index is None:
            index = self.highest_unused_index

        self.pool[index] = constant
        constant.index = index
        constant.pool = self
        if constant.TAG in (5, 6):
            self.pool[index + 1] = None

        return index

    def remove(self, index: int):
        """Remove the constant at `index` from the pool.

        ..note::

            If the constant being removed at `index` is a LONG or DOUBLE, the
            adjacent padding constant will also be removed.

        :param index: Index in the pool to be removed.
        """
        const = self.pool.pop(index)
        if const.TAG in (5, 6):
            # If this was a double-width LONG or DOUBLE cleanup the adjacent
            # padding.
            del self.pool[index + 1]
        self.update_trackers()

    def __iter__(self):
        yield from (
            (k, v) for k, v in sorted(self.pool.items())
            if v is not None
        )

    def __getitem__(self, index):
        return self.pool[index]

    def __len__(self):
        return sum(1 for v in self.pool.values() if v is not None)

    def find(self, type_=None, f=None):
        """
        Iterates over the pool, yielding each matching ``Constant``. Calling
        without any arguments is equivalent to iterating over the pool.

        :param type_: Any subclass of :class:`Constant` or ``None``.
        :param f: Any callable which takes one argument (the constant).
        """
        for index, constant in self:
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
