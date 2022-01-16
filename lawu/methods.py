from typing import Optional, Callable, Iterator, IO, List
from struct import unpack, pack
from itertools import repeat
from enum import IntFlag

from lawu.constants import UTF8
from lawu.util.descriptor import method_descriptor, JVMType
from lawu.attribute import AttributeTable
from lawu.attributes.code import CodeAttribute


class Method(object):
    class AccessFlags(IntFlag):
        PUBLIC = 0x0001
        PRIVATE = 0x0002
        PROTECTED = 0x0004
        STATIC = 0x0008
        FINAL = 0x0010
        SYNCHRONIZED = 0x0020
        BRIDGE = 0x0040
        VARARGS = 0x0080
        NATIVE = 0x0100
        ABSTRACT = 0x0400
        STRICT = 0x0800
        SYNTHETIC = 0x1000

    def __init__(self, cf):
        self._cf = cf
        self.access_flags = Method.AccessFlags(0)
        self._name_index = 0
        self._descriptor_index = 0
        self.attributes = AttributeTable(cf)

    @property
    def descriptor(self) -> UTF8:
        """
        The UTF8 Constant containing the method's descriptor.
        """
        return self._cf.constants[self._descriptor_index]

    @property
    def name(self) -> UTF8:
        """
        The UTF8 Constant containing the method's name.
        """
        return self._cf.constants[self._name_index]

    @property
    def returns(self) -> JVMType:
        """
        A :class:`~lawu.util.descriptor.JVMType` representing the method's
        return type.
        """
        return method_descriptor(self.descriptor.value).returns

    @property
    def args(self) -> List[JVMType]:
        """
        A list of :class:`~lawu.util.descriptor.JVMType` representing the
        method's argument list.
        """
        return method_descriptor(self.descriptor.value).args

    @property
    def code(self) -> CodeAttribute:
        """
        A shortcut for :code:`method.attributes.find_one(name='Code')`.
        """
        return self.attributes.find_one(name='Code')

    def __repr__(self):
        return f'<Method(name={self.name})>'

    def unpack(self, source: IO):
        """
        Read the Method from the file-like object `fio`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param source: Any file-like object providing `read()`
        """
        self.access_flags = Method.AccessFlags(unpack('>H', source.read(2))[0])
        self._name_index, self._descriptor_index = unpack('>HH', source.read(4))
        self.attributes.unpack(source)

    def pack(self, out: IO):
        """
        Write the Method to the file-like object `out`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when saving a ClassFile.

        :param out: Any file-like object providing `write()`
        """
        out.write(pack('>H', int(self.access_flags)))
        out.write(pack(
            '>HH',
            self._name_index,
            self._descriptor_index
        ))
        self.attributes.pack(out)


class MethodTable(object):
    def __init__(self, cf):
        self._cf = cf
        self._table = []

    def append(self, method: Method):
        self._table.append(method)

    def find_and_remove(self, f: Callable):
        """
        Removes any and all methods for which `f(method)` returns `True`.
        """
        self._table = [fld for fld in self._table if not f(fld)]

    def remove(self, method: Method):
        """
        Removes a `method` from the table by identity.
        """
        self._table = [fld for fld in self._table if fld is not method]

    def create(self, name: str, descriptor: str,
               code: CodeAttribute = None) -> Method:
        """
        Creates a new method from `name` and `descriptor`. If `code` is not
        ``None``, add a `Code` attribute to this method.
        """
        method = Method(self._cf)
        name = self._cf.constants.create_utf8(name)
        descriptor = self._cf.constants.create_utf8(descriptor)
        method._name_index = name.index
        method._descriptor_index = descriptor.index
        method.access_flags.PUBLIC = True

        if code is not None:
            method.attributes.create(CodeAttribute)

        self.append(method)
        return method

    def __iter__(self):
        for method in self._table:
            yield method

    def unpack(self, source: IO):
        """
        Read the MethodTable from the file-like object `source`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when loading a ClassFile.

        :param source: Any file-like object providing `read()`
        """
        method_count = unpack('>H', source.read(2))[0]
        for _ in repeat(None, method_count):
            method = Method(self._cf)
            method.unpack(source)
            self.append(method)

    def pack(self, out: IO):
        """
        Write the MethodTable to the file-like object `out`.

        .. note::

            Advanced usage only. You will typically never need to call this
            method as it will be called for you when saving a ClassFile.

        :param out: Any file-like object providing `write()`
        """
        out.write(pack('>H', len(self)))
        for method in self._table:
            method.pack(out)

    def find(self, *, name: Optional[str] = None, args: Optional[str] = None,
             returns: Optional[str] = None, f: Optional[Callable] = None
             ) -> Iterator[Method]:
        """
        Iterates over the methods table, yielding each matching method. Calling
        without any arguments is equivalent to iterating over the table. For
        example, to get all methods that take three integers and return void::

            for method in cf.methods.find(args='III', returns='V'):
                print(method.name.value)

        Or to get all private methods::

            is_private = lambda m: m.access_flags.acc_private
            for method in cf.methods.find(f=is_private):
                print method.name.value

        :param name: The name of the method(s) to find.
        :param args: The argument descriptor (ex: ``III``)
        :param returns: The return descriptor (Ex: ``V``)
        :param f: Any callable which takes one argument (the method).
        """
        for method in self._table:
            if name is not None and method.name.value != name:
                continue

            descriptor = method.descriptor.value
            end_para = descriptor.find(')')

            m_args = descriptor[1:end_para]
            if args is not None and args != m_args:
                continue

            m_returns = descriptor[end_para + 1:]
            if returns is not None and returns != m_returns:
                continue

            if f is not None and not f(method):
                continue

            yield method

    def find_one(self, **kwargs) -> Optional[Method]:
        """
        Same as ``find()`` but returns only the first result.
        """
        return next(self.find(**kwargs), None)

    def __len__(self):
        return len(self._table)
