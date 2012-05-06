try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from struct import unpack, calcsize


class ClassFile(object):
    def __init__(self, io=None):
        self._load_from_io(io)

    @classmethod
    def from_str(cls, data):
        """
        Utility to return a new ClassFile from a string buffer.
        """
        return
        sio = StringIO(data)
        tmp = cls(sio)
        sio.close()
        return tmp

    def _load_from_io(self, io):
        if unpack('>I', io.read(4))[0] != 0xCAFEBABE:
            raise IOError('Not a ClassFile!')
