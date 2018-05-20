def test_exceptions_read(loader):
    cf = loader['HelloWorldDebug']
    m = cf.methods.find_one(name='main')
    a = m.code.attributes.find_one(name='LineNumberTable')

    assert len(a.line_no) == 2

    assert a.line_no[0] == (0, 3)
    assert a.line_no[1] == (8, 4)


def test_exceptions_write(loader):
    cf = loader['HelloWorldDebug']
    m = cf.methods.find_one(name='main')
    a = m.code.attributes.find_one(name='LineNumberTable')

    assert a.pack() == b'\x00\x02\x00\x00\x00\x03\x00\x08\x00\x04'
