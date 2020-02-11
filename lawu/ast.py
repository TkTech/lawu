"""
Regardless of the origin of a Class (Jasmin, .class, .java, API, etc...) it is
interally structured as a hierarchy of Node objects.
"""
import sys
from typing import List

from lawu.util.descriptor import method_descriptor, field_descriptor


class Node:
    __slots__ = ('parent', 'children', 'line_no', 'uuid')

    def __init__(self, *, line_no=0, children=None):
        #: List of children for this Node.
        self.children: List[Node] = []
        #: The parent node.
        self.parent: 'Node' = None
        #: The source line number, if known.
        self.line_no = line_no

        if children:
            self.extend(children)

    def pprint(self, indent='', file=sys.stdout, is_last=False):
        """Pretty-print this node and all of its children.

        :param file: IO object for output, defaults to STDOUT.
        """
        fork = '\u251C'
        dash = '\u2500'
        end = '\u2514'
        pipe = '\u2502'

        file.write(f'[{self.line_no:04}]')
        file.write(f'{indent}{end if is_last else fork}{dash}')

        file.write(repr(self))
        file.write('\n')
        file.flush()

        child_count = len(self.children) - 1
        for i, child in enumerate(self.children):
            child.pprint(
                indent=f'{indent}{" " if is_last else pipe} ',
                file=file,
                is_last=child_count == i
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
                if child.node_name != name:
                    continue

            if f is not None:
                if not f(child):
                    continue

            yield child

    def find_one(self, **kwargs):
        try:
            return next(self.find(**kwargs))
        except StopIteration:
            return None

    def append(self, value):
        self.extend([value])

    def extend(self, value):
        self.children.extend(value)
        for child in value:
            child.parent = self

    def __iter__(self):
        yield from self.children

    def __repr__(self):
        return f'<{self.__class__.__name__}()>'

    def __iadd__(self, value: 'Node'):
        self.extend([value])
        return self

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

    def same(self, other):
        """Compare the entire AST of `other` to this one.

        Unlike simple equality (left == right) this checks all children
        as well.
        """
        if len(other.children) != len(self.children):
            return False

        for i, own_child in enumerate(self.children):
            if other.children[i] != own_child:
                return False

            if not other.children[i].same(own_child):
                return False

        return True


class Root(Node):
    """
    Every node in a typical project is an [indirect] child of the Root Node,
    which can contain some top-level directives as well as multiple Classes.
    """
    def __eq__(self, other):
        return isinstance(other, self.__class__)


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
        return self.major == other.major and self.minor == other.minor


class Class(Node):
    __slots__ = ('access_flags', 'descriptor')

    def __init__(self, *, descriptor, access_flags=None, line_no=0,
                 children=None):
        super().__init__(line_no=line_no, children=children)
        self.descriptor = descriptor
        self.access_flags = access_flags

    def __repr__(self):
        return f'<Class({self.descriptor!r}, {self.access_flags!r})>'

    def __eq__(self, other):
        return (
            self.descriptor == other.descriptor
            and self.access_flags == other.access_flags
        )


class Super(Node):
    __slots__ = ('descriptor',)

    def __init__(self, *, descriptor, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.descriptor = descriptor

    def __repr__(self):
        return f'<Super({self.descriptor!r})>'

    def __eq__(self, other):
        return self.descriptor == other.descriptor


class Method(Node):
    __slots__ = ('access_flags', 'name', 'descriptor')

    def __init__(self, *, name, descriptor, access_flags=None, line_no=0,
                 children=None):
        super().__init__(line_no=line_no, children=children)
        self.name = name
        self.descriptor = descriptor
        self.access_flags = access_flags

    def __repr__(self):
        return f'<Method({self.name!r}, {self.descriptor!r})>'

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


class Code(Node):
    def __init__(self, *, max_locals=0, max_stack=0, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)

        self.max_locals = max_locals
        self.max_stack = max_stack

    def __repr__(self):
        return (
            f'<Code(max_locals={self.max_locals!r},'
            f' max_stack={self.max_stack!r})>'
        )


class Label(Node):
    __slots__ = ('name',)

    def __init__(self, name, *, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.name = name

    def __repr__(self):
        return f'<Label({self.name!r})>'

    def __eq__(self, other):
        return self.name == other.name


class Instruction(Node):
    __slots__ = ('opcode',)

    def __init__(self, opcode, *, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.opcode = opcode

    def __repr__(self):
        return f'<Instruction({self.opcode!r})>'

    @property
    def operands(self):
        yield from self.find(f=lambda n: isinstance(n, Operand))

    def __eq__(self, other):
        return self.opcode == other.opcode


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
        return self.target == other.target


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
        return self.target == other.target and self.match == other.match


class Local(Operand):
    __slots__ = ('slot',)

    def __init__(self, *, slot, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.slot = slot

    def __repr__(self):
        return f'<Local({self.slot!r})>'


class String(Operand):
    __slots__ = ('value',)

    def __init__(self, *, value, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.value = value

    def __repr__(self):
        return f'<String({self.value!r})>'


class Number(Operand):
    __slots__ = ('value',)

    def __init__(self, *, value, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.value = value

    def __repr__(self):
        return f'<Number({self.value!r})>'


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


class Implements(Node):
    __slots__ = ('descriptor',)

    def __init__(self, *, descriptor, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.descriptor = descriptor

    def __repr__(self):
        return f'<Implements({self.descriptor!r})>'


class Field(Node):
    __slots__ = ('name', 'descriptor', 'access_flags')

    def __init__(self, *, name, descriptor, access_flags, line_no=0,
                 children=None):
        super().__init__(line_no=line_no, children=children)
        self.name = name
        self.descriptor = descriptor
        self.access_flags = access_flags

    def __repr__(self):
        return f'<Field({self.name!r}, {self.descriptor!r})>'

    @property
    def parsed_descriptor(self):
        return field_descriptor(self.descriptor)


class Signature(Node):
    __slots__ = ('signature',)

    def __init__(self, *, signature, line_no=0, children=None):
        super().__init__(line_no=line_no, children=children)
        self.signature = signature

    def __repr__(self):
        return f'<Signature({self.signature!r})>'
