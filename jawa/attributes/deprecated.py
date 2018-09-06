from jawa.attribute import Attribute
from jawa.constants import UTF8


class DeprecatedAttribute(Attribute):
    ADDED_IN = '1.1.0'
    MINIMUM_CLASS_VERSION = (45, 3)

    def __init__(self, table, name_index=None):
        super(DeprecatedAttribute, self).__init__(
            table,
            name_index or UTF8(
                pool=table.cf.constants,
                value='Deprecated'
            )
        )

    def __repr__(self):
        return '<DeprecatedAttribute()>'

    def pack(self):
        return b''

    def unpack(self, info):
        pass
