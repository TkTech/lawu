import inspect
import pkgutil
import importlib
from typing import IO, Callable, Iterator, Union, Dict, Any, Tuple
from struct import unpack, pack
from itertools import repeat

from jawa.constants import UTF8
from jawa.util.stream import BufferStreamReader


class Attribute(object):
    ADDED_IN: int = None
    MINIMUM_CLASS_VERSION: Tuple[int, int] = None

    def __init__(self, parent: 'AttributeTable', name_index: int):
        self.parent = parent
        self.name_index = name_index

    @property
    def name(self) -> UTF8:
        """
        The name of this attribute.
        """
        return self.cf.constants[self.name_index]

    @property
    def cf(self):
        """
        The ClassFile that owns this attribute, if any.
        """
        return self.parent.cf

    def unpack(self, info: Union[bytes, BufferStreamReader]):
        """
        Parses an instance of this attribute from the blob `info`.
        """
        raise NotImplementedError()

    def pack(self) -> bytes:
        """
        This attribute packed into its on-disk representation.
        """
        raise NotImplementedError()


class UnknownAttribute(Attribute):
    def __init__(self, parent: 'AttributeTable', name_index: int):
        super().__init__(parent, name_index)
        self.info = None

    def unpack(self, info: Union[bytes, BufferStreamReader]):
        self.info = info

    def pack(self) -> bytes:
        return self.info


class AttributeTable(object):
    def __init__(self, cf, parent: Attribute=None):
        #: The ClassFile that ultimately owns this AttributeTable.
        self.cf = cf
        #: The parent Attribute, if one exists.
        self.parent = parent
        self._table = []

    def unpack(self, source: IO):
        """
        Read the ConstantPool from the file-like object `source`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param source: Any file-like object providing `read()`
        """
        count = unpack('>H', source.read(2))[0]
        for _ in repeat(None, count):
            name_index, length = unpack('>HI', source.read(6))
            info_blob = source.read(length)
            self._table.append((name_index, info_blob))

    def __getitem__(self, key):
        attr = self._table[key]

        if not isinstance(attr, Attribute):
            name_index, info = attr[0], attr[1]
            name = self.cf.constants[name_index].value

            attribute_type = ATTRIBUTE_CLASSES.get(name, UnknownAttribute)
            self._table[key] = attr = attribute_type(self, name_index)
            if attribute_type is UnknownAttribute:
                attr.unpack(info)
            else:
                attr.unpack(BufferStreamReader(info))

        return attr

    def __len__(self):
        return len(self._table)

    def pack(self, out: IO):
        """
        Write the AttributeTable to the file-like object `out`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when saving a ClassFile.

        :param out: Any file-like object providing `write()`
        """
        out.write(pack('>H', len(self._table)))
        for attribute in self:
            info = attribute.pack()
            out.write(pack(
                '>HI',
                attribute.name.index,
                len(info)
            ))
            out.write(info)

    def create(self, type_, *args, **kwargs) -> Any:
        """
        Creates a new attribute of `type_`, appending it to the attribute
        table and returning it.
        """
        attribute = type_(self, *args, **kwargs)
        self._table.append(attribute)
        return attribute

    def find(self, *, name: str=None, f: Callable=None) -> Iterator[Any]:
        for idx, attribute in enumerate(self._table):
            if name is not None:
                # Optimization to filter solely on name without causing
                # a full attribute load.
                if not isinstance(attribute, Attribute) and f is None:
                    attr_name = self.cf.constants[attribute[0]].value
                    if attr_name != name:
                        continue
                elif name != attribute.name.value:
                    continue

            # Force an attribute load.
            if not isinstance(attribute, Attribute):
                attribute = self[idx]

            if f is not None and not f(attribute):
                continue

            yield attribute

    def find_one(self, **kwargs) -> Any:
        """
        Same as ``find()`` but returns only the first result.
        """
        return next(self.find(**kwargs), None)


def get_attribute_classes() -> Dict[str, Attribute]:
    """
    Lookup all builtin Attribute subclasses, load them, and return a dict
    """
    attribute_children = pkgutil.iter_modules(
        importlib.import_module('jawa.attributes').__path__,
        prefix='jawa.attributes.'
    )

    result = {}
    for _, name, _ in attribute_children:
        classes = inspect.getmembers(
            importlib.import_module(name),
            lambda c: (
                inspect.isclass(c) and issubclass(c, Attribute) and
                c is not Attribute
            )
        )

        for class_name, class_ in classes:
            attribute_name = getattr(class_, 'ATTRIBUTE_NAME', class_name[:-9])
            result[attribute_name] = class_

    return result


#: A dictionary of known attribute subclasses at the time this module
#: was loaded.
ATTRIBUTE_CLASSES = get_attribute_classes()
