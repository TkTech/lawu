from struct import unpack
from typing import BinaryIO
from itertools import repeat
from dataclasses import dataclass

from lawu.ast import LocalVariableTable
from lawu.constants import ConstantPool, UTF8
from lawu.attribute import Attribute


@dataclass
class LocalVariableEntry:
    start_pc: int
    length: int
    name: UTF8
    descriptor: UTF8
    index: int
    parent: LocalVariableTable = None


class LocalVariableTableAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> LocalVariableTable:
        local_variables = []
        for _ in repeat(None, unpack('>H', source.read(2))[0]):
            pc, length, name, desc, idx = unpack('>HHHHH', source.read(10))
            local_variables.append(LocalVariableEntry(
                pc, length, pool[name], pool[desc], idx
            ))
        return LocalVariableTable(children=local_variables)
