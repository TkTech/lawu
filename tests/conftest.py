from pathlib import Path

import pytest

from jawa.util.classloader import ClassLoader


@pytest.fixture(scope='session')
def loader() -> ClassLoader:
    cl = ClassLoader()
    cl.update(str(Path(__file__).parent / 'data'))
    return cl
