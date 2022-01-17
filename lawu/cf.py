"""
ClassFile reader & writer.

The :mod:`lawu.cf` module provides tools for working with JVM ``.class``
ClassFiles.
"""
from typing import BinaryIO, Iterable, Union, Sequence, Optional, List
from struct import pack, unpack
from collections import namedtuple
from enum import IntFlag

from lawu.constants import ConstantPool, ConstantClass, UTF8
from lawu.fields import FieldTable
from lawu.methods import MethodTable
from lawu.attribute import AttributeTable, ATTRIBUTE_CLASSES
from lawu.attributes.bootstrap import BootstrapMethod
from lawu.context import class_context


class ClassVersion(namedtuple('ClassVersion', ['major', 'minor'])):
    """ClassFile file format version."""

    __slots__ = ()

    @property
    def human(self) -> str:
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

        >>> with open('HelloWorld.class', 'rb') as fin:
        ...    cf = ClassFile(fin)

    To save a newly created or modified ClassFile::

        >>> cf = ClassFile()
        >>> with open('HelloWorld.class', 'wb') as out:
        ...    cf.save(out)

    :meth:`~ClassFile()` sets up some reasonable defaults equivalent to:

    .. code-block:: java

        public class HelloWorld extends java.lang.Object{
        }

    :param source: any file-like object providing ``.read()``.
    """

    #: The JVM ClassFile magic number.
    MAGIC = 0xCAFEBABE

    class AccessFlags(IntFlag):
        """
        Possible values for the ClassFile.access_flags field.
        """
        PUBLIC = 0x0001
        FINAL = 0x0010
        SUPER = 0x0020
        INTERFACE = 0x0200
        ABSTRACT = 0x0400
        SYNTHETIC = 0x1000
        ANNOTATION = 0x2000
        ENUM = 0x4000
        MODULE = 0x8000

    def __init__(self, source: Optional[BinaryIO] = None, *,
                 this: str = 'HelloWorld', super_: str = 'java/lang/Object'):
        # Default to J2SE_7
        self._version = ClassVersion(0x32, 0)
        self.constants = ConstantPool()
        self.access_flags = (
            ClassFile.AccessFlags.PUBLIC |
            ClassFile.AccessFlags.SUPER
        )
        self.this = self.constants.add(
            ConstantClass(
                pool=self.constants,
                name=self.constants.add(UTF8(this))
            )
        )
        self.super_ = self.constants.add(
            ConstantClass(
                pool=self.constants,
                name=self.constants.add(UTF8(super_))
            )
        )
        self._interfaces = []
        self.fields = FieldTable(self)
        self.methods = MethodTable(self)
        self.attributes = AttributeTable(self)
        #: The ClassLoader instance bound to this ClassFile, if any.
        self.classloader = None

        if source:
            self._from_io(source)

    def push_context(self):
        """Push this ClassFile to the top of the class context.

        It's generally better to use the ClassFile as a context manager using
        'with' then to manage the stack manually::

            >>> cf = ClassFile()
            >>> with cf:
            ...     print('Context is automatically managed.')
        """
        class_context().append(self)

    def pop_context(self):
        """Pop this ClassFile off the top of the class context.

        It is a RuntimeError if the ClassFile popped off the top of the stack
        is not _this_ ClassFile.
        """
        cont = class_context()
        if cont:
            ctx = cont.pop()
            if ctx is not self:
                # This should never happen unless a user is manually managing
                # the context stack instead of using the ClassFile as a context
                # manager.
                raise RuntimeError(
                    'A ClassFile tried to pop a context which was not itself.'
                )

    def __enter__(self):
        self.push_context()

    def __exit__(self, _, __, ___):
        self.pop_context()

    def save(self, source: BinaryIO):
        """
        Saves the class to the file-like object `source`.

        :param source: Any file-like object providing write().
        """
        write = source.write

        write(pack(
            '>IHH',
            ClassFile.MAGIC,
            self.version.minor,
            self.version.major
        ))

        self.constants.pack(source)

        write(pack('>H', int(self.access_flags)))
        write(pack(
            f'>HHH{len(self._interfaces)}H',
            self.this.index,
            self.super_.index,
            len(self._interfaces),
            *self._interfaces
        ))

        self.fields.pack(source)
        self.methods.pack(source)
        self.attributes.pack(source)

    def _from_io(self, source: BinaryIO):
        """
        Loads an existing JVM ClassFile from any file-like object.
        """
        read = source.read

        if unpack('>I', source.read(4))[0] != ClassFile.MAGIC:
            raise ValueError('invalid magic number')

        # The version is swapped on disk to (minor, major), so swap it back.
        self.version = unpack('>HH', source.read(4))[::-1]

        # We created some default values when the class was constructed, just
        # purge them.
        self.constants.clear()
        self.constants.unpack(source)

        # ClassFile access_flags, see section #4.1 of the JVM specs.
        self.access_flags = unpack('>H', read(2))

        # The CONSTANT_Class indexes for "this" class and its superclass.
        # Interfaces are a simple list of CONSTANT_Class indexes.
        this_, super_, interfaces_count = unpack('>HHH', read(6))
        self.this = self.constants[this_]
        self.super_ = self.constants[super_]

        self._interfaces = unpack(
            f'>{interfaces_count}H',
            read(2 * interfaces_count)
        )

        self.fields.unpack(source)
        self.methods.unpack(source)
        self.attributes.unpack(source)

    @property
    def version(self) -> ClassVersion:
        """
        The :class:`~lawu.cf.ClassVersion` for this class.

        Example::

            >>> cf = ClassFile(this='HelloWorld')
            >>> cf.version = 51, 0
            >>> print(cf.version)
            ClassVersion(major=51, minor=0)
            >>> print(cf.version.major)
            51
        """
        return self._version

    @version.setter
    def version(self, major_minor: Union[ClassVersion, Sequence]):
        self._version = ClassVersion(*major_minor)

    @property
    def interfaces(self) -> Iterable[ConstantClass]:
        """
        A list of direct superinterfaces of this class as indexes into
        the constant pool, in left-to-right order.
        """
        return [self.constants[idx] for idx in self._interfaces]

    @property
    def bootstrap_methods(self) -> BootstrapMethod:
        """
        Returns the bootstrap methods' table from the BootstrapMethods
        attribute, if one exists. If it does not, one will be created.

        :returns: Table of `BootstrapMethod` objects.
        """
        bootstrap = self.attributes.find_one(name='BootstrapMethods')

        if bootstrap is None:
            bootstrap = self.attributes.create(
                ATTRIBUTE_CLASSES['BootstrapMethods']
            )

        return bootstrap.table

    def __repr__(self):
        return f'<ClassFile(this={self.this.name.value!r})>'
