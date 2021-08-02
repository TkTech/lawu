from struct import unpack
from typing import BinaryIO

from lawu.ast import Exceptions
from lawu.constants import ConstantPool
from lawu.attribute import Attribute


class ExceptionsAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> Exceptions:
        l = unpack('>H', source.read(2))[0]
        entries = [pool[i] for i in unpack(f'>{l}H', source.read(l * 2))]
        return Exceptions(entries=entries)
