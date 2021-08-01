from struct import unpack
from typing import BinaryIO

from lawu.ast import ConstantValue
from lawu.constants import ConstantPool
from lawu.attribute import Attribute


class ConstantValueAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> ConstantValue:
        return ConstantValue(value=pool[unpack('>H', source.read(2))[0]])
