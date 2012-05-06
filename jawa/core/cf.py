try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from struct import unpack


class ConstantType(object):
    """
    Tag values for working with Constants.
    """
    Class = 7
    FieldRef = 9
    MethodRef = 10
    InterfaceMethodref = 11
    String = 8
    Integer = 3
    Float = 4
    Long = 5
    Double = 6
    NameAndType = 12
    Utf8 = 1
    MethodHandle = 15
    MethodType = 16
    InvokeDynamic = 18


class ClassFile(object):
    """
    Creates a new ClassFile, optionally loading the JVM class at `io`, where
    `io` is a file-like object providing `read()` or a file-system path.
    """
    def __init__(self, io=None):
        if io and isinstance(io, basestring):
            fin = open(io, 'rb')
            self._load_from_io(fin)
            fin.close()
        elif io:
            self._load_from_io(io)

    @classmethod
    def from_str(cls, data):
        """
        Returns a new :py:class:`jawa.core.cf.ClassFile` from a string buffer.

        >>> from jawa.util.jf import JarFile
        >>> from jawa.core.cf import ClassFile
        >>> with JarFile(sys.argv[1]) as jf:
        ...    for path in jf.namelist():
        ...        cf = ClassFile.from_str(jf.read(path))
        """
        sio = StringIO(data)
        tmp = cls(io=sio)
        sio.close()
        return tmp

    def _load_from_io(self, io):
        """
        Parses a raw `ClassFile` given a file-like object `io` providing
        a blocking `read()`.
        """
        if unpack('>I', io.read(4))[0] != 0xCAFEBABE:
            raise IOError('Not a ClassFile!')

        minv, maxv, count = unpack('>3H', io.read(6))
        self.version = (maxv, minv)

        # Loads the constant pool.
        constants = []
        i = 1
        while i < count:
            tag = unpack('>B', io.read(1))[0]
            # CONSTANT_Class_info
            if tag == 7:
                constants.append((tag,
                    unpack('>H', io.read(2))
                ))
            # CONSTANT_*ref_info
            # Faster than "in", if uglier.
            elif tag == 9 or tag == 10 or tag == 11:
                constants.append((tag,
                    unpack('>HH', io.read(4))
                ))
            # CONSTANT_String_info
            elif tag == 8:
                constants.append((tag,
                    unpack('>H', io.read(2))
                ))
            # CONSTANT_Integer_info
            elif tag == 3:
                constants.append((tag,
                    unpack('>i', io.read(4))
                ))
            # CONSTANT_Float_info
            elif tag == 4:
                constants.append((tag,
                    unpack('>f', io.read(4))
                ))
            # CONSTANT_Long_info
            elif tag == 5:
                constants.append((tag,
                    unpack('>q', io.read(8))
                ))
            # CONSTANT_Double_info
            elif tag == 6:
                constants.append((tag,
                    unpack('>d', io.read(8))
                ))
            # CONSTANT_NameAndType_info
            elif tag == 12:
                constants.append((tag, unpack('>HH', io.read(4))))
            # CONSTANT_Utf8_info
            elif tag == 1:
                length = unpack('>H', io.read(2))[0]
                constants.append((tag,
                    unpack('>%ss' % length, io.read(length))
                ))
            i += 2 if tag == 5 or tag == 6 else 1
