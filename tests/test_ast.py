import pytest

from lawu import ast


def test_basic_equality():
    """Ensure simple hierarchy comparison works."""
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

    assert left == right
