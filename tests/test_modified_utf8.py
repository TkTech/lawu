#!/usr/bin/env python
# encoding: utf-8
import os

from jawa import ClassFile


def test_decode_modified_utf8():
    """
    JVM ClassFile's use a "modified" form of UTF8 which cannot always be
    parsed by python's UTF-8 decoder.
    """
    sample_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'ModifiedUTF8.class'
    )

    with open(sample_path, 'rb') as fin:
        # We simply need to make sure no encoding exceptions are raised
        # when we parse the ClassFile.
        ClassFile(fin)
