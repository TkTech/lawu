class Attribute(object):
    """
    The base attribute. All other attributes must subclass ``Attribute``.

    .. Note:
        This is not the default attribute, which is provided by
        :py:class:`jawa.core.attribs.unknown.UnknownAttribute`.
    """
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
        """
        Load the attribute from the file-like object `io`. All of `length`
        bytes must be consumed, or parsing the class will fail.
        """
        raise NotImplementedError()
