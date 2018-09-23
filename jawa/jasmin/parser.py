import sys
from ast import literal_eval
from typing import List, Iterator

from jawa.jasmin.tokenizer import Token, TokenType
from jawa.jasmin.errors import (
    ParserError,
    InvalidTokenError,
    UnknownDirectiveError
)


DIRECTIVES = {}


def directive(*, name=None, allowed_in=None):
    # TODO: This is dirty, and makes both the parser and extending
    #       supported directives global. Find a better way.
    def _f(cls):
        DIRECTIVES[name or cls.__name__.lower()] = (
            cls,
            allowed_in
        )
        return cls
    return _f


class Node(object):
    __slots__ = ('children', '_parent', 'line_no')

    def __init__(self, parent: 'Node'=None, *, line_no: int=0):
        #: List of children for this Node.
        self.children: List[Node] = []
        #: Parent of this Node.
        self._parent = None
        #: The source line number, if known.
        self.line_no = line_no

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
            f'<{self.__class__.__name__}(children={len(self.children)!r})>'
        )

    def pprint(self, indent=2, file=sys.stdout, level=0):
        print('{pre} {self!r}'.format(
            pre=f'[{self.line_no:04}] {(indent * level) * " "} |',
            self=self
        ), file=file)
        for child in self.children:
            child.pprint(indent=indent, file=file, level=level + 1)

    def parse_from_tokens(self, tokens):
        raise NotImplementedError()


class Root(Node):
    def parse_from_tokens(self, tokens):
        for t in tokens:
            if t.token_type == TokenType.END_OF_LINE:
                continue

            if t.value[0] != '.':
                raise InvalidTokenError(
                    'Only directives & comments are allowed at the top-level.',
                    token=t
                )

            try:
                parser_class, allowed_in = DIRECTIVES[t.value[1:]]
            except KeyError:
                raise UnknownDirectiveError(
                    f'Don\'t know how to handle {t.value[1:]!r}.',
                    token=t
                )

            if self.__class__.__name__ not in allowed_in:
                raise ParserError(
                    f'Directive {t.value[1:]!r} not allowed here.',
                    token=t
                )

            node = parser_class(self, line_no=t.line_no)
            node.parse_from_tokens(tokens)


@directive(allowed_in={'Root'})
class Bytecode(Node):
    __slots__ = ('major', 'minor')

    def __init__(self, parent: 'Node'=None, *, line_no: int = 0):
        super().__init__(parent=parent, line_no=line_no)
        self.major = None
        self.minor = None

    def parse_from_tokens(self, tokens):
        value = next(tokens).value.split('.')
        self.major = literal_eval(value[0])
        self.minor = literal_eval(value[1])

    def __repr__(self):
        return f'<Bytecode(major={self.major!r}, minor={self.minor!r})>'


@directive(allowed_in={'Root'})
class Class(Node):
    __slots__ = ('access_flags', 'descriptor')

    def __init__(self, parent: 'Node'=None, *, line_no: int=0):
        super().__init__(parent=parent, line_no=line_no)
        self.access_flags = None
        self.descriptor = None

    def parse_from_tokens(self, tokens):
        line = tokens.get_line()
        self.access_flags = [t.value for t in line[:-1]]
        self.descriptor = line[-1].value

        for t in tokens:
            if t.token_type == TokenType.END_OF_LINE:
                continue

            if t.value[0] != '.':
                raise InvalidTokenError(
                    'Only directives are allowed at the top level of a class.',
                    token=t
                )

            if t.value[1:] == 'end':
                tokens.get_line()
                return

            try:
                parser_class, allowed_in = DIRECTIVES[t.value[1:]]
            except KeyError:
                raise UnknownDirectiveError(
                    f'Don\'t know how to handle {t.value[1:]!r}.',
                    token=t
                )

            if self.__class__.__name__ not in allowed_in:
                raise ParserError(
                    f'Directive {t.value[1:]!r} not allowed here.',
                    token=t
                )

            node = parser_class(self, line_no=t.line_no)
            node.parse_from_tokens(tokens)


@directive(allowed_in={'Class'})
class Super(Node):
    __slots__ = ('descriptor',)

    def __init__(self, parent: 'Node'=None, *, line_no: int=0):
        super().__init__(parent=parent, line_no=line_no)
        self.descriptor = None

    def parse_from_tokens(self, tokens):
        self.descriptor = tokens.get_line()[0].value

    def __repr__(self):
        return f'<Super({self.descriptor})>'


@directive(allowed_in={'Class'})
class Method(Node):
    __slots__ = ('access_flags', 'descriptor')

    def __init__(self, parent: 'Node'=None, *, line_no: int=0):
        super().__init__(parent=parent, line_no=line_no)
        self.access_flags = None
        self.descriptor = None

    def parse_from_tokens(self, tokens):
        line = tokens.get_line()
        self.access_flags = [t.value for t in line[:-1]]
        self.descriptor = line[-1].value

        for t in tokens:
            if t.token_type == TokenType.END_OF_LINE:
                continue

            if t.value[0] == '.':
                if t.value[1:] == 'end':
                    tokens.get_line()
                    return

                try:
                    parser_class, allowed_in = DIRECTIVES[t.value[1:]]
                except KeyError:
                    raise UnknownDirectiveError(
                        f'Don\'t know how to handle {t.value[1:]!r}.',
                        token=t
                    )

                if self.__class__.__name__ not in allowed_in:
                    raise ParserError(
                        f'Directive {t.value[1:]!r} not allowed here.',
                        token=t
                    )

                node = parser_class(self, line_no=t.line_no)
                node.parse_from_tokens(tokens)
            else:
                # Return the opcode token before we start parsing it.
                tokens.put(t)
                Instruction(self, line_no=t.line_no).parse_from_tokens(tokens)


@directive(allowed_in={'Method'})
class Limit(Node):
    __slots__ = ('of_type', 'count')

    def __init__(self, parent: 'Node', *, line_no: int = 0):
        super().__init__(parent=parent, line_no=line_no)
        self.of_type = None
        self.count = None

    def parse_from_tokens(self, tokens):
        line = tokens.get_line()
        self.of_type = line[0].value
        self.count = literal_eval(line[1].value)

    def __repr__(self):
        return f'<Limit({self.of_type!r}, {self.count})>'


class Instruction(Node):
    __slots__ = ('opcode', 'operands')

    def __init__(self, parent: 'Node', *, line_no: int = 0):
        super().__init__(parent=parent, line_no=line_no)
        self.opcode = None
        self.operands = None

    def parse_from_tokens(self, tokens):
        line = tokens.get_line()
        self.opcode = line[0].value
        if len(line) > 1:
            self.operands = [t.value for t in line[1:]]

    def __repr__(self):
        return f'<Instruction({self.opcode!r}, {self.operands!r})>'


class TokenReader(object):
    def __init__(self, tokens: Iterator[Token], ignore_comments=True):
        """
        A convience wrapper around a stream of Tokens.

        :param tokens: Any iterator of Token objects.
        :param ignore_comments: Do not yield tokens of type COMMENT.
                                [default: True]
        """
        #: The token iterator.
        self.tokens = tokens
        self.put_back: List[Token] = []
        self.ignore_comments = ignore_comments

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            t = self.put_back.pop() if self.put_back else next(self.tokens)
            if self.ignore_comments and t.token_type == TokenType.COMMENT:
                continue
            return t

    def put(self, token: Token):
        """Return a Token to to the front of the stream.

        :param token: The token to prepend.
        """
        self.put_back.append(token)

    def take_until(self, f, inclusive=False, put_back=False):
        """Consume and yield Token from the stream until the condition
        `f` is reached.

        :param f: Any callable that will be passed the current Token.
        :param inclusive: Include the token that caused iteration to stop.
                          [default: False]
        :param put_back: Return the token that caused iteration to stop
                         to the stream. [default: False]
        """
        for token in self:
            if f(token):
                if not inclusive:
                    if put_back:
                        self.put(token)
                    return
                yield token
                return
            yield token

    def get_line(self):
        """Consume and return a list of tokens on the current line, excluding
        the EOL itself.
        """
        return list(self.take_until(
            lambda t: t.token_type == TokenType.END_OF_LINE
        ))


def parse(tokens: Iterator[Token]) -> Node:
    """
    Parse an iterable of Tokens to produce a tree with structured information
    and additional typing.

    :param tokens: An iterable of tokenizer tokens.
    :return: The root node.
    """
    root = Root()
    root.parse_from_tokens(TokenReader(tokens))
    return root
