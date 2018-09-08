import sys
import itertools
from enum import Enum
from typing import List, Any, Iterator
from ast import literal_eval

from jawa.jasmin.tokenizer import Token, TokenType
from jawa.jasmin.errors import InvalidTokenError, UnknownDirectiveError


class NodeTypes(Enum):
    ROOT = 0
    CLASS = 1
    DIRECTIVE = 2
    METHOD = 3
    FIELD = 4
    SUPER = 5
    LIMIT = 6
    INSTRUCTION = 7
    BYTECODE = 8


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
    t = []
    for i, token in enumerate(tokens):
        if token_type is not None and token.token_type == token_type:
            return t, itertools.chain([token], tokens)
        t.append(token)
    return t, iter([])


def parse(tokens: Iterator[Token]):
    """
    Parse an iterable of Tokens to produce an Abstract Syntax Tree (AST).

    :param tokens:
    :return:
    """
    root = Node(node_type=NodeTypes.ROOT)
    parent = root

    s = NodeTypes.ROOT
    while True:
        try:
            t: Token = next(tokens)
        except StopIteration:
            return root

        # Comments might be useful to preserve in the AST for the future,
        # but for now we just completely ignore them.
        if t.token_type == TokenType.COMMENT:
            continue
        elif t.token_type == TokenType.END_OF_LINE:
            continue

        if s == NodeTypes.ROOT:
            if t.token_type != TokenType.DIRECTIVE:
                raise InvalidTokenError(
                    'Only directives may be contained at the top level.',
                    token=t
                )

            args, tokens = _to_next(tokens, TokenType.END_OF_LINE)
            if t.value == 'class':
                parent = Node(
                    node_type=NodeTypes.CLASS,
                    value=([a.value for a in args[0:-1]], args[-1].value),
                    parent=root,
                    line_no=t.line_no
                )
            elif t.value == 'super':
                Node(
                    node_type=NodeTypes.SUPER,
                    value=args[0].value,
                    parent=parent,
                    line_no=t.line_no
                )
            elif t.value == 'bytecode':
                Node(
                    node_type=NodeTypes.BYTECODE,
                    value=args[0].value,
                    parent=parent,
                    line_no=t.line_no
                )
            elif t.value == 'method':
                parent = Node(
                    node_type=NodeTypes.METHOD,
                    value=([a.value for a in args[0:-1]], args[-1].value),
                    parent=parent,
                    line_no=t.line_no
                )
                s = NodeTypes.METHOD
            else:
                raise UnknownDirectiveError(
                    f'Unknown or unsupported directive {t.value!r} '
                    f'encountered while parsing top-level.',
                    token=t
                )
        elif s == NodeTypes.METHOD:
            if t.token_type == TokenType.DIRECTIVE:
                if t.value == 'limit':
                    args, tokens = _to_next(tokens, TokenType.END_OF_LINE)
                    Node(
                        node_type=NodeTypes.LIMIT,
                        value=(args[0].value, literal_eval(args[1].value)),
                        parent=parent,
                        line_no=t.line_no
                    )
                elif t.value == 'end':
                    args, tokens = _to_next(tokens, TokenType.END_OF_LINE)
                    parent = parent.parent
                    s = NodeTypes.ROOT
                else:
                    raise UnknownDirectiveError(
                        f'Unknown or unsupported directive {t.value!r} '
                        f'encountered while parsing method.',
                        token=t
                    )
            elif t.token_type == TokenType.GENERIC:
                args, tokens = _to_next(tokens, TokenType.END_OF_LINE)
                Node(
                    node_type=NodeTypes.INSTRUCTION,
                    value=(t.value, [a.value for a in args]),
                    parent=parent,
                    line_no=t.line_no
                )
