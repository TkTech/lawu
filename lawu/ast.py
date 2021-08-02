"""
Regardless of the origin of a Class (Jasmin, .class, .java, API, etc...) it is
interally structured as a hierarchy of Node objects.
"""
import io
import sys
from typing import List, Optional, Dict
from enum import IntFlag
from abc import ABC, abstractmethod
from dataclasses import dataclass

from lawu.util.descriptor import method_descriptor, field_descriptor


class Node(ABC):
    __slots__ = ('parent', 'children', 'line_no', 'col_no', 'col_end_no')

    def __init__(self, *, line_no=0, col_no=0, col_end_no=0, children=None):
        #: List of children for this Node.
        self.children: List[Node] = []
        #: The parent node.
        self.parent: Optional['Node'] = None
        #: The source line number, if known.
        self.line_no: int = line_no
        #: The starting column number, if known.
        self.col_no: int = col_no
        #: The ending column number, if known.
        self.col_end_no: int = col_end_no

        if children:
            self.extend(children)

    def pretty(self, *, indent='', show_line_no=True):
        """Pretty-print this node and all of its children, returning the
        result as a string.

        :param indent: The indent to apply at the start of each line.
                       [default: '']
        :param show_line_no: True if source line numbers should be shown.
                             [default: True]
        """
        with io.StringIO() as out:
            self.pprint(indent=indent, show_line_no=show_line_no, file=out)
            return out.getvalue()

    def pprint(self, *, indent='', file=sys.stdout, is_last=False,
               show_line_no=True):
        """Pretty-print this node and all of its children to a file-like
        object.

        :param indent: The indent to apply at the start of each line.
                       [default: '']
        :param file: IO object for output. [default: sys.stdout]
        :param is_last: True if this is the last child in a sequence.
                        [default: False]
        :param show_line_no: True if source line numbers should be shown.
                             [default: True]
        """
        fork = '\u251C'
        dash = '\u2500'
        end = '\u2514'
        pipe = '\u2502'

        if show_line_no:
            file.write(f'[{self.line_no or 0:04}]')
        file.write(f'{indent}{end if is_last else fork}{dash}')

        file.write(repr(self))
        file.write('\n')
        file.flush()

        child_count = len(self) - 1
        for i, child in enumerate(self):
            child.pprint(
                indent=f'{indent}{" " if is_last else pipe} ',
                file=file,
                is_last=child_count == i,
                show_line_no=show_line_no
            )

    @property
    def node_name(self):
        return self.__class__.__name__.lower()

    def find(self, *, name=None, f=None, depth=None):
        """Find and yield child nodes that match all given filters.

        :param name: The lowercase name of a node to match.
        :param f: Any callable object which will be given the node.
        :param depth: The maximum depth to search for matching children.
                      By default only immediate children are checked. Passing
                      a negative value will search with no limit.
        """
        for child in self.children:
            if depth is not None and depth != 0:
                yield from child.find(
                    name=name,
                    f=f,
                    depth=depth - 1
                )

            if name is not None:
                if child.node_name != name.lower():
                    continue

            if f is not None:
                if not f(child):
                    continue

            yield child

    def find_one(self, **kwargs) -> Optional['Node']:
        return next(self.find(**kwargs), None)

    def append(self, value):
        self.extend([value])

    def extend(self, value):
        for child in value:
            child.parent = self
            self.children.append(child)

    def fix_missing_locations(self):
        """Recursively populates line_no values on child nodes using the parent
        value."""
        for child in self.children:
            if child.line_no == 0:
                child.line_no = self.line_no
            child.fix_missing_locations()

    def descend(self, f):
        f(self)
        for child in self.children:
            child.descend(f)

    def _re_eq(self, other) -> bool:
        # Recurisive equality check. Used by nodes implementations of __eq__
        # when it's possible for them to have children.
        if len(other) != len(self) or other is self:
            return False

        other_children = iter(other)
        for own_child in self:
            other_child = next(other_children)
            if other_child != own_child:
                return False

            if not other_child._re_eq(own_child):
                return False

        return True

    def __iter__(self):
        yield from self.children

    def __repr__(self):
        return f'<{type(self).__name__}()>'

    def __iadd__(self, value: 'Node'):
        self.extend([value])
        return self

    def __len__(self):
        return len(self.children)

    def __bool__(self):
        return True

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass


class Fragment(Node):
    """A (typically) temporary container for a selection of AST nodes."""
    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self._re_eq(other)
        )


class Root(Node):
    """
    Every node in a typical project is an [indirect] child of the Root Node,
    which can contain some top-level directives as well as multiple Classes.
    """


class Bytecode(Node):
    __slots__ = ('major', 'minor')

    def __init__(self, *, major=None, minor=None, line_no=0, children=None):
        """A Bytecode node changes the bytecode generation version for all
        following Classes.

        :param major: The major version.
        :param minor: The minor version.
        """
        super().__init__(line_no=line_no, children=children)
        self.major = major
        self.minor = minor

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

    @property
    def version(self):
        return (self.major, self.minor)

    @version.setter
    def version(self, major, minor):
        self.major = major
        self.minor = minor

    def __repr__(self):
        return f'<Bytecode(major={self.major!r}, minor={self.minor!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.major == other.major and
            self.minor == other.minor and
            self._re_eq(other)
        )


class Class(Node):
    __slots__ = ('access_flags', 'descriptor')

    class AccessFlags(IntFlag):
        PUBLIC = 0x0001
        FINAL = 0x0010
        SUPER = 0x0020
        INTERFACE = 0x0200
        ABSTRACT = 0x0400
        SYNTHETIC = 0x1000
        ANNOTATION = 0x2000
        ENUM = 0x4000
        MODULE = 0x8000

    def __init__(self, *, descriptor, access_flags=None, line_no=0,
                 children=None):
        super().__init__(line_no=line_no, children=children)
        self.descriptor = descriptor
        self.access_flags = access_flags

    def __repr__(self):
        return f'<Class({self.descriptor!r}, {self.access_flags!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.descriptor == other.descriptor and
            self.access_flags == other.access_flags and
            self._re_eq(other)
        )


class Super(Node):
    __slots__ = ('descriptor',)

    def __init__(self, *, descriptor, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.descriptor = descriptor

    def __repr__(self):
        return f'<Super({self.descriptor!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.descriptor == other.descriptor and
            self._re_eq(other)
        )


class Method(Node):
    __slots__ = ('access_flags', 'name', 'descriptor')

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

    def __init__(self, *, name, descriptor, access_flags: AccessFlags,
                 line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.name = name
        self.descriptor = descriptor
        self.access_flags = access_flags

    def __repr__(self):
        return (
            f'<Method({self.name!r}, {self.descriptor!r}),'
            f' {self.access_flags!r}>'
        )

    @property
    def parsed_descriptor(self):
        return method_descriptor(self.descriptor)

    @property
    def args(self):
        return self.parsed_descriptor.args

    @property
    def returns(self):
        return self.parsed_descriptor.returns

    @property
    def code(self):
        return self.find_one(name='code')

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.name == other.name and
            self.descriptor == other.descriptor and
            self._re_eq(other)
        )


class Label(Node):
    __slots__ = ('name',)

    def __init__(self, name, *, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.name = name

    def __repr__(self):
        return f'<Label({self.name!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.name == other.name and
            self._re_eq(other)
        )


class Instruction(Node):
    __slots__ = ('name',)

    def __init__(self, name, *, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.name = name

    def __repr__(self):
        return f'<Instruction({self.name!r})>'

    @property
    def operands(self):
        return list(self.find(f=lambda n: isinstance(n, Operand)))

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.name == other.name and
            self._re_eq(other)
        )


class Operand(Node):
    pass


class Jump(Operand):
    __slots__ = ('target',)

    def __init__(self, target, *, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.target = target

    def __repr__(self):
        return f'<Jump({self.target!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.target == other.target and
            self._re_eq(other)
        )


class ConditionalJump(Operand):
    __slots__ = ('target', 'match')

    def __init__(self, *, match, target, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.target = target
        self.match = match

    def __repr__(self):
        return (
            f'<ConditionalJump(match={self.match!r}, target={self.target!r})>'
        )

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.target == other.target and
            self.match == other.match and
            self._re_eq(other)
        )


class Local(Operand):
    __slots__ = ('slot',)

    def __init__(self, *, slot, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.slot = slot

    def __repr__(self):
        return f'<Local({self.slot!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.slot == other.slot and
            self._re_eq(other)
        )


class String(Operand):
    __slots__ = ('value',)

    def __init__(self, *, value, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.value = value

    def __repr__(self):
        return f'<String({self.value!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.value == other.value and
            self._re_eq(other)
        )


class Number(Operand):
    __slots__ = ('value',)

    def __init__(self, *, value, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.value = value

    def __repr__(self):
        return f'<Number({self.value!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.value == other.value and
            self._re_eq(other)
        )


class Reference(Operand):
    __slots__ = ('class_', 'target', 'is_type')

    def __init__(self, *, class_, target, is_type, line_no=0,
                 children=None):
        super().__init__(line_no=line_no, children=children)
        self.class_ = class_
        self.target = target
        self.is_type = is_type

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}({self.class_!r},'
            f' {self.target!r}, {self.is_type!r})>'
        )

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.class_ == other.class_ and
            self.target == other.target and
            self.is_type == other.is_type and
            self._re_eq(other)
        )


class MethodReference(Reference):
    pass


class InterfaceMethodRef(Reference):
    pass


class FieldReference(Reference):
    pass


class ClassReference(Operand):
    __slots__ = ('descriptor',)

    def __init__(self, *, descriptor, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.descriptor = descriptor

    def __repr__(self):
        return f'<ClassReference({self.descriptor!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.descriptor == other.descriptor and
            self._re_eq(other)
        )


class InvokeDynamic(Operand):
    __slots__ = ('bootstrap_index', 'name', 'is_type')

    def __init__(self, *, bootstrap_index, name, is_type, line_no=0,
                 children=None):
        super().__init__(line_no=line_no, children=children)
        self.bootstrap_index = bootstrap_index
        self.name = name
        self.is_type = is_type

    def __repr__(self):
        return (
            f'<InvokeDynamic({self.bootstrap_index!r}, {self.name!r},'
            f' {self.is_type!r})>'
        )

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.bootstrap_index == other.bootstrap_index and
            self.name == other.name and
            self.is_type == other.is_type and
            self._re_eq(other)
        )


class Implements(Node):
    __slots__ = ('descriptor',)

    def __init__(self, *, descriptor, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.descriptor = descriptor

    def __repr__(self):
        return f'<Implements({self.descriptor!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.descriptor == other.descriptor and
            self._re_eq(other)
        )


class Field(Node):
    __slots__ = ('name', 'descriptor', 'access_flags')

    class AccessFlags(IntFlag):
        PUBLIC = 0x0001
        PRIVATE = 0x0002
        PROTECTED = 0x0004
        STATIC = 0x0008
        FINAL = 0x0010
        VOLATILE = 0x0040
        TRANSIENT = 0x0080
        SYNTHETIC = 0x1000
        ENUM = 0x4000

    def __init__(self, *, name, descriptor, access_flags: AccessFlags,
                 line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.name = name
        self.descriptor = descriptor
        self.access_flags = access_flags

    def __repr__(self):
        return (
            f'<Field({self.name!r}, {self.descriptor!r},'
            f' {self.access_flags!r})>'
        )

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.name == other.name and
            self.descriptor == other.descriptor and
            self.access_flags == other.access_flags and
            self._re_eq(other)
        )

    @property
    def parsed_descriptor(self):
        return field_descriptor(self.descriptor)


class TryCatch(Node):
    __slots__ = ('target', 'handles')

    def __init__(self, target, handles, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.target = target
        self.handles = handles

    def __repr__(self):
        return f'<TryCatch({self.target!r}, {self.handles!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.target == other.target and
            self.handles == other.handles and
            self._re_eq(other)
        )


class Finally(TryCatch):
    def __init__(self, target, line_no=0, children=None):
        super().__init__(target, None, line_no=line_no, children=children)

    def __repr__(self):
        return f'<Finally({self.target!r})>'


class Attribute(Node):
    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self._re_eq(other)
        )


class UnknownAttribute(Attribute):
    __slots__ = ('name', 'payload')

    def __init__(self, name, payload, *, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.name = name
        self.payload = payload

    def __repr__(self):
        return (
            f'<UnknownAttribute(name={self.name!r},'
            f' payload={len(self.payload)} bytes)>'
        )

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.name == other.name and
            self.payload == other.payload and
            self._re_eq(other)
        )


class Code(Attribute):
    __slots__ = ('max_locals', 'max_stacks')

    def __init__(self, *, max_locals=0, max_stack=0, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.max_locals = max_locals
        self.max_stack = max_stack

    def __repr__(self):
        return (
            f'<Code(max_locals={self.max_locals!r},'
            f' max_stack={self.max_stack!r})>'
        )

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.max_locals == other.max_locals and
            self.max_stack == other.max_stack and
            self._re_eq(other)
        )


class EnclosingMethod(Attribute):
    __slots__ = ('enclosing_class', 'name_and_type')

    def __init__(self, *, enclosing_class, name_and_type, line_no, children):
        super().__init__(line_no=line_no, children=children)
        self.enclosing_class = enclosing_class
        self.name_and_type = name_and_type

    def __repr__(self):
        return (
            f'<EnclosingMethod(class={self.enclosing_class!r},'
            f' name_and_type={self.name_and_type!r})>'
        )

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.enclosing_class == other.enclosing_class and
            self.name_and_type == other.name_and_type and
            self._re_eq(other)
        )


class Deprecated(Attribute):
    pass


class Synthetic(Attribute):
    pass


class ValueAttribute(Attribute):
    __slots__ = ('value',)

    def __init__(self, *, value, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.value = value

    def __repr__(self):
        return f'<{type(self).__name__}({self.value!r})>'

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.value == other.value and
            self._re_eq(other)
        )


class Signature(ValueAttribute):
    @property
    def signature(self):
        return self.value

    @signature.setter
    def signature(self, new_signature):
        self.value = new_signature


class ConstantValue(ValueAttribute):
    pass

class SourceFile(ValueAttribute):
    pass


class TableAttribute(Attribute):
    __slots__ = ('entries',)

    def __init__(self, *, entries, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.entries = entries

    def __eq__(self, other):
        return (
            isinstance(self, other.__class__) and
            self.entries == other.entries and
            self._re_eq(other)
        )


class BootstrapMethods(TableAttribute):
    pass


class Exceptions(TableAttribute):
    pass


class InnerClasses(TableAttribute):
    pass


class LineNumberTable(TableAttribute):
    pass


class LocalVariableTable(TableAttribute):
    pass


class LocalVariableTypeTable(TableAttribute):
    pass
