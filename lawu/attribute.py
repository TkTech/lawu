import io
import inspect
import pkgutil
import importlib
import functools
from itertools import repeat
from typing import Dict, Tuple, BinaryIO, Iterable
from struct import unpack

from lawu import ast


class Attribute(object):
    ADDED_IN: int = None
    MINIMUM_CLASS_VERSION: Tuple[int, int] = None

    @staticmethod
    def from_binary(pool, source):
        """Called when converting a ClassFile into an AST."""
        raise NotImplementedError()


@functools.lru_cache()
def get_attribute_classes() -> Dict[str, Attribute]:
    """
    Lookup all builtin Attribute subclasses, load them, and return a dict of
    attribute name -> class.
    """
    attribute_children = pkgutil.iter_modules(
        importlib.import_module('lawu.attributes').__path__,
        prefix='lawu.attributes.'
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
            result[attribute_name.lower()] = class_

    return result


def read_attribute_table(pool, source: BinaryIO) -> Iterable[Attribute]:
    attributes = get_attribute_classes()

    size = unpack('>H', source.read(2))[0]
    for _ in repeat(None, size):
        name_idx, length = unpack('>HI', source.read(6))
        name = pool[name_idx].value

        attr_parser = attributes.get(name.lower())
        with io.BytesIO(source.read(length)) as blob:
            if attr_parser:
                yield attr_parser.from_binary(pool, blob)
            else:
                yield ast.UnknownAttribute(name=name, payload=blob.getvalue())
