from typing import BinaryIO

from lawu.ast import Deprecated
from lawu.constants import ConstantPool
from lawu.attribute import Attribute

class DeprecatedAttribute(Attribute):
    ADDED_IN = '1.1.0'
    MINIMUM_CLASS_VERSION = (45, 3)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> Deprecated:
        return Deprecated()
