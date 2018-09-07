from io import StringIO

from jawa.jasmin.tokenizer import tokenize, States


def test_quoted_string():
    tokens = list(tokenize(
        StringIO('"No Escapes"')
    ))
    assert len(tokens) == 1
    assert tokens[0].token_type == States.QUOTED_STRING
    assert tokens[0].value == 'No Escapes'
    assert tokens[0].line_no == 1

    tokens = list(tokenize(
        StringIO('"Escaped \\"Quote"')
    ))
    assert len(tokens) == 1
    assert tokens[0].token_type == States.QUOTED_STRING
    assert tokens[0].value == 'Escaped \"Quote'
    assert tokens[0].line_no == 1
