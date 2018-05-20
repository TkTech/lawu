from struct import pack

from jawa.attribute import Attribute


class EnclosingMethodAttribute(Attribute):
    ADDED_IN = '5.0.0'
    MINIMUM_CLASS_VERSION = (49, 0)

    def __init__(self, table, name_index=None):
        super().__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'EnclosingMethod'
            ).index
        )
        self.class_index = None
        self.method_index = None

    def pack(self):
        return pack('>HH', self.class_index, self.method_index)

    def unpack(self, info):
        self.class_index = info.u2()
        self.method_index = info.u2()
