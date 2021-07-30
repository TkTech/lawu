from struct import unpack
from typing import BinaryIO, Tuple
from dataclasses import dataclass
from itertools import repeat

from lawu.ast import BootstrapMethods
from lawu.constants import ConstantPool, MethodHandle
from lawu.attribute import Attribute


@dataclass
class BootstrapMethod:
    method_ref: MethodHandle
    args: Tuple[int]
    parent: BootstrapMethods = None


class BootstrapMethodsAttribute(Attribute):
    ADDED_IN = '7.0.0'
    MINIMUM_CLASS_VERSION = (51, 0)

    @classmethod
    def from_binary(cls, pool: ConstantPool, source: BinaryIO) -> BootstrapMethods:
        methods = []
        for _ in repeat(None, unpack('>H', source.read(2))[0]):
            ref, arg_len = unpack('>HH', source.read(4))
            methods.append(BootstrapMethod(
                pool[ref], unpack(f'>{arg_len}H', source.read(arg_len * 2))
            ))

        return BootstrapMethods(children=methods)
