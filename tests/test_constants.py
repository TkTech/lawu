from lawu.constants import ConstantPool, Double, Long, UTF8


def test_basics():
    """Ensure we can add & remove from the pool with proper state tracking."""
    pool = ConstantPool()

    # Simple add.
    pool.add(UTF8(value='test string'))

    assert pool.pool == {1: UTF8(value='test string')}

    # Ensure we can remove a simple constant.
    pool.remove(1)

    assert pool.pool == {}


def test_double():
    """Ensure we can add & remove double-width constants."""
    pool = ConstantPool()

    # Test adding double-width constants.
    pool.add(Double(value=5.5))
    pool.add(Long(value=6.6))

    assert pool.pool == {
        1: Double(value=5.5),
        2: None,
        3: Long(value=6.6),
        4: None
    }

    # Test adding double-width constant at specific index at the end of the
    # pool.
    pool.add(Double(value=7.7), index=6)

    assert pool.pool == {
        1: Double(value=5.5),
        2: None,
        3: Long(value=6.6),
        4: None,
        6: Double(value=7.7),
        7: None,
    }

    # Ensure adding a double-width constant doesn't fill in a single-size gap
    # that exists at slot 5.
    pool.add(Long(value=8.8))

    assert pool.pool == {
        1: Double(value=5.5),
        2: None,
        3: Long(value=6.6),
        4: None,
        6: Double(value=7.7),
        7: None,
        8: Long(value=8.8),
        9: None
    }
