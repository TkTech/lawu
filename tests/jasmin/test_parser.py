import pytest
from io import StringIO

from jawa.jasmin.errors import InvalidTokenError, UnknownDirectiveError
from jawa.jasmin.tokenizer import tokenize
from jawa.jasmin.parser import parse, Method, TokenReader, Class, Root


def test_top_level():
    """
    Only directives are allowed at the top level, stray literal values
    will cause an error, but not comments.
    """
    tokens = tokenize(StringIO(
        '; Top Level\n'
        'literal_value'
    ))
    with pytest.raises(InvalidTokenError) as exc:
        parse(tokens)

    assert exc.value.token.value == 'literal_value'
    assert exc.value.token.line_no == 1


def test_unknown_directives():
    """
    Ensure we error out when unknown directives are encountered.
    """
    # Root-level directive.
    tokens = tokenize(StringIO(
        '.unknown_directive'
    ))
    with pytest.raises(UnknownDirectiveError):
        node = Root()
        node.parse_from_tokens(TokenReader(tokens))

    # Class-level directive.
    tokens = tokenize(StringIO(
        '.super java/lang/Object\n'
        '.unknown_directive'
    ))
    with pytest.raises(UnknownDirectiveError) as exc:
        node = Class()
        node.parse_from_tokens(TokenReader(tokens))

    assert exc.value.token.value == '.unknown_directive'
    assert exc.value.token.line_no == 1

    # Method-level directive.
    tokens = tokenize(StringIO(
        '.limit stack 2\n'
        '.unknown_directive\n'
    ))
    with pytest.raises(UnknownDirectiveError) as exc:
        node = Method()
        node.parse_from_tokens(TokenReader(tokens))

    assert exc.value.token.value == '.unknown_directive'
    assert exc.value.token.line_no == 1
