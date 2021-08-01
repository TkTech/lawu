from struct import unpack
from typing import BinaryIO

from lawu.ast import EnclosingMethod
from lawu.constants import ConstantPool
from lawu.attribute import Attribute


class EnclosingMethodAttribute(Attribute):
    ADDED_IN = '5.0.0'
    MINIMUM_CLASS_VERSION = (49, 0)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> EnclosingMethod:
        class_ = pool[unpack('>H', source.read(2))[0]]
        nt = pool[idx] if (idx := unpack('>H', source.read(2))[0]) else None
        return EnclosingMethod(enclosing_class=class_, name_and_type=nt)
