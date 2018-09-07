from jawa.attribute import Attribute
from jawa.constants import UTF8


class SyntheticAttribute(Attribute):
    ADDED_IN = '5.0.0'
    MINIMUM_CLASS_VERSION = (49, 0)

    def __init__(self, table, name_index=None):
        super().__init__(
            table,
            name_index or UTF8(
                pool=table.cf.constants,
                value='Synthetic'
            ).index
        )

    def pack(self):
        return b''

    def unpack(self, info):
        pass
