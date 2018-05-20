from jawa.attribute import Attribute


class SyntheticAttribute(Attribute):
    ADDED_IN = '5.0.0'
    MINIMUM_CLASS_VERSION = (49, 0)

    def __init__(self, table, name_index=None):
        super().__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'Synthetic'
            ).index
        )

    def pack(self):
        pass

    def unpack(self, info):
        pass
