def test_enclosing_method_read(loader):
    cf = loader['EnclosingMethod$1EnclosedClass']
    a = cf.attributes.find_one(name='EnclosingMethod')
    assert cf.constants[a.method_index].name.value == 'main'
    assert cf.constants[a.class_index].name.value == 'EnclosingMethod'


def test_exceptions_write(loader):
    cf = loader['EnclosingMethod$1EnclosedClass']
    a = cf.attributes.find_one(name='EnclosingMethod')
    assert a.pack() == b'\x00\x0b\x00\x0c'
