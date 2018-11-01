"""
Regardless of the origin of a Class (Jasmin, .class, .java, API, etc...) it is
interally structured as a hierarchy of Node objects.
"""
import sys

from typing import List


class Node(object):
    __slots__ = ('children', '_parent', 'line_no')

    def __init__(self, *, parent: 'Node'=None, line_no: int=0, children=None):
        #: List of children for this Node.
        self.children: List[Node] = []
        #: Parent of this Node.
        self._parent = None
        #: The source line number, if known.
        self.line_no = line_no

        if parent:
            self.parent = parent

        if children:
            # If we've been given a list of children we should attach them
            # to us automatically.
            for child in children:
                if child.parent is not None:
                    raise ValueError(
                        'Attempted to attach a node already owned by another '
                        'parent.'
                    )

                child.parent = self

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        value.children.append(self)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}(children={len(self.children)!r})>'
        )

    def pprint(self, indent=2, file=sys.stdout, level=0):
        print('{pre} {self!r}'.format(
            pre=f'[{self.line_no:04}] {(indent * level) * " "} |',
            self=self
        ), file=file)
        for child in self.children:
            child.pprint(indent=indent, file=file, level=level + 1)


class Root(Node):
    """
    Every node in a typical project is an [indirect] child of the Root Node,
    which can contain some top-level directives as well as multiple Classes.
    """


class Bytecode(Node):
    __slots__ = ('major', 'minor')

    def __init__(self, *, major=None, minor=None, parent: 'Node'=None,
                 line_no: int=0, children=None):
        """A Bytecode node changes the bytecode generation version for all
        following Classes.

        :param major: The major version.
        :param minor: The minor version.
        """
        super().__init__(parent=parent, line_no=line_no, children=children)
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


class Class(Node):
    __slots__ = ('access_flags', 'descriptor')

    def __init__(self, *, descriptor, access_flags=None, parent: 'Node'=None,
                 line_no: int=0, children=None):
        super().__init__(parent=parent, line_no=line_no, children=children)
        self.descriptor = descriptor
        self.access_flags = access_flags

    def __repr__(self):
        return f'<Class({self.descriptor!r}, {self.access_flags!r})>'


class Super(Node):
    __slots__ = ('descriptor',)

    def __init__(self, *, descriptor, parent: 'Node'=None, line_no: int=0,
                 children=None):
        super().__init__(parent=parent, line_no=line_no, children=children)
        self.descriptor = descriptor

    def __repr__(self):
        return f'<Super({self.descriptor})>'


class Method(Node):
    __slots__ = ('access_flags', 'descriptor')

    def __init__(self, *, descriptor, access_flags=None, parent: 'Node'=None,
                 line_no: int=0, children=None):
        super().__init__(parent=parent, line_no=line_no, children=children)
        self.descriptor = descriptor
        self.access_flags = access_flags

    def __repr__(self):
        return f'<Method({self.descriptor!r}, {self.access_flags!r})>'


class Label(Node):
    __slots__ = ('name',)

    def __init__(self, *, name, parent: 'Node'=None, line_no: int=0,
                 children=None):
        super().__init__(parent=parent, line_no=line_no, children=children)
        self.name = name

    def __repr__(self):
        return f'<Label({self.name!r})>'


class Instruction(Node):
    __slots__ = ('opcode', 'operands')

    def __init__(self, *, opcode, operands, parent: 'Node'=None,
                 line_no: int=0, children=None):
        super().__init__(parent=parent, line_no=line_no, children=children)
        self.opcode = opcode
        self.operands = operands

    def __repr__(self):
        return f'<Instruction({self.opcode!r}, {self.operands!r})>'


class Limit(Node):
    __slots__ = ('what', 'count')

    def __init__(self, *, what, count, parent: 'Node'=None, line_no: int=0,
                 children=None):
        super().__init__(parent=parent, line_no=line_no, children=children)
        self.what = what
        self.count = count

    def __repr__(self):
        return f'<Limit({self.what!r}, {self.count!r})>'


class Constant(Node):
    __slots__ = ('constant', 'index')

    def __init__(self, *, constant, index=None, parent: 'Node'=None,
                 line_no: int=0, children=None):
        super().__init__(parent=parent, line_no=line_no, children=children)
        self.constant = constant
        self.index = index

    def __repr__(self):
        return f'<Constant({self.constant}, index={self.index!r})>'
