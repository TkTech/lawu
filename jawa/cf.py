# -*- coding: utf8 -*-
"""
ClassFile support.

The :mod:`jawa.cf` module provides tools for working with JVM ``.class``
ClassFiles.
"""
from struct import pack, unpack
from collections import namedtuple


from jawa.constants import ConstantPool
from jawa.fields import FieldTable
from jawa.methods import MethodTable
from jawa.attribute import AttributeTable
from jawa.util.flags import Flags


class ClassVersion(namedtuple('ClassVersion', ['major', 'minor'])):
    """ClassFile file format version."""

    __slots__ = ()

    @property
    def human(self):
        """
        A human-readable string identifying this version.

        If the version is unknown, `None` is returned instead.
        """
        return {
            0x33: 'J2SE_7',
            0x32: 'J2SE_6',
            0x31: 'J2SE_5',
            0x30: 'JDK1_4',
            0x2F: 'JDK1_3',
            0x2E: 'JDK1_2',
            0x2D: 'JDK1_1',
        }.get(self.major, None)


class ClassFile(object):
    """
    Implements the JVM ClassFile (files typically ending in ``.class``).

    To open an existing ClassFile::

        from jawa import ClassFile
        with open('HelloWorld.class', 'rb') as fin:
            cf = ClassFile(fin)

    To save a newly created or modified ClassFile::

        with open('HelloWorld.class', 'wb') as fout:
            cf.save(fout)

    To create a new ClassFile, use the helper :meth:`~ClassFile.create`::

        from jawa import ClassFile
        cf = ClassFile.create('HelloWorld')
        with open('HelloWorld.class', 'wb') as fout:
            cf.save(fout)

    :meth:`~ClassFile.create` sets up some reasonable defaults equivelent to:

    .. code-block:: java

        public class HelloWorld extends java.lang.Object{
        }

    :param fio: any file-like object providing ``.read()``.
    """

    #: The JVM ClassFile magic number.
    MAGIC = 0xCAFEBABE

    def __init__(self, fio=None):
        # Default to J2SE_7
        self._version = ClassVersion(0x32, 0)
        self._constants = ConstantPool()
        self._access_flags = Flags('>H', {
            'acc_public': 0x0001,
            'acc_final': 0x0010,
            'acc_super': 0x0020,
            'acc_interface': 0x0200,
            'acc_abstract': 0x0400,
            'acc_synthetic': 0x1000,
            'acc_annotation': 0x2000,
            'acc_enum': 0x4000
        })
        self._this = 0
        self._super = 0
        self._interfaces = []
        self._fields = FieldTable(self)
        self._methods = MethodTable(self)
        self._attributes = AttributeTable(self)

        if fio:
            self._from_io(fio)

    @classmethod
    def create(cls, this, super_='java/lang/Object'):
        """
        A utility which sets up reasonable defaults for a new public class.

        :param this: The name of this class.
        :param super_: The name of this class's superclass.
        """
        cf = ClassFile()
        cf.access_flags.acc_public = True
        cf.access_flags.acc_super = True

        cf.this = cf.constants.create_class(this)
        cf.super_ = cf.constants.create_class(super_)

        return cf

    def save(self, fout):
        """
        Saves the class to the file-like object `fout`.
        """
        write = fout.write

        write(pack(
            '>IHH',
            ClassFile.MAGIC,
            self.version.minor,
            self.version.major
        ))

        self._constants.pack(fout)

        write(self.access_flags.pack())
        write(pack(
            '>HHH{0}H'.format(len(self._interfaces)),
            self._this,
            self._super,
            len(self._interfaces),
            *self._interfaces
        ))

        self._fields.pack(fout)
        self._methods.pack(fout)
        self._attributes.pack(fout)

    def _from_io(self, fio):
        """
        Loads an existing JVM ClassFile from any file-like object.
        """
        read = fio.read

        if unpack('>I', fio.read(4))[0] != ClassFile.MAGIC:
            raise ValueError('invalid magic number')

        # The version is swapped on disk to (minor, major), so swap it back.
        self.version = unpack('>HH', fio.read(4))[::-1]

        self._constants.unpack(fio)

        # ClassFile access_flags, see section #4.1 of the JVM specs.
        self.access_flags.unpack(read(2))

        # The CONSTANT_Class indexes for "this" class and its superclass.
        # Interfaces are a simple list of CONSTANT_Class indexes.
        self._this, self._super, interfaces_count = unpack('>HHH', read(6))
        self._interfaces = unpack(
            '>{0}H'.format(interfaces_count),
            read(2 * interfaces_count)
        )

        self._fields.unpack(fio)
        self._methods.unpack(fio)
        self._attributes.unpack(fio)

    @property
    def version(self):
        """
        The :class:`~jawa.cf.ClassVersion` for this class.

        Example::

            >>> cf = ClassFile.create('HelloWorld')
            >>> cf.version = 51, 0
            >>> print(cf.version)
            ClassVersion(major=51, minor=0)
            >>> print(cf.version.major)
            51
        """
        return self._version

    @version.setter
    def version(self, (major, minor)):
        self._version = ClassVersion(major, minor)

    @property
    def constants(self):
        """
        The :class:`~jawa.cp.ConstantPool` for this class.
        """
        return self._constants

    @property
    def access_flags(self):
        return self._access_flags

    @property
    def this(self):
        """
        The :class:`~jawa.constants.ConstantClass` which represents this class.
        """
        return self.constants.get(self._this)

    @this.setter
    def this(self, value):
        self._this = value.index

    @property
    def super_(self):
        """
        The :class:`~jawa.constants.ConstantClass` which represents this
        class's superclass.
        """
        return self.constants.get(self._super)

    @super_.setter
    def super_(self, value):
        self._super = value.index

    @property
    def interfaces(self):
        """
        A list of direct superinterfaces of this class as indexes into
        the constant pool, in left-to-right order.
        """
        return self._interfaces

    @property
    def fields(self):
        """
        The :class:`~jawa.fields.FieldTable` for this class.
        """
        return self._fields

    @property
    def methods(self):
        """
        The :class:`~jawa.methods.MethodTable` for this class.
        """
        return self._methods

    @property
    def attributes(self):
        """
        The :class:`~jawa.attribute.AttributeTable` for this class.
        """
        return self._attributes
