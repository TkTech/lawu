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

        count = unpack('>H', source.read(2))[0]
        entries = iter(unpack(f'>{count * 2}H', source.read(count * 4)))

        return LineNumberTable(entries=dict(zip(entries, entries)))
