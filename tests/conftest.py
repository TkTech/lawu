from pathlib import Path

import pytest

from jawa.classloader import ClassLoader


@pytest.fixture(scope='session')
def loader() -> ClassLoader:
    return ClassLoader(Path(__file__).parent / 'data', max_cache=-1)
