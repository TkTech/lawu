# -*- coding: utf8 -*-
import io
import inspect
import functools
from typing import Iterator
from struct import pack
from itertools import repeat
from collections import namedtuple

from jawa.attribute import Attribute, AttributeTable
from jawa.util.bytecode import (
    read_instruction,
    write_instruction,
    Instruction
)

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
    """
    ADDED_IN = '1.0.2'
    MINIMUM_CLASS_VERSION = (45, 3)

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
        self._max_stack, self._max_locals, c_len = info.unpack('>HHI')
        self._code = info.read(c_len)

        # The exception table
        ex_table_len = info.u2()
        self._ex_table = []
        for _ in repeat(None, ex_table_len):
            self._ex_table.append(CodeException(
                *info.unpack('>HHHH')
            ))
        self._attributes = AttributeTable(self.cf, parent=self)
        self._attributes.unpack(info)

    def pack(self):
        """
        The `CodeAttribute` in packed byte string form.
        """
        with io.BytesIO() as file_out:
            file_out.write(pack(
                '>HHI',
                self._max_stack,
                self._max_locals,
                len(self._code)
            ))
            file_out.write(self._code)

            file_out.write(pack('>H', len(self._ex_table)))
            for exception in self._ex_table:
                file_out.write(pack('>HHHH', *exception))

            self._attributes.pack(file_out)
            return file_out.getvalue()

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
        with io.BytesIO() as code_out:
            for ins in code:
                write_instruction(code_out, code_out.tell(), ins)
            self._code = code_out.getvalue()

    def disassemble(self, *, transforms=None) -> Iterator[Instruction]:
        """
        Disassembles this method, yielding an iterable of
        :class:`~jawa.util.bytecode.Instruction` objects.
        """
        if transforms is None:
            if self.cf.classloader:
                transforms = self.cf.classloader.bytecode_transforms
            else:
                transforms = []

        transforms = [self._bind_transform(t) for t in transforms]

        with io.BytesIO(self._code) as code:
            ins_iter = iter(lambda: read_instruction(code, code.tell()), None)
            for ins in ins_iter:
                for transform in transforms:
                    ins = transform(ins)
                yield ins

    def _bind_transform(self, transform):
        sig = inspect.signature(transform, follow_wrapped=True)
        return functools.partial(
            transform,
            **{k: v for k, v in {
                'cf': self.cf,
                'attribute': self
            }.items() if k in sig.parameters}
        )
