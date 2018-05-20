"""
Utility methods for handling oddities in character encoding encountered
when parsing and writing JVM ClassFiles or object serialization archives.

.. note::

    http://bugs.python.org/issue2857 was an attempt in 2008 to get support
    for MUTF-8/CESU-8 into the python core.
"""


def decode_modified_utf8(s: bytes) -> str:
    """
    Decodes a bytestring containing modified UTF-8 as defined in section
    4.4.7 of the JVM specification.

    :param s: bytestring to be converted.
    :returns: A unicode representation of the original string.
    """
    s = bytearray(s)
    buff = []
    buffer_append = buff.append
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
            v, w, x, y, z = s[ix:ix+6]
            ix += 5
            x = 0x10000 + (
                ((v & 0x0F) << 16) +
                ((w & 0x3F) << 10) +
                ((y & 0x0F) << 6) +
                (z & 0x3F)
            )
        elif x == 0xC0 and s[ix] == 0x80:
            ix += 1
            x = 0
        buffer_append(x)
    return u''.join(chr(b) for b in buff)


def encode_modified_utf8(u: str) -> bytearray:
    """
    Encodes a unicode string as modified UTF-8 as defined in section 4.4.7
    of the JVM specification.

    :param u: unicode string to be converted.
    :returns: A decoded bytearray.
    """
    final_string = bytearray()

    for c in [ord(char) for char in u]:
        if c == 0x00 or (0x80 < c < 0x7FF):
            final_string.extend([
                (0xC0 | (0x1F & (c >> 6))),
                (0x80 | (0x3F & c))]
            )
        elif c < 0x7F:
            final_string.append(c)
        elif 0x800 < c < 0xFFFF:
            final_string.extend([
                (0xE0 | (0x0F & (c >> 12))),
                (0x80 | (0x3F & (c >> 6))),
                (0x80 | (0x3F & c))]
            )

    return final_string
