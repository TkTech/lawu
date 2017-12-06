# -*- coding: utf8 -*-
from struct import pack
from jawa.attribute import Attribute, lazy_attribute_property


class SourceFileAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    def __init__(self, table, sourcefile=None, name_index=None):
        super(SourceFileAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'SourceFile'
            ).index
        )
        self._sourcefile_index = sourcefile.index if sourcefile else None

    def unpack(self, info):
        self._sourcefile_index = info.u2()

    @property
    def info(self):
        return pack('>H', self._sourcefile_index)

    @property
    @lazy_attribute_property
    def sourcefile(self):
        return self._cf.constants[self._sourcefile_index]
