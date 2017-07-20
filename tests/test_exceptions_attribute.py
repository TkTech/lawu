# -*- coding: utf-8 -*-
import os.path

import pytest

from jawa.cf import ClassFile


@pytest.fixture
def cf():
    sample_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'ExceptionsTest.class'
    )

    with open(sample_path, 'rb') as fin:
        cf = ClassFile(fin)
        yield cf


def test_exceptions_read(cf):
    m = cf.methods.find_one(name='test')
    a = m.attributes.find_one(name='Exceptions')

    assert len(a.exceptions) == 1

    assert cf.constants[a.exceptions[0]].name.value == \
        u'java/lang/IndexOutOfBoundsException'


def test_exceptions_write(cf):
    m = cf.methods.find_one(name='test')
    a = m.attributes.find_one(name='Exceptions')

    assert a.info == b'\x00\x01\x00\x0A'

    a.exceptions.append(
        cf.constants.create_class(
            name=u'java/lang/TestException'
        ).index
    )

    assert a.info == b'\x00\x02\x00\x0A\x00\x12'
