import pytest

from lawu import ast


def test_same():
    """Ensure hierarchy comparison works."""
    left = ast.Class(
        descriptor=None,
        access_flags=['public'],
        children=[
            ast.Bytecode(major=0x33, minor=0x00),
            ast.Super(descriptor='java/lang/Object')
        ]
    )

    right = ast.Class(
        descriptor=None,
        access_flags=['public'],
        children=[
            ast.Bytecode(major=0x33, minor=0x00),
            ast.Super(descriptor='java/lang/Object')
        ]
    )

    assert left.same(right)


@pytest.mark.skip(reason='WIP')
def test_equality():
    """Ensure all Node subclasses implement equality checks."""
    def _subs(c):
        yield from c.__subclasses__()
        for results in (_subs(s) for s in c.__subclasses__()):
            yield from results

    for subclass in _subs(ast.Node):
        assert subclass.__eq__ is not object.__eq__, (
            f'{subclass.__name__} node does not implement equality'
        )
