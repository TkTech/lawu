from enum import Enum
from typing import Any, TextIO, Iterator, Union


class TokenType(Enum):
    GENERIC = 1
    QUOTED_STRING = 2
    DIRECTIVE = 3
    COMMENT = 4
    LITERAL = 5
    QUOTED_ESCAPE = 6
    END_OF_LINE = 7


class Token(object):
    __slots__ = ('token_type', 'value', 'line_no')

    def __init__(self, *, token_type=None, value=None, line_no=None):
        self.token_type: int = token_type or TokenType.GENERIC
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
    s = TokenType.GENERIC
    c = source.read(1)
    prev_c = ''
    buff = []
    line_no = 1
    while c != '':
        if s in (TokenType.GENERIC, TokenType.DIRECTIVE):
            if c == '.':
                # We've found the start of a directive.
                s = TokenType.DIRECTIVE
            elif c == ';' and prev_c in (' ', '\t', '\n', ''):
                # We've found the start of a comment.
                s = TokenType.COMMENT
            elif c in (' ', '\t', '\n'):
                # We've found some whitespace, which acts as a terminator
                # in Jasmin. We don't care about blanks, so we only yield
                # if there's something in the buffer.
                value = ''.join(buff)
                if value:
                    yield Token(token_type=s, value=value, line_no=line_no)
                s = TokenType.GENERIC
                del buff[:]
            elif c in '"':
                # We've found the start of a quoted string and need to handle
                # escapes.
                s = TokenType.QUOTED_STRING
            else:
                buff.append(c)
        elif s == TokenType.COMMENT:
            if c == '\n':
                value = ''.join(buff)
                if value:
                    yield Token(token_type=s, value=value, line_no=line_no)
                s = TokenType.GENERIC
                del buff[:]
            elif not buff and c in (' ', '\t'):
                # Skip starting whitespace on comments.
                pass
            else:
                buff.append(c)
        elif s == TokenType.QUOTED_STRING:
            if c == '\\':
                # We've found the start of an escape, such as \".
                s = TokenType.QUOTED_ESCAPE
            elif c == '"':
                # We've found the end of the quoted string.
                yield Token(token_type=s, value=''.join(buff), line_no=line_no)
                s = TokenType.GENERIC
                del buff[:]
            else:
                buff.append(c)
        elif s == TokenType.QUOTED_ESCAPE:
            s = TokenType.QUOTED_STRING
            buff.append(c)
            if c == '\\':
                s = TokenType.QUOTED_ESCAPE

        if c == '\n':
            yield Token(token_type=TokenType.END_OF_LINE, line_no=line_no)
            # We keep track of what line we're currently tokenizing to use
            # later for useful error messages.
            line_no += 1

        prev_c = c
        c = source.read(1)

    # If tokenizing a subset, or if a file is missing the terminating
    # newline, then we yield whatever is leftover in the buffer. Probably
    # not correct.
    if buff:
        yield Token(token_type=s, value=''.join(buff), line_no=line_no)
    yield Token(token_type=TokenType.END_OF_LINE, line_no=line_no)
