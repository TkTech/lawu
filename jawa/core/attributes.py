# -*- coding: utf8 -*-
from struct import unpack
from itertools import repeat


class AttributeTable(object):
    def __init__(self, class_file):
        self._table = []
        self._cf = class_file

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

        count = unpack('>H', read(2))[0]
        for _ in repeat(None, count):
            name_i, attr_length = unpack('>HI', read(6))
            data = unpack('>%ss' % attr_length, read(attr_length))[0]
