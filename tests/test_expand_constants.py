from jawa.constants import FieldReference
from jawa.transforms import expand_constants


def test_expand_constants(loader):
    cf = loader['HelloWorld']
    main = cf.methods.find_one(name='main')
    ins = list(main.code.disassemble(transforms=[expand_constants]))
    assert isinstance(ins[0].operands[0], FieldReference)
