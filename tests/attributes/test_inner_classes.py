from jawa.attributes.inner_classes import InnerClass


def test_inner_classes_read(loader):
    cf = loader['InnerClasses']
    a = cf.attributes.find_one(name='InnerClasses')
    assert a.inner_classes == [
        InnerClass(
            inner_class_info_index=4,
            outer_class_info_index=2,
            inner_name_index=5,
            inner_class_access_flags=2
        )
    ]


def test_exceptions_write(loader):
    cf = loader['InnerClasses']
    a = cf.attributes.find_one(name='InnerClasses')
    assert a.pack() == b'\x00\x01\x00\x04\x00\x02\x00\x05\x00\x02'
