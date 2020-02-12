from lawu.util.utf import encode_modified_utf8, decode_modified_utf8


def test_decode_encode_utf8():
    """
    Test encoding and decoding of Modified UTF8 (MUTF-8), a CESU-8 variant with
    modified 0x00 encoding.
    """
    pairs = (
        # Embedded NULL
        (b'\x31\xC0\x80\x32', '1\x002'),
        # "two-times-three" codepoint.
        (b'\xED\xA0\xBD\xED\xB8\x88', '\U0001F608'),
        # 2-byte codepoint.
        (b'\xC2\xB6', '\u00B6'),
        (b'\xE2\x82\xA3', '\u20A3')
    )

    for original, decoded in pairs:
        assert decode_modified_utf8(original) == decoded
        assert encode_modified_utf8(decoded) == original
