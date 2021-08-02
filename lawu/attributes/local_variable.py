from struct import unpack
from typing import BinaryIO
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


class LocalVariableTableAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> LocalVariableTable:
        entries = []
        num_entries = unpack('>H', source.read(2))[0]
        data = unpack(f'>{num_entries * 5}H', source.read(num_entries * 10))
        for i in range(0, num_entries * 5, 5):
            pc, length, name, desc, idx = data[i:i+5]
            entries.append(LocalVariableEntry(
                pc, length, pool[name], pool[desc], idx
            ))
        return LocalVariableTable(entries=entries)
