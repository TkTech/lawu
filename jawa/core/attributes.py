# -*- coding: utf8 -*-
from struct import unpack
from itertools import repeat


class AttributeTable(object):
    def __init__(self, class_file, attrib_map=None):
        self._table = []
        self._cf = class_file
        self._map = attrib_map or _DEFAULT_ATTRIBUTES

    @property
    def class_file(self):
        """
        Returns the :py:class:`jawa.core.cf.ClassFile` associated with
        this ``AttributeTable``.
        """
        return self._cf

    def _load_from_io(self, io):
        """
        Load an AttributeTable from a ClassFile. It should never be called
        manually.
        """
        read = io.read
        append = self._table.append
        cf = self._cf
        map_ = self._map

        count = unpack('>H', read(2))[0]
        for _ in repeat(None, count):
            name_i, attr_length = unpack('>HI', read(6))
            name = cf.constants.get(name_i)
            append(map_.get(name, UnknownAttribute)._load_from_io(
                cf,
                name_i,
                attr_length,
                io
            ))

    def find(self, name=None, f=None):
        for attrib in self._table:
            if name and attrib.name != name:
                continue

            if f and not f(attrib):
                continue

            yield attrib

    def find_one(self, *args, **kwargs):
        """
        Same as ``find()`` but returns only the first result, or `None` if
        nothing was found.
        """
        try:
            return next(self.find(*args, **kwargs))
        except StopIteration:
            return None


from jawa.core.attribs.unknown import UnknownAttribute
from jawa.core.attribs.sourcefile import SourceFileAttribute
from jawa.core.attribs.code import CodeAttribute

_DEFAULT_ATTRIBUTES = {
    'Code': CodeAttribute,
    'SourceFile': SourceFileAttribute
}
