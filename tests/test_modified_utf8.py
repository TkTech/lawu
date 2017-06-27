#!/usr/bin/env python
# encoding: utf-8
import os

import binascii

from jawa import ClassFile
from jawa.util.utf import encode_modified_utf8, decode_modified_utf8


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


def test_encode_utf8_1():
    """
    Tests encoding of some special cases:
        1 - byte 00 must be encoded as 'c080'
        2 - supplementary characters (represented by the two surrogate code
        units of their UTF-16 representation): each surrogate must be encoded
        by three bytes. This means supplementary characters are represented by
        six bytes then U+10400 (represented as \uD801\uDC00) will be encoded as
        'eda081edb080'
    """
    # string containing byte 00
    str1 = u'1\x002'
    bb = encode_modified_utf8(str1)
    assert '31c08032' == binascii.hexlify(bb), binascii.hexlify(bb)

    # Unicode supplementary character U+10400
    str1 = u'\uD801\uDC00'
    bb = encode_modified_utf8(str1)
    assert 'eda081edb080' == binascii.hexlify(bb), binascii.hexlify(bb)


def test_decode_utf8_1():
    """
    Counterpart of test_encode_utf8_1.
    Tests decoding of some special cases:
        1 - c080 must be decoded as byte 00
        2 - eda081edb080 must be decoded as \uD801\uDC00 (representing U+10400)
    """
    str1 = '31c08032'
    str2 = decode_modified_utf8(binascii.unhexlify(str1))
    assert u'1\x002' == str2

    str1 = 'eda081edb080'
    str2 = decode_modified_utf8(binascii.unhexlify(str1))
    assert u'\uD801\uDC00' == str2
