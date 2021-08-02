from struct import unpack
from typing import BinaryIO
from dataclasses import dataclass

from lawu.ast import LocalVariableTypeTable
from lawu.constants import ConstantPool, UTF8
from lawu.attribute import Attribute


@dataclass
class LocalVariableTypeEntry:
    start_pc: int
    length: int
    name: UTF8
    signature: UTF8
    index: int


class LocalVariableTypeTableAttribute(Attribute):
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> LocalVariableTypeTable:
        entries = []
        num_entries = unpack('>H', source.read(2))[0]
        data = unpack(f'>{num_entries * 5}H', source.read(num_entries * 10))
        for i in range(0, num_entries * 5, 5):
            pc, length, name, sig, idx = data[i:i+5]
            entries.append(LocalVariableTypeEntry(
                pc, length, pool[name], pool[sig], idx
            ))
        return LocalVariableTypeTable(entries=entries)
