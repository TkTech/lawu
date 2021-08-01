from struct import unpack
from typing import BinaryIO

from lawu.ast import SourceFile
from lawu.constants import ConstantPool
from lawu.attribute import Attribute


class SourceFileAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> SourceFile:
        return SourceFile(value=pool[unpack('>H', source.read(2))[0]])
