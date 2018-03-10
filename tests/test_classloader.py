from jawa.cf import ClassFile
from jawa.util.classloader import ClassLoader
from jawa.transforms.simple_swap import simple_swap
from jawa.assemble import assemble


def test_load_from_class():
    """Ensure we can add ClassFile's directly to the ClassLoader."""
    cl = ClassLoader()

    cf = ClassFile.create('TestClass')
    cl.update(cf)

    assert cl.load('TestClass') is cf


def test_default_bytecode_transforms():
    cl = ClassLoader(bytecode_transforms=[simple_swap])

    cf = ClassFile.create('TestClass')
    cl.update(cf)

    test_method = cf.methods.create('test', '(V)V;', code=True)
    test_method.code.max_stack = 2
    test_method.code.max_locals = 0

    test_method.code.assemble(assemble([
        ('iconst_0',),
        ('pop',),
        ('return',)
    ]))

    # Load from the ClassLoader to bind to it.
    cf = cl.load('TestClass')

    # Ensure the defaults apply.
    ins_iter = test_method.code.disassemble()
    ins = next(ins_iter)
    assert ins.mnemonic == 'bipush'
    assert len(ins.operands) == 1
    assert ins.operands[0].value == 0

    # Ensure we can override the default.
    ins_iter = test_method.code.disassemble(transforms=[])
    ins = next(ins_iter)
    assert ins.mnemonic == 'iconst_0'
    assert len(ins.operands) == 0
