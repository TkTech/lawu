from jawa.cf import ClassFile
from jawa.constants import ConstantPool


def test_printable_constants():
    # Ensure we can successfully repr valid constants without crashing.
    pool = ConstantPool()
    repr(pool.create_utf8('HelloWorld'))
    repr(pool.create_class('HelloWorld'))
    repr(pool.create_double(1))
    repr(pool.create_float(1))
    repr(pool.create_integer(1))
    repr(pool.create_long(1))
    repr(pool.create_name_and_type('HelloWorld', 'I'))
    repr(pool.create_field_ref('HelloWorld', 'test', 'I'))
    repr(pool.create_method_ref('HelloWorld', 'test', 'I)V'))
    repr(pool.create_interface_method_ref(
        'HelloWorld',
        'test',
        'I)V'
    ))
    repr(pool.create_string('HelloWorld'))


def test_printable_classes():
    cf = ClassFile.create('HelloWorld')
    assert repr(cf) == '<ClassFile(this=\'HelloWorld\')>'
    assert repr(cf.version) == 'ClassVersion(major=50, minor=0)'
