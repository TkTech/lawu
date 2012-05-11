# -*- coding: utf8 -*-
from struct import unpack
from itertools import repeat

from jawa.core.attributes import AttributeTable
from jawa.core.descriptor import field_descriptor


class Field(object):
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
        Returns the access flags for this field.
        """
        return self._flags

    @property
    def name(self):
        """
        Returns the name of this field.
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
    def type_(self):
        """
        Returns a human-readable type for this field as parsed from the field's
        descriptor.
        """
        return field_descriptor(self.descriptor)

    @property
    def attributes(self):
        """
        Returns the :py:class:`jawa.core.attributes.AttributeTable` for this
        field.
        """
        return self._attributes

    def __repr__(self):
        return '<Field(name=%r, descriptor=%r, flags=%r)>' % (
            self.name, self.descriptor, self.access_flags
        )


class FieldTable(object):
    """
    A field table represents all of the fields of a ``ClassFile``, as defined
    in section 4.5 of the JVM specification.
    """
    def __init__(self, class_file):
        self._table = []
        self._cf = class_file

    @property
    def class_file(self):
        """
        Returns the :py:class:`jawa.core.classfile.ClassFile` associated with
        this ``FieldTable``.
        """
        return self._cf

    def _load_from_io(self, io):
        """
        Load a FieldTable from a ClassFile. It should never be called manually.
        """
        read = io.read
        append = self._table.append

        count = unpack('>H', read(2))[0]
        for _ in repeat(None, count):
            args = unpack('>3H', read(6))
            attr = AttributeTable()
            attr._load_from_io(io)
            append(Field(self._cf, *args, attributes=attr))
