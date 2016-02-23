# -*- coding: utf8 -*-
__all__ = ('CodeAttribute', 'CodeException')

from struct import unpack, pack
from itertools import repeat
from collections import namedtuple

from jawa.attribute import Attribute, AttributeTable
from jawa.util.bytecode import (
    read_instruction,
    write_instruction
)

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


CodeException = namedtuple('CodeException', [
    'start_pc', 'end_pc', 'handler_pc', 'catch_type'
])


class CodeAttribute(Attribute):
    """
    A `CodeAttribute` contains the executable bytecode of a single method.

    As a quick example, lets make a "HelloWorld" class with a single method
    that simply returns when it's called:

    .. code-block:: python

        from jawa import ClassFile
        from jawa.util.bytecode import Instruction

        cf = ClassFile.create('HelloWorld')

        main = cf.methods.create(
            # The name of the method
            'main',
            # The signature of the method
            '([Ljava/lang/String;)V',
            # Tell Jawa to automatically create an empty CodeAttribute for
            # us to use.
            code=True
        )
        main.code.max_locals = 1
        main.access_flags.acc_static = True
        main.code.assemble([
            Instruction.from_mnemonic('return')
        ])

        # Save it to disk so we can run it with the JVM.
        with open('HelloWorld.class', 'wb') as fout:
            cf.save(fout)

    .. note::

        Not all :class:`~jawa.methods.Method` objects will have an associated
        `CodeAttribute` - methods that are flagged as `acc_native` or
        `acc_abstract` will never have one.
    """
    def __init__(self, table, name_index=None):
        super(CodeAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'Code'
            ).index
        )
        self._max_stack = 0
        self._max_locals = 0
        self._ex_table = []
        self._attributes = AttributeTable(table.cf, parent=self)
        self._code = ''

    def unpack(self, info):
        """
        Read the CodeAttribute from the byte string `info`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param info: A byte string containing an unparsed CodeAttribute.
        """
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
        self._attributes = AttributeTable(self._cf, parent=self)
        self._attributes.unpack(fio)
        fio.close()

    @property
    def info(self):
        """
        The `CodeAttribute` in packed byte string form.
        """
        fout = StringIO()
        fout.write(pack(
            '>HHI',
            self._max_stack,
            self._max_locals,
            len(self._code)
        ))
        fout.write(self._code)
        fout.write(pack('>H', len(self._ex_table)))
        for exception in self._ex_table:
            fout.write(pack('>HHHH', *exception))
        self._attributes.pack(fout)
        return fout.getvalue()

    @property
    def max_stack(self):
        """The maximum size of the stack."""
        return self._max_stack

    @max_stack.setter
    def max_stack(self, value):
        self._max_stack = value

    @property
    def max_locals(self):
        """The maximum number of locals."""
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
        """
        An :class:`~jawa.attribute.AttributeTable` containing all of the
        attributes associated with this `CodeAttribute`.
        """
        return self._attributes

    def assemble(self, code):
        """
        Assembles an iterable of :class:`~jawa.util.bytecode.Instruction`
        objects into a method's code body.
        """
        fout = StringIO()
        for ins in code:
            write_instruction(fout, fout.tell(), ins)
        self._code = fout.getvalue()
        fout.close()

    def disassemble(self):
        """
        Disassembles this method, yielding an iterable of
        :class:`~jawa.util.bytecode.Instruction` objects.
        """
        fio = StringIO(self._code)

        for ins in iter(lambda: read_instruction(fio, fio.tell()), None):
            yield ins
