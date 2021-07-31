from typing import BinaryIO

from lawu.ast import Synthetic
from lawu.constants import ConstantPool
from lawu.attribute import Attribute


class SyntheticAttribute(Attribute):
    ADDED_IN = '5.0.0'
    MINIMUM_CLASS_VERSION = (49, 0)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> Synthetic:
        return Synthetic()
