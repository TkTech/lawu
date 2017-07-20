# -*- coding: utf-8 -*-
import os.path

import pytest

from jawa.cf import ClassFile


@pytest.fixture
def cf():
    sample_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'HelloWorldDebug.class'
    )

    with open(sample_path, 'rb') as fin:
        cf = ClassFile(fin)
        yield cf


def test_exceptions_read(cf):
    m = cf.methods.find_one(name='main')
    a = m.code.attributes.find_one(name='LineNumberTable')

    assert len(a.line_no) == 2

    assert a.line_no[0] == (0, 3)
    assert a.line_no[1] == (8, 4)


def test_exceptions_write(cf):
    m = cf.methods.find_one(name='main')
    a = m.code.attributes.find_one(name='LineNumberTable')

    assert a.info == b'\x00\x02\x00\x00\x00\x03\x00\x08\x00\x04'
