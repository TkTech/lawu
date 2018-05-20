from struct import pack
from collections import namedtuple

from jawa.attribute import Attribute


local_variable_type_entry = namedtuple('local_variable_type_entry', [
    'start_pc',
    'length',
    'name_index',
    'signature_index',
    'index'
])


class LocalVariableTypeTableAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    def __init__(self, table, name_index=None):
        super().__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'LocalVariableTypeTable'
            ).index
        )
        self.local_variables = []

    def unpack(self, info):
        length = info.u2()
        table = info.unpack('>{0}H'.format(length * 5))

        self.local_variables = [
            local_variable_type_entry(*x)
            for x in zip(*[iter(table)] * 5)
        ]

    def pack(self):
        return pack(
            '>H{0}H'.format(len(self.local_variables) * 5),
            len(self.local_variables),
            *sum(self.local_variables, ())
        )

    def __repr__(self):
        return f'<LocalVariableTypeTableAttribute({self.local_variables!r})>'
