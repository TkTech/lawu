__all__ = ('Flags',)
import struct


class Flags(object):
    """
    Convenience class for handling bit flags.
    """
    def __init__(self, binary_format, flags):
        object.__setattr__(self, 'binary_format', binary_format)
        object.__setattr__(self, 'flags', flags)
        object.__setattr__(self, '_value', 0)
        object.__setattr__(self, '_cache', struct.Struct(binary_format))

    def pack(self):
        """
        A shortcut for `struct.pack(flag.binary_format, flag.value)`.
        """
        return self._cache.pack(self.value)

    @property
    def value(self):
        """
        The numeric value of the bitfield.
        """
        return self._value

    def unpack(self, source):
        """
        A shortcut for `struct.unpack(flag.binary_format, <bytes>)`.
        """
        self._value = self._cache.unpack(source)[0]

    def get(self, name):
        """
        Returns the value of the field `name`.
        """
        return bool(self.flags[name] & self.value)

    def set(self, name, value):
        """
        Sets the value of the field `name` to `value`, which is `True` or
        `False`.
        """
        flag = self.flags[name]
        self._value = (self.value | flag) if value else (self.value & ~flag)

    def __getattr__(self, attr):
        if attr not in self.flags:
            return object.__getattr__(self, attr)
        return self.get(attr)

    def __setattr__(self, attr, value):
        if attr not in self.flags:
            return object.__setattr__(self, attr, value)
        self.set(attr, value)

    def to_dict(self):
        """
        Returns this `Flags` object's fields as a dictionary.
        """
        return dict((k, self.get(k)) for k in self.flags.keys())
