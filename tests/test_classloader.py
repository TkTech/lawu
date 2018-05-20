import os.path
import shutil
import tempfile
import zipfile

from jawa.cf import ClassFile
from jawa.classloader import ClassLoader
from jawa.transforms import simple_swap
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


def test_load_from_directory():
    """Ensure we can load a ClassFile from a simple directory."""
    with tempfile.TemporaryDirectory() as dir:
        shutil.copy(
            os.path.join(
                os.path.dirname(__file__),
                'data',
                'HelloWorld.class'
            ),
            dir
        )

        cl = ClassLoader()
        cl.update(dir)

        assert isinstance(cl.load('HelloWorld'), cl.klass)


def test_load_from_zipfile():
    """Ensure we can load a ClassFile from a ZipFile."""
    with tempfile.NamedTemporaryFile(suffix='.jar') as tmp:
        with zipfile.ZipFile(tmp, 'w') as zf:
            zf.write(
                os.path.join(
                    os.path.dirname(__file__),
                    'data',
                    'HelloWorld.class'
                ),
                arcname='HelloWorld.class'

            )

        cl = ClassLoader()
        cl.update(tmp.name)

        assert isinstance(cl.load('HelloWorld'), cl.klass)


def test_contains(loader):
    assert 'HelloWorld' in loader


def test_dependencies(loader):
    assert loader.dependencies('HelloWorld') == {
        'java/lang/Object',
        'java/io/PrintStream',
        'HelloWorld',
        'java/lang/System'
    }
