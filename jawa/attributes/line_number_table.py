from struct import pack
from collections import namedtuple

from jawa.attribute import Attribute


line_number_entry = namedtuple('line_number_entry', 'start_pc line_number')


class LineNumberTableAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    def __init__(self, table, name_index=None):
        super(LineNumberTableAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'LineNumberTable'
            ).index
        )
        self.line_no = []

    def unpack(self, info):
        length = info.u2()
        table = info.unpack('>{0}H'.format(length * 2))

        self.line_no = [
            line_number_entry(*x)
            for x in zip(*[iter(table)] * 2)
        ]

    def pack(self):
        return pack(
            '>H{0}H'.format(len(self.line_no) * 2),
            len(self.line_no),
            *sum(self.line_no, ())
        )

    def __repr__(self):
        return '<LineNumberTableAttribute({0!r})>'.format(self.line_no)
