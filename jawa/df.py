# -*- coding: utf-8 -*-
import itertools
from functools import partial
from struct import unpack
from collections import namedtuple

from jawa.cf import ClassFile
from jawa.util.stream import DexStreamReader
from jawa.util.utf import decode_modified_utf8
from jawa.util.descriptor import method_descriptor
"""
Dalvik Executable support.

The :mod:`jawa.df` module provides tools for working with Android DEX
(``.dex``) files.
"""


FieldItem = namedtuple('FieldItem', 'origin type_ name')
MethodItem = namedtuple('MethodItem', 'origin type_ name')
ClassItem = namedtuple('ClassItem', [
    'origin',
    'access_flags',
    'superclass',
    'interaces',
    'source_file',
    'annotations_off',
    'class_data_off',
    'static_values_off'
])


class DexFile(object):
    SUPPORTED_VERSIONS = ('035', '038')
    ENDIAN_CONSTANT = 0x12345678
    REVERSE_ENDIAN_CONSTANT = 0x78563412
    NO_INDEX = 0xffffffff

    def __init__(self, fio):
        """
        Implements the Android DEX format.

        .. note::

            Currently support is read-only. DexFile support is a work in
            progress.

        .. note::

            All processing is done in-memory. Loading exceptionally large
            DEX files may use large amounts of memory and time. Effort was
            made to make usage simple over efficient.

        :param fio: any file-like object providing ``.read()``.
        """
        # Only set when the DEX file was loaded from disk, in which case it's
        # the adler32 checksum of the file - magic - sum.
        self._checksum = None
        self._signature = None
        self._version = '038'
        self._little_endian = True

        self._link_size = 0
        self._link_off = 0
        self._map_off = None

        self._string_table = []
        self._type_table = []

        self._from_io(fio)

    def _from_io(self, fio):
        """
        Loads an existing DEX file from any file-like object supporting
        seek(), read(), and tell().
        """
        read = fio.read

        magic, version, null = unpack('4s3sc', read(8))
        if magic != 'dex\n' or null != '\x00':
            raise ValueError('invalid magic number')

        if version not in self.SUPPORTED_VERSIONS:
            raise ValueError('unsupported dexfile version')

        self._version = version

        # Before we read anything else we need to find the endianess
        # flag or we may read things incorrectly.
        fio.seek(0x28)
        self._little_endian = unpack('<L', read(4))[0] == \
            self.ENDIAN_CONSTANT
        # ... and back up to the top.
        fio.seek(8)

        dsr = DexStreamReader(fio, self._little_endian)
        self._checksum = dsr.uint()
        self._signature = dsr.unpack('20B')
        # Discard the file size, isn't useful.
        dsr.uint()
        # Discrad the header size, although this might actually be useful in
        # the future to skip over unknown sections. Will future version headers
        # always append? Who knows!
        dsr.uint()
        # We've already read the endian tag, discard it.
        dsr.uint()

        self._link_size = dsr.uint()
        self._link_off = dsr.uint()
        self._map_off = dsr.uint()

        self._string_table = self._read_offset_list(
            dsr,
            self._read_string_item
        )
        self._type_table = self._read_offset_list(
            dsr,
            lambda dsr: dsr.uint()
        )
        proto_table = self._read_offset_list(
            dsr,
            self._read_proto_item
        )
        field_table = self._read_offset_list(
            dsr,
            self._read_field_item
        )
        method_table = self._read_offset_list(
            dsr,
            partial(self._read_method_item, proto_table=proto_table),
        )
        class_table = self._read_offset_list(
            dsr,
            self._read_class_item
        )

        for class_def in class_table:
            pass

    def _read_offset_list(self, dsr, item_callback):
        """
        Most of the header tables follow the same count + offset + list
        format. This helper can be used to save some typing
        """
        count = dsr.uint()
        offset = dsr.uint()

        if offset == 0:
            return

        items = []
        with dsr.jump(offset):
            for i in itertools.repeat(None, count):
                items.append(item_callback(dsr))

        return items

    def _read_string_item(self, dsr):
        with dsr.jump(dsr.uint()):
            # For some idiotic reason this is the length of the
            # *decoded* string, with the encoded string being null
            # terminated so read it in byte-by-byte until we find the
            # end. We just discard the useless length.
            dsr.uleb128()

            c = bytearray()
            while True:
                v = dsr.ubyte()
                if v == 0:
                    break
                c.append(v)

            # Strings are stored as in the JVM using MUTF-8.
            return decode_modified_utf8(c)

    def _read_proto_item(self, dsr):
        """
        Reads the method prototype table.
        """
        # Discard the "shorty" descriptor, which we have no need of.
        dsr.uint()
        returns = self.string_table[self.type_table[dsr.uint()]]

        parameters_offset = dsr.uint()
        if parameters_offset != 0:
            # If non-zero this prototype has a list of parameters
            # at the offset.

            with dsr.jump(parameters_offset):
                parameters = [
                    self.string_table[
                        self.type_table[idx]
                    ]
                    for idx in self._read_type_list(dsr)
                ]
        else:
            parameters = []

        return method_descriptor(
            # Create a "fake" JVM-style long form descriptor so we
            # can re-use method_descriptor.
            u'({0}){1}'.format(u''.join(parameters), returns)
        )

    def _read_type_list(self, dsr):
        """
        Reads a list of types, used in the prototype and class definition
        tables.
        """
        return [dsr.ushort() for _ in itertools.repeat(None, dsr.uint())]

    def _read_field_item(self, dsr):
        return FieldItem(
            self.string_table[self.type_table[dsr.ushort()]],
            self.string_table[self.type_table[dsr.ushort()]],
            self.string_table[dsr.uint()]
        )

    def _read_method_item(self, dsr, proto_table):
        return MethodItem(
            self.string_table[self.type_table[dsr.ushort()]],
            proto_table[dsr.ushort()],
            self.string_table[dsr.uint()]
        )

    def _read_class_item(self, dsr):
        return ClassItem(
            dsr.uint(),
            dsr.uint(),
            dsr.uint(),
            dsr.uint(),
            dsr.uint(),
            dsr.uint(),
            dsr.uint(),
            dsr.uint()
        )

    @property
    def checksum(self):
        return self._checksum

    @property
    def version(self):
        return self._version

    @property
    def little_endian(self):
        return self._little_endian

    @property
    def link_off(self):
        return self._link_off

    @property
    def link_size(self):
        return self._link_size

    @property
    def map_off(self):
        return self._map_off

    @property
    def string_table(self):
        return self._string_table

    @property
    def type_table(self):
        return self._type_table

    @property
    def signature(self):
        """SHA-1 hash of the file minus the magic, checksum, and itself."""
        return self._signature
