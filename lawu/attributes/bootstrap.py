from struct import unpack
from typing import BinaryIO, Tuple
from dataclasses import dataclass
from itertools import repeat

from lawu.ast import BootstrapMethods
from lawu.constants import ConstantPool, MethodHandle
from lawu.attribute import Attribute


@dataclass
class BootstrapMethod:
    reference_kind: MethodHandle.ReferenceKind
    reference_index: int
    args: Tuple[int]


class BootstrapMethodsAttribute(Attribute):
    ADDED_IN = '7.0.0'
    MINIMUM_CLASS_VERSION = (51, 0)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> BootstrapMethods:
        entries = []
        for _ in repeat(None, unpack('>H', source.read(2))[0]):
            ref, arg_len = unpack('>HH', source.read(4))
            handle = pool[ref]
            entries.append(BootstrapMethod(
                handle.reference_kind,
                handle.reference_index,
                unpack(f'>{arg_len}H', source.read(arg_len * 2))
            ))

        return BootstrapMethods(entries=entries)
