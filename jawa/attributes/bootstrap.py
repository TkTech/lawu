import io
from collections import namedtuple
from itertools import repeat
from struct import pack

from jawa.attribute import Attribute

BootstrapMethod = namedtuple(
    'BootstrapMethod',
    ['method_ref', 'bootstrap_args']
)


class BootstrapMethodsAttribute(Attribute):
    ADDED_IN = '7'
    MINIMUM_CLASS_VERSION = (51, 0)

    def __init__(self, table, name_index=None):
        super(BootstrapMethodsAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'BootstrapMethods'
            ).index
        )
        self.table = []

    def __repr__(self):
        return '<BootstrapMethods(table={self.table})>'.format(
            self=self
        )

    def pack(self):
        out = io.BytesIO()
        out.write(pack('>H', len(self.table)))

        for table_entry in self.table:
            out.write(pack(
                '>HH',
                table_entry.method_ref,
                len(table_entry.bootstrap_args)
            ))
            out.write(pack(
                '>{0}H'.format(len(table_entry.bootstrap_args)),
                table_entry.bootstrap_args
            ))

        return out.getvalue()

    def unpack(self, info):
        length = info.u2()

        for _ in repeat(None, length):
            self.table.append(BootstrapMethod(
                info.u2(),
                info.unpack('>{0}H'.format(info.u2()))
            ))
