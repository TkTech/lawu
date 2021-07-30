from dataclasses import dataclass
from struct import unpack
from typing import BinaryIO, Union
from dataclasses import dataclass
from itertools import repeat

from lawu.ast import InnerClasses, IntFlag
from lawu.constants import ConstantPool, ConstantClass, UTF8
from lawu.attribute import Attribute


@dataclass
class InnerClass:
    class AccessFlags(IntFlag):
        PUBLIC     = 0x0001
        PRIVATE    = 0x0002
        PROTECTED  = 0x0004
        STATIC     = 0x0008
        FINAL      = 0x0010
        INTERFACE  = 0x0200
        ABSTRACT   = 0x0400
        SYNTHETIC  = 0x1000
        ANNOTATION = 0x2000
        ENUM       = 0x4000

    inner_class: ConstantClass
    outer_class: Union[ConstantClass, None]
    inner_name: Union[UTF8, None]
    access_flags: AccessFlags
    parent: InnerClasses = None


class InnerClassesAttribute(Attribute):
    ADDED_IN = '1.1.0'
    MINIMUM_CLASS_VERSION = (45, 3)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> InnerClasses:
        inner_classes = []

        for _ in repeat(None, unpack('>H', source.read(2))[0]):
            inner, outer, name, flags = unpack('>HHHH', source.read(8))
            inner_classes.append(InnerClass(
                pool[inner],
                pool[outer] if outer else None,
                pool[name] if name else None,
                InnerClass.AccessFlags(flags)
            ))

        return InnerClasses(children=inner_classes)
