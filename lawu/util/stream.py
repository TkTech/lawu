from io import BytesIO
from struct import unpack, calcsize


class BufferStreamReader(BytesIO):
    """Stream-like reader over a buffer mimicking the JVM spec types.
    """
    def u1(self):
        return unpack('>B', self.read(1))[0]

    def u2(self):
        return unpack('>H', self.read(2))[0]

    def u4(self):
        return unpack('>I', self.read(4))[0]

    def unpack(self, fmt):
        return unpack(fmt, self.read(calcsize(fmt)))
