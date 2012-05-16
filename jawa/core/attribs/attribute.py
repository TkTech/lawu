class Attribute(object):
    NAME = None

    def __init__(self, class_file, name_i=None):
        self._cf = class_file
        self._name_i = name_i

    @property
    def name(self):
        """The name of this attribute."""
        return self._cf.constants.get(self._name_i)

    @property
    def class_file(self):
        """
        The :py:class:`jawa.core.cf.ClassFile` associated with this
        ``Attribute``.
        """
        return self._cf

    @classmethod
    def _load_from_io(cls, class_file, name_i, length, io):
        """Load the attribute from the file-like object `io`."""
        raise NotImplementedError()
