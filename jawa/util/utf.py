def decode_modified_utf8(s):
    """
    Parses a bytestring containing modified UTF-8 as defined in section
    4.4.7 of the JVM specification.

    :param s: bytestring to be converted.
    :returns: A unicode representation of the original string.
    """
    s = bytearray(s)
    final_string = unicode()
    ix = 0
    while ix < len(s):
        x = s[ix]
        ix += 1

        if x >> 7 == 0:
            # Just an ASCII character, nothing else to do.
            pass
        elif x >> 6 == 6:
            y = s[ix]
            ix += 1
            x = ((x & 0x1F) << 6) + (y & 0x3F)
        elif x >> 4 == 14:
            y, z = s[ix:ix+2]
            ix += 2
            x = ((x & 0xF) << 12) + ((y & 0x3F) << 6) + (z & 0x3F)
        elif x == 0xED:
            v, w, x, y, z = s[ix:ix+5]
            ix += 5
            x = 0x10000 + (
                ((v & 0x0F) << 16)
                + ((w & 0x3F) << 10)
                + ((y & 0x0F) << 6)
                + (z & 0x3F)
            )

        final_string += unichr(x)
    return final_string
