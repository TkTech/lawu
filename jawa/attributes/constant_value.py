from struct import pack
from jawa.attribute import Attribute
from jawa.constants import UTF8


class ConstantValueAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    def __init__(self, table, name_index=None):
        super(ConstantValueAttribute, self).__init__(
            table,
            name_index or UTF8(
                pool=table.cf.constants,
                value='ConstantValue'
            ).index
        )
        self._constant_value_index = None

    def unpack(self, info):
        self._constant_value_index = info.u2()

    def pack(self):
        return pack('>H', self._constant_value_index)

    @property
    def value(self):
        return self.cf.constants[self._constant_value_index]

    @value.setter
    def value(self, value):
        self._constant_value_index = value.index

    def __repr__(self):
        return f'<ConstantValue(value={self.value!r})>'
