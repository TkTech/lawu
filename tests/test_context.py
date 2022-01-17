from lawu.cf import ClassFile
from lawu.constants import ConstantPool, ConstantClass


def test_context_implicit_pool():
    """
    Ensure that when a ClassFile context is active, it's used by any
    constants created without an explicit pool.
    """
    cf = ClassFile()
    with cf:
        auto_const = ConstantClass(name='ImplicitConstant')
        assert auto_const.pool is cf.constants
        assert auto_const.name.pool is cf.constants


def test_context_explicit_pool():
    """
    Ensure that when specifying an explicit ConstantPool, an active ClassFile
    context does not affect it.
    """
    cf = ClassFile()
    with cf:
        explicit_pool = ConstantPool()
        explicit_const = ConstantClass(
            name='ExplicitConstant',
            pool=explicit_pool
        )

        assert explicit_const.pool is explicit_pool
        assert explicit_const.name.pool is explicit_pool
