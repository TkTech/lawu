from struct import unpack
from typing import BinaryIO
from itertools import repeat
from dataclasses import dataclass

from lawu.ast import LocalVariableTypeTable, String
from lawu.constants import ConstantPool, UTF8
from lawu.attribute import Attribute


@dataclass
class LocalVariableTypeEntry:
    start_pc: int
    length: int
    name: UTF8
    signature: UTF8
    index: int
    parent: LocalVariableTypeTable = None


class LocalVariableTypeTableAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> LocalVariableTypeTable:
        local_types = []
        for _ in repeat(None, unpack('>H', source.read(2))[0]):
            pc, length, name, desc, idx = unpack('>HHHHH', source.read(10))
            local_types.append(LocalVariableTypeEntry(
                pc, length, pool[name], pool[desc], idx
            ))
        return LocalVariableTypeTable(children=local_types)
