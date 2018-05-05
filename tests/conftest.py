from pathlib import Path

import pytest

from jawa.util.classloader import ClassLoader


@pytest.fixture()
def loader() -> ClassLoader:
    return ClassLoader(Path(__file__).parent / 'data')
