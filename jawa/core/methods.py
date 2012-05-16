# -*- coding: utf8 -*-
from struct import unpack
from itertools import repeat

from jawa.core.attributes import AttributeTable
from jawa.util.descriptor import method_descriptor


class Method(object):
    """
    Represents a single Method of a JVM class.
    """
    def __init__(self, class_file, flags=0, name_i=None, descriptor_i=None,
            attributes=None):
        self._cf = class_file
        self._flags = flags
        self._name_i = name_i
        self._descriptor_i = descriptor_i
        self._attributes = attributes

    @property
    def access_flags(self):
        """
        Returns the access flags for this ``Method``.
        """
        return self._flags

    @property
    def name(self):
        """
        Returns the name of this ``Method``.
        """
        return self._cf.constants.get(self._name_i)

    @property
    def descriptor(self):
        """
        Returns the JVM type descriptor string as described in section 4.3 of
        the JVM specification.
        """
        return self._cf.constants.get(self._descriptor_i)

    @property
    def returns(self):
        """
        Returns a human-readable return type for this ``Method`` as parsed from
        the method's descriptor.
        """
        return method_descriptor(self.descriptor)[1]

    @property
    def args(self):
        """
        Returns a tuple of human-readable method argument types for this
        ``Method`` as parsed from the method's descriptor.
        """
        return method_descriptor(self.descriptor)[0]

    @property
    def attributes(self):
        """
        Returns the :py:class:`jawa.core.attributes.AttributeTable` for this
        ``Method``.
        """
        return self._attributes

    def __repr__(self):
        return '<Method(name=%r, returns=%r, args=%r, flags=%r)>' % (
            self.name, self.returns, self.args, self.access_flags
        )

    @property
    def class_file(self):
        """
        Returns the :py:class:`jawa.core.cf.ClassFile` associated with this
        ``Method``.
        """
        return self._cf


class MethodTable(object):
    def __init__(self, class_file):
        self._cf = class_file
        self._table = []

    @property
    def class_file(self):
        """
        Returns the :py:class:`jawa.core.cf.ClassFile` associated with this
        ``MethodTable``.
        """
        return self._cf

    def _load_from_io(self, io):
        """
        Load a ``MethodTable`` from a ``ClassFile``. It should never be called
        manually.
        """
        read = io.read
        append = self._table.append

        count = unpack('>H', read(2))[0]
        for _ in repeat(None, count):
            args = unpack('>3H', read(6))
            attr = AttributeTable(self._cf)
            attr._load_from_io(io)
            append(Method(self._cf, *args, attributes=attr))
