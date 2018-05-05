def test_exceptions_read(loader):
    cf = loader['ExceptionsTest']

    m = cf.methods.find_one(name='test')
    a = m.attributes.find_one(name='Exceptions')

    assert len(a.exceptions) == 1

    assert cf.constants[a.exceptions[0]].name.value == \
        u'java/lang/IndexOutOfBoundsException'


def test_exceptions_write(loader):
    cf = loader['ExceptionsTest']

    m = cf.methods.find_one(name='test')
    a = m.attributes.find_one(name='Exceptions')

    assert a.pack() == b'\x00\x01\x00\x0A'

    a.exceptions.append(
        cf.constants.create_class(
            name=u'java/lang/TestException'
        ).index
    )

    assert a.pack() == b'\x00\x02\x00\x0A\x00\x12'
