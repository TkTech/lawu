from jawa.cf import ClassFile
from jawa.attributes.synthetic import SyntheticAttribute


def test_synthetic_read(loader):
    """
    Ensure we can read a Synthetic generated by javac.
    """
    cf = loader['InnerClasses$InnerClass']
    field = cf.fields.find_one(name='this$0')
    synthetic = field.attributes.find_one(name='Synthetic')
    assert synthetic is not None


def test_synthetic_write():
    """
    Ensure Synthetic can be written and read back.
    """
    cf_one = ClassFile.create('Synthetic')
    syn = cf_one.attributes.create(SyntheticAttribute)
    assert syn.pack() == b''
