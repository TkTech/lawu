try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from struct import unpack
import jawa.core.constants as const


class ClassFile(object):
    """
    Creates a new ClassFile, optionally loading the JVM class at `io`, where
    `io` is a file-like object providing `read()` or a file-system path.
    """
    def __init__(self, io=None):
        self.constants = const.ConstantPool()

        if io and isinstance(io, basestring):
            fin = open(io, 'rb')
            self._load_from_io(fin)
            fin.close()
        elif io:
            self._load_from_io(io)
        else:
            # We need to construct a default name and superclass.
            self.set_this("HelloWorld")
            self.set_superclass("java/lang/Object")

    def set_this(self, name):
        """
        A helper to set the name of this ``ClassFile``. It generates the
        required ``Constants*`` and inserts them into the pool.
        """
        pool = self.constants
        klass = const.ConstantClass(pool, pool.insert(name))
        pool.insert(klass)
        self._this = klass

    def set_superclass(self, name):
        """
        A helper to set the superclass of this ``ClassFile``. It generates the
        required ``Constants*`` and inserts them into the pool.
        """
        pool = self.constants
        klass = const.ConstantClass(pool, pool.insert(name))
        pool.insert(klass)
        self._super = klass

    @property
    def this(self):
        """
        Returns the :py:class:`jawa.core.constants.ConstantClass` for this
        ``ClassFile``.
        """
        return self._this

    @this.setter
    def this(self, value):
        if not isinstance(value, const.ConstantClass):
            raise TypeError('this must be a ConstantClass.')
        self._this = value

    @property
    def superclass(self):
        """
        Returns the :py:class:`jawa.core.constants.ConstantClass` for the
        superclass of this ``ClassFile``.
        """
        return self._super

    @superclass.setter
    def superclass(self, value):
        if not isinstance(value, const.ConstantClass):
            raise TypeError('superclass must be a ConstantClass.')
        self._super = value

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

        minv, maxv = unpack('>HH', io.read(4))
        self.version = (maxv, minv)
        self.constants._load_from_io(io)

        flags, this, super_ = unpack('>HHH', io.read(6))
        self.access_flags = flags
        self._this = self.constants[this]
        self._super = self.constants[super_]
