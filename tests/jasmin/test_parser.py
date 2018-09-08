import pytest
from io import StringIO

from jawa.jasmin.errors import InvalidTokenError, UnknownDirectiveError
from jawa.jasmin.tokenizer import tokenize
from jawa.jasmin.ast import parse


def test_top_level():
    """
    Only directives are allowed at the top level, stray literal values
    will cause an error, but not comments.
    """
    tokens = tokenize(StringIO(
        '; Top Level\n'
        'literal_value'
    ))
    with pytest.raises(InvalidTokenError) as ex:
        parse(tokens)
    assert ex.value.token.line_no == 1


def test_unknown_directives():
    """
    Ensure we error out when unknown directives are encountered.
    """
    tokens = tokenize(StringIO(
        '.unknown_directive'
    ))
    with pytest.raises(UnknownDirectiveError):
        parse(tokens)

    tokens = tokenize(StringIO(
        '.method public <init>()V\n'
        '\t.unknown_directive\n'
        '.end method'
    ))
    with pytest.raises(UnknownDirectiveError):
        parse(tokens)
