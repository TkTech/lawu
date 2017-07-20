# -*- coding: utf-8 -*-
import os.path

import pytest

from jawa.cf import ClassFile
from jawa.util.verifier import VerificationTypes


@pytest.fixture
def cf():
    sample_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'ArrayTest.class'
    )

    with open(sample_path, 'rb') as fin:
        cf = ClassFile(fin)
        yield cf


def test_stack_map_table_read(cf):
    m = cf.methods.find_one(name='addOne')
    a = m.code.attributes.find_one(name='StackMapTable')

    assert len(a.frames) == 2

    assert a.frames[0].frame_type == 76
    assert a.frames[0].frame_stack == [
        (VerificationTypes.ITEM_Integer,)
    ]

    assert a.frames[1].frame_type == 255
    assert a.frames[1].frame_stack == [
        (VerificationTypes.ITEM_Integer,),
        (VerificationTypes.ITEM_Integer,)
    ]
    assert a.frames[1].frame_locals == [
        (VerificationTypes.ITEM_Object, 17),
        (VerificationTypes.ITEM_Integer,)
    ]
