from struct import unpack
from typing import BinaryIO

from lawu.ast import Signature
from lawu.constants import ConstantPool
from lawu.attribute import Attribute


class SignatureAttribute(Attribute):
    ADDED_IN = '5.0.0'
    MINIMUM_CLASS_VERSION = (49, 0)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> Signature:
        return Signature(value=pool[unpack('>H', source.read(2))[0]])
