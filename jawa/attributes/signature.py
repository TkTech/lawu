# -*- coding: utf8 -*-
from struct import pack
from jawa.attribute import Attribute


class SignatureAttribute(Attribute):
    ADDED_IN = '5.0.0'
    MINIMUM_CLASS_VERSION = (49, 0)

    def __init__(self, table, signature=None, name_index=None):
        super(SignatureAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'Signature'
            ).index
        )
        self._signature_index = signature.index if signature else None

    def unpack(self, info):
        self._signature_index = info.u2()

    @property
    def info(self):
        return pack('>H', self._signature_index)

    @property
    def signature(self):
        return self._cf.constants[self._signature_index]
