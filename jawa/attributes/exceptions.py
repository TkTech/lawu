from struct import pack

from jawa.attribute import Attribute


class ExceptionsAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    def __init__(self, table, name_index=None):
        super(ExceptionsAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'Exceptions'
            ).index
        )
        self.exceptions = []

    def unpack(self, info):
        length = info.u2()
        self.exceptions = list(info.unpack('>{0}H'.format(length)))

    def pack(self):
        return pack(
            '>H{0}H'.format(
                len(self.exceptions)
            ),
            len(self.exceptions),
            *self.exceptions
        )

    def __repr__(self):
        return '<ExceptionsAttribute({0!r})>'.format(self.exceptions)
