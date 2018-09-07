from enum import Enum
from typing import Any, TextIO, Iterator, Union


class States(Enum):
    GENERIC = 1
    QUOTED_STRING = 2
    DIRECTIVE = 3
    COMMENT = 4
    LITERAL = 5
    QUOTED_ESCAPE = 6


class Token(object):
    __slots__ = ('token_type', 'value', 'line_no')

    def __init__(self, *, token_type=None, value=None, line_no=None):
        self.token_type: int = token_type or States.GENERIC
        self.value: Any = value
        self.line_no: Union[int, None] = line_no

    def __repr__(self):
        return (
            f'TokenType(token_type={self.token_type!r}, '
            f'value={self.value!r}, '
            f'line_no={self.line_no!r})'
        )


def tokenize(source: TextIO) -> Iterator[Token]:
    """
    Tokenize a Jasmin source file, yield an stream of Tokens.

    :param source: Source to read from.
    :return: Iterator of Token objects.
    """
    s = States.GENERIC
    c = source.read(1)
    v = []
    line_no = 1
    while c is not None and c != '':
        if s == States.GENERIC:
            # Start of a directive.
            if c == '.':
                s = States.DIRECTIVE
            elif c == ';':
                s = States.COMMENT
            elif c in (' ', '\t', '\n'):
                value = ''.join(v)
                if value:
                    yield Token(token_type=s, value=value, line_no=line_no)
                s = States.GENERIC
                del v[:]
            elif c in '"':
                s = States.QUOTED_STRING
            else:
                v.append(c)
        elif s == States.COMMENT:
            if c == '\n':
                value = ''.join(v)
                if value:
                    yield Token(token_type=s, value=value, line_no=line_no)
                s = States.GENERIC
                del v[:]
            elif not v and c in (' ', '\t'):
                # Skip starting whitespace on comments.
                pass
            else:
                v.append(c)
        elif s == States.DIRECTIVE:
            if c in (' ', '\t', '\n'):
                yield Token(token_type=s, value=''.join(v), line_no=line_no)
                s = States.GENERIC
                del v[:]
            else:
                v.append(c)
        elif s == States.QUOTED_STRING:
            if c == '\\':
                s = States.QUOTED_ESCAPE
            elif c == '"':
                yield Token(token_type=s, value=''.join(v), line_no=line_no)
                s = States.GENERIC
                del v[:]
            else:
                v.append(c)
        elif s == States.QUOTED_ESCAPE:
            s = States.QUOTED_STRING
            v.append(c)
            if c == '\\':
                s = States.QUOTED_ESCAPE

        if c == '\n':
            line_no += 1

        c = source.read(1)
