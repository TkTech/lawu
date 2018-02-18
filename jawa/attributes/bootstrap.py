# -*- coding: utf-8 -*-
from itertools import repeat
from struct import pack

import six

from jawa.attribute import Attribute


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
        return '<BootstrapMethods()>'

    def pack(self):
        out = six.BytesIO()
        out.write(pack('>H', len(self.table)))
        for table_entry in self.table:
            out.write(pack('>HH', table_entry[0], table_entry[1]))
            out.write(pack('>{0}H'.format(
                len(table_entry[2]),
                table_entry[2]
            )))
        return out.getvalue()

    def unpack(self, info):
        length = info.u2()

        for _ in repeat(None, length):
            bootstrap_method_ref = info.u2()
            num_bootstrap_arguments = info.u2()
            bootstrap_arguments = info.unpack(
                '>{0}H'.format(num_bootstrap_arguments)
            )

            self.table.append((
                bootstrap_method_ref,
                num_bootstrap_arguments,
                bootstrap_arguments
            ))
