from struct import unpack
from itertools import repeat

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from jawa.core.attributes import AttributeTable
from jawa.core.attribs.attribute import Attribute
from jawa.util.bytecode import StreamDisassembler


class CodeException(object):
    __slots__ = ('_start_pc', '_end_pc', '_handler_pc', '_catch_type', '_cf')

    def __init__(self, class_file, start_pc, end_pc, handler_pc, catch_type):
        self._cf = class_file
        self._start_pc = start_pc
        self._end_pc = end_pc
        self._handler_pc = handler_pc
        self._catch_type = catch_type

    @property
    def start_pc(self):
        """
        The starting IP of the try block (inclusive).
        """
        return self._start_pc

    @property
    def end_pc(self):
        """
        The ending IP of the try block (exclusive).
        """
        return self._end_pc

    @property
    def bounds(self):
        return (self.start_pc, self.end_pc)

    @property
    def handler_pc(self):
        """
        The IP of the exception handler.
        """
        return self._handler_pc

    @property
    def catch_type(self):
        """
        Returns the ``ConstantClass`` for the class that should trigger this
        exception. As a special case, a value of 0 is returned if any exception
        should be caught (used to implement `finally`).
        """
        if self._catch_type != 0:
            return self._cf.constants.get(self._catch_type)
        return 0

    @property
    def class_file(self):
        """
        The :py:class:`jawa.core.cf.ClassFile` this ``CodeException`` is
        associated with.
        """
        return self._cf

    def __repr__(self):
        return (
            '<CodeException(start_pc=%r, end_pc=%r, handler_pc=%r,'
            ' catch_type=%r)>' % (
                self.start_pc,
                self.end_pc,
                self.handler_pc,
                self.catch_type
        ))


class CodeAttribute(Attribute):
    """
    The body of a method.
    """
    NAME = 'Code'

    def __init__(self, class_file, name_i=None, max_stack=None,
            max_locals=None, raw_code=None, ex_table=None, attribs=None):
        super(CodeAttribute, self).__init__(class_file, name_i)
        self._max_stack = max_stack
        self._max_locals = max_locals
        self._raw_code = raw_code
        self._ex_table = ex_table or []
        self._attribs = attribs or AttributeTable(class_file)
        self._code = None

    @property
    def max_stack(self):
        """
        The maximum size of the operand stack at any time. May be out of date
        if the code has been modified since loading.
        """
        return self._max_stack

    @property
    def max_locals(self):
        """
        The size of the method's locals array. May be out of date
        if the code has been modified since loading.
        """
        return self._max_locals

    @property
    def raw_code(self):
        """
        The raw bytecode for this method.
        """
        if self._code:
            return self._code.assemble(cache=True)
        return self._raw_code

    @property
    def exceptions(self):
        """
        The exception table for this method.
        """
        return self._ex_table

    @property
    def attributes(self):
        """
        Returns the :py:class:`jawa.core.attributes.AttributeTable` for this
        method.
        """
        return self._attribs

    @classmethod
    def _load_from_io(cls, class_file, name_i, length, io):
        read = io.read

        max_stack, max_locals, code_length = unpack('>HHI', read(8))
        code = read(code_length)
        ex_table_length = unpack('>H', read(2))[0]
        ex_table = []
        for _ in repeat(None, ex_table_length):
            ex_table.append(CodeException(class_file,
                *unpack('>HHHH', read(8))
            ))
        attribs = AttributeTable(class_file)
        attribs._load_from_io(io)

        return CodeAttribute(
            class_file,
            name_i,
            max_stack=max_stack,
            max_locals=max_locals,
            raw_code=code,
            ex_table=ex_table,
            attribs=attribs
        )

    def n(self):
        sd = StreamDisassembler()
        sio = StringIO(self._raw_code)
        while True:
            try:
                print sd.get_single(sio)
            except IOError:
                return
