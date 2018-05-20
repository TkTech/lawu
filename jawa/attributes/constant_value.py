from struct import pack
from jawa.attribute import Attribute


class ConstantValueAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    def __init__(self, table, value=None, name_index=None):
        super(ConstantValueAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'ConstantValue'
            ).index
        )
        self._constant_value_index = value.index if value else None

    def unpack(self, info):
        self._constant_value_index = info.u2()

    def pack(self):
        return pack('>H', self._constant_value_index)

    @property
    def constant_value(self):
        return self.cf.constants[self._constant_value_index]
