# -*- coding: utf8 -*-
from struct import unpack_from, pack
from jawa.attribute import Attribute


class SourceFileAttribute(Attribute):
    def __init__(self, table, sourcefile=None, name_index=None):
        super(SourceFileAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'SourceFile'
            ).index
        )
        self._sourcefile_index = sourcefile.index if sourcefile else None

    def unpack(self, info):
        self._sourcefile_index = unpack_from('>H', info)[0]

    @property
    def info(self):
        return pack('>H', self._sourcefile_index)

    @property
    def sourcefile(self):
        return self._cf.constants[self._sourcefile_index]
