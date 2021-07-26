from struct import unpack
from typing import BinaryIO

from lawu import ast
from lawu.attribute import Attribute


class SignatureAttribute(Attribute):
    ADDED_IN = '5.0.0'
    MINIMUM_CLASS_VERSION = (49, 0)

    @classmethod
    def from_binary(cls, pool, source: BinaryIO) -> ast.Signature:
        index = unpack('>H', source.read(2))[0]
        return ast.Signature(signature=pool[index])
