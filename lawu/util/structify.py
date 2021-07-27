"""
Utilities for parsing and explaining Python's Struct format specification.
"""
import struct
import itertools

from enum import Enum
from dataclasses import dataclass


class SegmentType(Enum):
    PAD_BYTE = 'X'
    CHAR = 'c'
    SIGNED_CHAR = 'b'
    UNSIGNED_CHAR = 'B'
    BOOL = '?'
    SHORT = 'h'
    UNSIGNED_SHORT = 'H'
    INT = 'i'
    UNSIGNED_INT = 'I'
    LONG = 'l'
    UNSIGNED_LONG = 'L'
    LONG_LONG = 'q'
    UNSIGNED_LONG_LONG = 'Q'
    SSIZE_T = 'n'
    SIZE_T = 'N'
    HALF_FLOAT = 'e'
    FLOAT = 'f'
    DOUBLE = 'd'
    STRING = 's'


@dataclass
class Segment:
    of_type: SegmentType
    count: int = 1
    label: str = None
    endianess: str = '@'

    @property
    def size(self):
        return struct.calcsize(f'{self.endianess}{self.of_type.value}')


def structify(fmt, labels=None):
    """Parses a format string used for the Python Struct module, yielding
    Segments.

    :param fmt: A python struct format string.
    :param labels: An iterable of labels to apply to each segment, in order.
    """
    endianess = '@'
    count = ''
    labels = itertools.repeat(None) if labels is None else iter(labels)

    for pos, char in enumerate(fmt):
        if char in ('@', '=', '!', '>', '<'):
            if pos != 0:
                raise ValueError(
                    'Byte order characters are only allowed at the start of'
                    ' a foramt string.'
                )

            endianess = char
        elif char.isdigit():
            count += char
        else:
            if char == 's':
                # As a special case, a string's count is its size rather then
                # a repeat.
                yield Segment(
                    of_type=SegmentType(char),
                    count=int(count) if count else 1,
                    label=next(labels) if labels is not None else None,
                    endianess=endianess
                )
            else:
                label = next(labels) if labels is not None else None

                for _ in range(int(count) if count else 1):
                    yield Segment(
                        of_type=SegmentType(char),
                        label=label,
                        endianess=endianess
                    )

            count = ''
