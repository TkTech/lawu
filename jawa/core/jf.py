# -*- coding: utf8 -*-
"""
Tools for working with JVM `.jar` archives, which are simply ZIP archives with
some mandatory structure.

.. note::
    If `czipfile <http://pypi.python.org/pypi/czipfile>`_ is available,
    decompression will be noticably faster.
"""
from jawa.util.ezip import EditableZipFile
from jawa.core.cf import ClassFile


class JarFile(EditableZipFile):
    """
    Provides Jawa-specific helpers around EditableZipFile.

    As of 0.1.0, :py:class:`jawa.util.jf.JarFile` is also a context manager.

    >>> from jawa.util.jf import JarFile
    >>> with JarFile(sys.argv[1]) as jf:
    ...    print(jf.namelist())
    """
    def open_class(self, path):
        """
        Return's a :py:class:`jawa.core.cf.ClassFile` for the given `path`.
        """
        return ClassFile.from_str(self.read(path))

    def all_classes(self):
        """
        An iterator that yields a :py:class:`jawa.core.cf.ClassFile` for each
        path ending in `.class` in this JarFile.
        """
        # About 10ms faster for 1028 files than using self.regex()
        for path in (p for p in self.namelist if p.endswith('.class')):
            yield ClassFile.from_str(self.read(path))
