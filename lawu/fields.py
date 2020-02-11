from typing import IO, Callable, Iterator, Optional
from struct import unpack, pack
from itertools import repeat

from lawu.util.flags import Flags
from lawu.attribute import AttributeTable
from lawu.constants import Constant, UTF8
from lawu.attributes.constant_value import ConstantValueAttribute
from lawu.util.descriptor import field_descriptor


class Field(object):
    def __init__(self, cf):
        self._cf = cf
        self.access_flags = Flags('>H', {
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
        self.attributes = AttributeTable(cf)

    @property
    def descriptor(self) -> UTF8:
        """
        The UTF8 Constant containing the field's descriptor.
        """
        return self._cf.constants[self._descriptor_index]

    @property
    def type(self):
        """
        A :class:`~lawu.util.descriptor.JVMType` representing the field's
        type.
        """
        return field_descriptor(self.descriptor.value)

    @property
    def name(self) -> UTF8:
        """
        The UTF8 Constant containing the field's name.
        """
        return self._cf.constants[self._name_index]

    @property
    def value(self) -> ConstantValueAttribute:
        """
        A shortcut for the field's ConstantValue attribute, should one exist.
        """
        return self.attributes.find_one(name='ConstantValue')

    def unpack(self, source: IO):
        """
        Read the Field from the file-like object `fio`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param source: Any file-like object providing `read()`
        """
        self.access_flags.unpack(source.read(2))
        self._name_index, self._descriptor_index = unpack('>HH', source.read(4))
        self.attributes.unpack(source)

    def pack(self, out: IO):
        """
        Write the Field to the file-like object `out`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when saving a ClassFile.

        :param out: Any file-like object providing `write()`
        """
        out.write(self.access_flags.pack())
        out.write(pack('>HH', self._name_index, self._descriptor_index))
        self.attributes.pack(out)


class FieldTable(object):
    def __init__(self, cf):
        self._cf = cf
        self._table = []

    def append(self, field: Field):
        self._table.append(field)

    def find_and_remove(self, f: Callable):
        """
        Removes any and all fields for which `f(field)` returns `True`.
        """
        self._table = [fld for fld in self._table if not f(fld)]

    def remove(self, field: Field):
        """
        Removes a `Field` from the table by identity.
        """
        self._table = [fld for fld in self._table if fld is not field]

    def create(self, name: str, descriptor: str, *,
               value: Constant=None) -> Field:
        """
        Creates a new field from `name` and `descriptor`. For example::

            >>> from lawu.cf import ClassFile
            >>> cf = ClassFile.create('BeerCounter')
            >>> field = cf.fields.create('BeerCount', 'I')

        To automatically create a static field, pass a value::

            >>> from lawu.cf import ClassFile
            >>> from lawu.constants import Integer
            >>> cf = ClassFile.create('BeerCounter')
            >>> field = cf.fields.create(
            ...     'MaxBeer',
            ...     'I',
            ...     value=Integer(pool=cf.constants, value=99)
            ... )

        :param name: Name of the new field.
        :param descriptor: Type descriptor of the new field.
        :param value: Optional static value for the field.
        """
        field = Field(self._cf)

        field._name_index = UTF8(
            pool=self._cf.constants,
            value=name
        ).index
        field._descriptor_index = UTF8(
            pool=self._cf.constants,
            value=descriptor
        ).index

        field.access_flags.acc_public = True

        if value is not None:
            const = field.attributes.create(ConstantValueAttribute)
            const.value = value
            field.access_flags.acc_static = True

        self.append(field)
        return field

    def __iter__(self):
        for field in self._table:
            yield field

    def unpack(self, source: IO):
        """
        Read the FieldTable from the file-like object `source`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param source: Any file-like object providing `read()`
        """
        field_count = unpack('>H', source.read(2))[0]
        for _ in repeat(None, field_count):
            field = Field(self._cf)
            field.unpack(source)
            self.append(field)

    def pack(self, out: IO):
        """
        Write the FieldTable to the file-like object `out`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when saving a ClassFile.

        :param out: Any file-like object providing `write()`
        """
        out.write(pack('>H', len(self)))
        for field in self._table:
            field.pack(out)

    def __len__(self):
        return len(self._table)

    def find(self, *, name: str=None, type_: str=None,
             f: Callable=None) -> Iterator[Field]:
        """
        Iterates over the fields table, yielding each matching method. Calling
        without any arguments is equivalent to iterating over the table.

        :param name: The name of the field(s) to find.
        :param type_: The field descriptor (Ex: 'I')
        :param f: Any callable which takes one argument (the field).
        """
        for field in self._table:
            if name is not None and field.name.value != name:
                continue

            descriptor = field.descriptor.value
            if type_ is not None and type_ != descriptor:
                continue

            if f is not None and not f(field):
                continue

            yield field

    def find_one(self, **kwargs) -> Optional[Field]:
        """
        Same as ``find()`` but returns only the first result.
        """
        return next(self.find(**kwargs), None)
