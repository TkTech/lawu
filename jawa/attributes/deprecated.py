from jawa.attribute import Attribute


class DeprecatedAttribute(Attribute):
    ADDED_IN = '1.1.0'
    MINIMUM_CLASS_VERSION = (45, 3)

    def __init__(self, table, name_index=None):
        super(DeprecatedAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'Deprecated'
            ).index
        )

    def __repr__(self):
        return '<DeprecatedAttribute()>'

    def pack(self):
        pass

    def unpack(self, info):
        pass
