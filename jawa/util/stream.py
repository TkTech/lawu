# -*- coding: utf-8 -*-
import types
import contextlib
from struct import unpack_from, calcsize, unpack


class StreamWithStack(object):
    def __init__(self):
        self.position_stack = []

    def push_pos(self):
        self.position_stack.append(self.fio.tell())

    def pop_pos(self):
        self.fio.seek(self.position_stack.pop())

    @contextlib.contextmanager
    def jump(self, offset, from_what=0):
        self.push_pos()
        self.fio.seek(offset, from_what)
        yield
        self.pop_pos()


class BufferStreamReader(object):
    """Stream-like reader over a buffer mimicing the JVM spec types.
    """
    def __init__(self, buff, starting_offset=0):
        self.pos = starting_offset
        self.buff = buff

    def u1(self):
        r = unpack_from('B', self.buff, offset=self.pos)
        self.pos += 1
        return r[0]

    def u2(self):
        r = unpack_from('>H', self.buff, offset=self.pos)
        self.pos += 2
        return r[0]

    def u4(self):
        r = unpack_from('>I', self.buff, offset=self.pos)
        self.pos += 4
        return r[0]

    def unpack(self, fmt):
        size = calcsize(fmt)
        r = unpack_from(fmt, self.buff, offset=self.pos)
        self.pos += size
        return r

    def seek(self, pos):
        self.pos = pos

    def read(self, length=None):
        if length is None:
            r = self.buff[self.pos:]
            self.pos = len(self.buff)
            return r

        r = self.buff[self.pos:self.pos+length]
        self.pos += length
        return r


DEX_UNPACK_TEMPLATE = '''\
def {name}(self, what=None):
    return unpack('{endian}{fmt}', self.fio.read({size}))[0]
'''


class DexStreamReader(StreamWithStack):
    """
    A utility for reading IO streams using the same naming convention as the
    official DEX language specs, along with efficiently supporting big & little
    endian parsing.

    Rather than constantly check to see if big endian parsing is flagged we
    check once when created and then generate methods with the appropriate
    parsing in them.
    """
    def __init__(self, fio, little_endian=True):
        super(DexStreamReader, self).__init__()
        self.fio = fio
        self.endian = '<' if little_endian else '>'

        # Since these methods are used so frequently we're doing our
        # best to reduce per-call overhead by compiling little/big
        # endian versions on the fly only once.
        fmts = [
            ('byte', 'b', 1),
            ('ubyte', 'B', 1),
            ('short', 'h', 2),
            ('ushort', 'H', 2),
            ('int', 'i', 4),
            ('uint', 'I', 4),
            ('long', 'q', 8),
            ('ulong', 'Q', 8)
        ]

        for method_name, fmt, size in fmts:
            definition = DEX_UNPACK_TEMPLATE.format(
                name=method_name,
                endian=self.endian,
                fmt=fmt,
                size=size
            )

            namespace = dict(unpack=unpack)
            exec definition in namespace
            setattr(self, method_name, types.MethodType(
                namespace[method_name],
                self
            ))

    def uleb128(self, why=None):
        r = 0
        v = 0

        while True:
            v = self.byte()
            r = (r << 7) | (v & 0x7F)
            if v > 0:
                break

        return r

    def unpack(self, fmt, why=None):
        return unpack(fmt, self.fio.read(calcsize(fmt)))
