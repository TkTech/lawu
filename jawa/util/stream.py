from struct import unpack_from, calcsize


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
