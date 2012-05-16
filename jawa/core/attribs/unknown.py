from jawa.core.attribs.attribute import Attribute


class UnknownAttribute(Attribute):
    """
    An unknown attribute (one whose name did not match the list
    of registered attributes) which cannot be parsed.
    """
    NAME = None

    def __init__(self, class_file, name_i=None, data=None):
        super(UnknownAttribute, self).__init__(class_file, name_i)
        self._data = data

    @property
    def data(self):
        """
        The raw blob of the attribute payload (the "info" field in
        the JVM specs).
        """
        return self._data

    @classmethod
    def _load_from_io(cls, class_file, name_i, length, io):
        return UnknownAttribute(class_file, name_i, data=io.read(length)[0])
