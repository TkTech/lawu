from lawu.constants import FieldReference
from lawu.transforms import expand_constants


def test_expand_constants(loader):
    cf = loader['HelloWorld']
    main = cf.methods.find_one(name='main')
    ins = list(main.code.disassemble(transforms=[expand_constants]))
    assert isinstance(ins[0].operands[0], FieldReference)
