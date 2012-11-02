# -*- coding: utf8 -*-
from struct import unpack_from, pack
from jawa.attribute import Attribute


class ConstantValueAttribute(Attribute):
    @classmethod
    def create(cls, cf, value):
        c = cls(cf, cf.constants.create_utf8('ConstantValue').index)
        c._constantvalue_index = value.index
        return c

    def unpack(self, info):
        self._constantvalue_index = unpack_from('>H', info)[0]

    @property
    def info(self):
        return pack('>H', self._constantvalue_index)

    @property
    def constantvalue(self):
        return self._cf.constants[self._constantvalue_index]
