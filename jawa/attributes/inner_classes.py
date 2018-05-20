import io
from struct import pack
from itertools import repeat
from collections import namedtuple
from jawa.attribute import Attribute


InnerClass = namedtuple('InnerClass', [
    'inner_class_info_index',
    'outer_class_info_index',
    'inner_name_index',
    'inner_class_access_flags'
])


class InnerClassesAttribute(Attribute):
    ADDED_IN = '1.1.0'
    MINIMUM_CLASS_VERSION = (45, 3)

    def __init__(self, table, name_index):
        super().__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'InnerClasses'
            ).index
        )
        self.inner_classes = []

    def unpack(self, info):
        for _ in repeat(None, info.u2()):
            self.inner_classes.append(InnerClass(*info.unpack('>HHHH')))

    def pack(self):
        with io.BytesIO() as out:
            out.write(pack('>H', len(self.inner_classes)))
            for inner_class in self.inner_classes:
                out.write(pack('>HHHH', *inner_class))
            return out.getvalue()
