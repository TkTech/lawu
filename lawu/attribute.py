import inspect
import pkgutil
import importlib
from typing import Dict, Tuple


class Attribute(object):
    ADDED_IN: int = None
    MINIMUM_CLASS_VERSION: Tuple[int, int] = None

    @staticmethod
    def from_binary(pool, source, blob):
        """Called when converting a ClassFile into an AST."""
        raise NotImplementedError()


def get_attribute_classes() -> Dict[str, Attribute]:
    """
    Lookup all builtin Attribute subclasses, load them, and return a dict
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
