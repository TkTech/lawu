from io import StringIO

from jawa.jasmin.tokenizer import tokenize, TokenType


def test_quoted_string():
    tokens = list(tokenize(
        StringIO('"No Escapes"')
    ))
    assert len(tokens) == 2
    assert tokens[0].token_type == TokenType.QUOTED_STRING
    assert tokens[0].value == 'No Escapes'
    assert tokens[0].line_no == 1

    assert tokens[1].token_type == TokenType.END_OF_LINE

    tokens = list(tokenize(
        StringIO('"Escaped \\"Quote"')
    ))
    assert len(tokens) == 2
    assert tokens[0].token_type == TokenType.QUOTED_STRING
    assert tokens[0].value == 'Escaped \"Quote'
    assert tokens[0].line_no == 1

    assert tokens[1].token_type == TokenType.END_OF_LINE


def test_directive():
    tokens = list(tokenize(
        StringIO('.class public HelloWorld')
    ))
    assert len(tokens) == 4
    assert tokens[0].token_type == TokenType.DIRECTIVE
    assert tokens[0].value == 'class'
    assert tokens[0].line_no == 1

    assert tokens[1].token_type == TokenType.GENERIC
    assert tokens[1].value == 'public'
    assert tokens[1].line_no == 1

    assert tokens[2].token_type == TokenType.GENERIC
    assert tokens[2].value == 'HelloWorld'
    assert tokens[2].line_no == 1

    assert tokens[3].token_type == TokenType.END_OF_LINE


def test_comment():
    tokens = list(tokenize(
        StringIO('; Test Comment')
    ))
    assert len(tokens) == 2
    assert tokens[0].token_type == TokenType.COMMENT
    assert tokens[0].value == 'Test Comment'
    assert tokens[0].line_no == 1

    assert tokens[1].token_type == TokenType.END_OF_LINE


def test_semicolon_in_generic():
    tokens = list(tokenize(
        StringIO('abc;123')
    ))
    assert len(tokens) == 2
    assert tokens[0].token_type == TokenType.GENERIC
    assert tokens[0].value == 'abc;123'
    assert tokens[0].line_no == 1

    assert tokens[1].token_type == TokenType.END_OF_LINE
