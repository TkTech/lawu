from struct import unpack

from jawa.core.attribs.attribute import Attribute


class SourceFileAttribute(Attribute):
    """
    Provides the name (and possibly path) of the file used to generate
    a class, useful for debugging purposes.
    """
    NAME = 'SourceFile'

    def __init__(self, class_file, name_i=None, sourcefile_i=None):
        super(SourceFileAttribute, self).__init__(class_file, name_i)
        self._sourcefile_i = sourcefile_i

    @property
    def sourcefile(self):
        """
        The raw blob of the attribute payload (the "info" field in
        the JVM specs).
        """
        return self._cf.constants.get(self._sourcefile_i)

    @classmethod
    def _load_from_io(cls, class_file, name_i, length, io):
        sourcefile_i = unpack('>H', io.read(2))[0]
        return SourceFileAttribute(class_file, name_i, sourcefile_i)
