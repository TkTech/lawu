from jawa.util.utf import encode_modified_utf8, decode_modified_utf8


def test_decode_modified_utf8(loader):
    """
    JVM ClassFile's use a "modified" form of UTF8 which cannot always be
    parsed by python's UTF-8 decoder.

    We simply need to make sure no encoding exceptions are raised
    when we parse the sample ClassFile.
    """
    loader.load('ModifiedUTF8')


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
    pairs = (
        (u'1\x002', b'\x31\xc0\x80\x32'),
        (u'\uD801\uDC00', b'\xed\xa0\x81\xed\xb0\x80')
    )
    for original, encoded in pairs:
        assert encode_modified_utf8(original) == encoded


def test_decode_utf8_1():
    """
    Counterpart of test_encode_utf8_1.

    Tests decoding of some special cases:
        1 - c080 must be decoded as byte 00
        2 - eda081edb080 must be decoded as \uD801\uDC00 (representing U+10400)
    """
    pairs = (
        (b'\x31\xc0\x80\x32', '1\x002'),
        (b'\xed\xa0\x81\xed\xb0\x80', '\uD801\uDC00')
    )

    for original, decoded in pairs:
        assert decode_modified_utf8(original) == decoded
