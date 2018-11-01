from ast import literal_eval
from typing import List, Iterator

from jawa import ast
from jawa.jasmin.tokenizer import Token, TokenType
from jawa.jasmin.errors import (
    InvalidTokenError,
    UnknownDirectiveError
)


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


class DirectiveProcessor(object):
    def parse_root(self, tokens):
        root = ast.Root()

        for t in tokens:
            if t.token_type == TokenType.END_OF_LINE:
                continue

            if t.value[0] != '.':
                raise InvalidTokenError(
                    'Only directives & comments are allowed at the top-level.',
                    token=t
                )

            try:
                parser = getattr(self, f'parse_{t.value[1:]}')
            except AttributeError:
                raise UnknownDirectiveError(
                    f'Don\'t know how to handle directives of type'
                    f' {t.value[1:]}.',
                    token=t
                )

            node = parser(tokens)
            node.parent = root

        return root

    @staticmethod
    def parse_bytecode(tokens):
        token = next(tokens)
        value = token.value.split('.')
        return ast.Bytecode(
            major=literal_eval(value[0]),
            minor=literal_eval(value[1]),
            line_no=token.line_no
        )

    def parse_class(self, tokens):
        line = tokens.get_line()

        class_ = ast.Class(
            descriptor=line[-1].value,
            access_flags=[t.value for t in line[:-1]],
            line_no=line[0].line_no
        )

        # We want to keep consuming tokens until we either reach the end of the
        # file or an explicit ".end class".
        for t in tokens:
            if t.token_type == TokenType.END_OF_LINE:
                continue

            if t.value[0] != '.':
                raise InvalidTokenError(
                    'Only directives are allowed at the top level of a class.',
                    token=t
                )

            # We've reached an explicit end-of-class, which is optional in a
            # file with just a single class.
            if t.value[1:] == 'end':
                end_what = next(tokens).value
                if end_what != 'class':
                    raise InvalidTokenError(
                        f'Expected ".end class", saw ".end {end_what}"'
                        f' instead.',
                        token=t
                    )

                return class_

            try:
                parser = getattr(self, f'parse_{t.value[1:]}')
            except AttributeError:
                raise UnknownDirectiveError(
                    f'Don\'t know how to handle directives of type'
                    f' {t.value[1:]}.',
                    token=t
                )

            node = parser(tokens)
            node.parent = class_

        # We reached the end of the token stream without finding an explicit
        # .end class.
        return class_

    @staticmethod
    def parse_super(tokens):
        token = next(tokens)
        return ast.Super(descriptor=token.value, line_no=token.line_no)

    @staticmethod
    def parse_limit(tokens):
        what = next(tokens)
        count = next(tokens)
        return ast.Limit(
            what=what.value,
            count=literal_eval(count.value),
            line_no=what.line_no
        )

    def parse_method(self, tokens):
        line = tokens.get_line()
        descriptor = line.pop().value

        method = ast.Method(
            descriptor=descriptor,
            access_flags=[t.value for t in line],
            line_no=line[0].line_no
        )

        for t in tokens:
            if t.token_type == TokenType.END_OF_LINE:
                continue

            v = t.value
            if v.startswith('.'):
                if v[1:] == 'end':
                    end_what = next(tokens).value
                    if end_what != 'method':
                        raise InvalidTokenError(
                            f'Expected ".end method", saw ".end {end_what}"'
                            f' instead.',
                            token=t
                        )

                    return method
                try:
                    parser = getattr(self, f'parse_{v[1:]}')
                except AttributeError:
                    raise UnknownDirectiveError(
                        f'Don\'t know how to handle directives of type'
                        f' {v[1:]!r}.',
                        token=t
                    )
                node = parser(tokens)
                node.parent = method
            elif v.endswith(':'):
                # This *should*(?) be okay, since a literal : should always
                # be illegal in a symbol unless it's a label.
                ast.Label(
                    name=v[:-1],
                    parent=method
                )
            else:
                line = tokens.get_line()
                ast.Instruction(
                    opcode=v,
                    operands=[t.value for t in line],
                    parent=method,
                    line_no=t.line_no
                )

        return method


def parse(tokens: Iterator[Token], processor=DirectiveProcessor) -> ast.Root:
    """
    Parse a stream of Tokens representing a Jasmin source file into the
    internal Jawa representation.

    :param tokens: An iterable of tokenizer tokens.
    :return: The root node.
    """
    return DirectiveProcessor().parse_root(TokenReader(tokens))
