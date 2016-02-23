# -*- coding: utf8 -*-
from struct import unpack_from, pack
from jawa.attribute import Attribute


class ConstantValueAttribute(Attribute):
    def __init__(self, table, value=None, name_index=None):
        super(ConstantValueAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'ConstantValue'
            ).index
        )
        self._constantvalue_index = value.index if value else None

    def unpack(self, info):
        self._constantvalue_index = unpack_from('>H', info)[0]

    @property
    def info(self):
        return pack('>H', self._constantvalue_index)

    @property
    def constantvalue(self):
        return self._cf.constants[self._constantvalue_index]
