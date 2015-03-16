# -*- coding: utf8 -*-
__all__ = ('CodeAttribute', 'CodeException')

from struct import unpack, pack
from itertools import repeat
from collections import namedtuple

from jawa.constants import Constant
from jawa.attribute import Attribute, AttributeTable
from jawa.util.bytecode import (
    read_instruction,
    write_instruction
)

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import BytesIO
        StringIO = BytesIO


CodeException = namedtuple('CodeException', [
    'start_pc', 'end_pc', 'handler_pc', 'catch_type'
])


class CodeAttribute(Attribute):
    @classmethod
    def create(cls, cf):
        c = cls(cf, cf.constants.create_utf8('Code').index)
        c._max_stack = 0
        c._max_locals = 0
        c._ex_table = []
        c._attributes = AttributeTable(cf)
        c._code = ''
        return c

    def unpack(self, info):
        fio = StringIO(info)
        self._max_stack, self._max_locals, c_len = unpack('>HHI', fio.read(8))
        self._code = fio.read(c_len)

        # The exception table
        ex_table_len = unpack('>H', fio.read(2))[0]
        self._ex_table = []
        for _ in repeat(None, ex_table_len):
            self._ex_table.append(CodeException(
                *unpack('>HHHH', fio.read(8))
            ))
        self._attributes = AttributeTable(self._cf)
        self._attributes._from_io(fio)
        fio.close()

    @property
    def info(self):
        fout = StringIO()
        fout.write(pack('>HHI',
            self._max_stack,
            self._max_locals,
            len(self._code)
        ))
        fout.write(self._code)
        fout.write(pack('>H',
            len(self._ex_table)
        ))
        for exception in self._ex_table:
            fout.write(pack('>HHHH', *exception))
        self._attributes._to_io(fout)
        return fout.getvalue()

    @property
    def max_stack(self):
        return self._max_stack

    @max_stack.setter
    def max_stack(self, value):
        self._max_stack = value

    @property
    def max_locals(self):
        return self._max_locals

    @max_locals.setter
    def max_locals(self, value):
        self._max_locals = value

    @property
    def exception_table(self):
        return self._ex_table

    @property
    def code(self):
        return self._code

    @property
    def attributes(self):
        return self._attributes

    def assemble(self, code):
        """
        Assembles an iterable of :class:`~jawa.util.bytecode.Instruction`
        objects into a methods code body.
        """
        fout = StringIO()
        for ins in code:
            write_instruction(fout, fout.tell(), ins)
        self._code = fout.getvalue()
        fout.close()

    def disassemble(self):
        """
        Disassembles this method.
        """
        fio = StringIO(self._code)

        for ins in iter(lambda: read_instruction(fio, fio.tell()), None):
            yield ins
