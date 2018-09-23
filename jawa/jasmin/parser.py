import sys
import itertools
from enum import Enum, auto
from typing import List, Any, Iterator

from jawa.jasmin.tokenizer import Token, TokenType
from jawa.jasmin.errors import InvalidTokenError, UnknownDirectiveError


class NodeTypes(Enum):
    ROOT = auto()
    CLASS = auto()
    METHOD = auto()
    FIELD = auto()
    SUPER = auto()
    LIMIT = auto()
    INSTRUCTION = auto()
    BYTECODE = auto()
    COMMENT = auto()
    END = auto()


class Node(object):
    def __init__(self, *, node_type: NodeTypes, value=None, parent=None,
                 line_no: int=0):
        #: Type of Node.
        self.node_type: NodeTypes = node_type
        #: List of children for this Node.
        self.children: List[Node] = []
        #: The literal node value, if this node contains one.
        self.value: Any = value
        #: List of parents for this node.
        self._parent: Node = None
        #: The source line number, if known.
        self.line_no: int = line_no

        if parent:
            self.parent = parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        value.children.append(self)

    def __repr__(self):
        return (
            f'<Node({self.node_type!r}, '
            f'value={self.value!r}, '
            f'children={self.children!r})>'
        )

    def pprint(self, indent=2, file=sys.stdout, level=0):
        pre = f'[{self.line_no:04}] {(indent * level) * " "} |'
        print(f'{pre} {self.node_type.name} {self.value}', file=file)
        for child in self.children:
            child.pprint(indent=indent, file=file, level=level + 1)


def _to_next(tokens: Iterator[Token], token_type):
    # Consume tokens up until a token of `token_type` is encountered,
    # returning (<consumed_tokens>, <token_stream>).
    t = []
    for i, token in enumerate(tokens):
        if token_type is not None and token.token_type == token_type:
            # itertools.chain is elegant, but what kind of overhead are we
            # getting when there are potentially hundreds of chains-on-chains?
            return t, itertools.chain([token], tokens)
        elif token.token_type != TokenType.COMMENT:
            # We should record trailing comments but for now we discard them.
            t.append(token)
    return t, iter([])


def parse(tokens: Iterator[Token]) -> Node:
    """
    Parse an iterable of Tokens to produce an Abstract Syntax Tree (AST).

    :param tokens: An iterable of tokenizer tokens.
    :return: The root node.
    """
    root = Node(node_type=NodeTypes.ROOT)
    parent = root

    while True:
        try:
            t: Token = next(tokens)
        except StopIteration:
            return root

        if t.token_type == TokenType.COMMENT:
            continue

        if parent.node_type == NodeTypes.ROOT:
            # Only directives and comments are allowed at the root level
            # of a source file.
            if t.token_type != TokenType.DIRECTIVE:
                raise InvalidTokenError(
                    'Only directives & comments are allowed at the root.',
                    token=t
                )
