from struct import pack

from lawu.attribute import Attribute
from lawu.constants import UTF8


class SourceFileAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    def __init__(self, table, name_index=None):
        super(SourceFileAttribute, self).__init__(
            table,
            name_index or UTF8(
                pool=table.cf.constants,
                value='SourceFile'
            ).index
        )
        self.source_file_index = None

    def unpack(self, info):
        self.source_file_index = info.u2()

    def pack(self):
        return pack('>H', self.source_file_index)

    @property
    def source_file(self):
        return self.cf.constants[self.source_file_index]

    @source_file.setter
    def source_file(self, value):
        self.source_file_index = value.index
