import os.path
import shutil
import tempfile
import zipfile

from lawu.cf import ClassFile
from lawu.classloader import ClassLoader


def test_load_from_class():
    """Ensure we can add ClassFile's directly to the ClassLoader."""
    cl = ClassLoader()

    cf = ClassFile()
    cf.this = 'TestClass'
    cl.update(cf)

    assert cl.load('TestClass') is cf


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
