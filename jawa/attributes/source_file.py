# -*- coding: utf8 -*-
from struct import unpack_from, pack
from jawa.attribute import Attribute


class SourceFileAttribute(Attribute):
    def unpack(self, info):
        self._sourcefile_index = unpack_from('>H', info)[0]

    @property
    def info(self):
        return pack('>H', self._sourcefile_index)

    @property
    def sourcefile(self):
        return self._cf.constants[self._sourcefile_index]
