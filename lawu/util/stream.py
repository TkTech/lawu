import io
from struct import unpack, calcsize


class JVMReader(io.BytesIO):
    def u1(self):
        return unpack('B', self.read(1))[0]

    def u2(self):
        return unpack('>H', self.read(2))[0]

    def u4(self):
        return unpack('>I', self.read(4))[0]

    def s4(self):
        return unpack('>i', self.read(4))[0]

    def float(self):
        return unpack('>f', self.read(4))[0]

    def long(self):
        return unpack('>q', self.read(8))[0]

    def unpack(self, fmt):
        return unpack(fmt, self.read(calcsize(fmt)))
