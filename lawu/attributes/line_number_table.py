from struct import unpack
from typing import BinaryIO
from itertools import repeat

from lawu.ast import LineNumberTable
from lawu.constants import ConstantPool
from lawu.attribute import Attribute


class LineNumberTableAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) \
            -> LineNumberTable:
        return LineNumberTable(entries=[
            LineNumberTable.LineNumberEntry(*unpack('>HH', source.read(4)))
            for _ in repeat(None, unpack('>H', source.read(2))[0])
        ])
