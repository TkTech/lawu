# -*- coding: utf8 -*-
"""
Tools for working with JVM `.jar` archives, which are simply ZIP archives with
some mandatory structure.

.. note::
    If `czipfile <http://pypi.python.org/pypi/czipfile>`_ is available,
    decompression will be noticably faster.
"""
import re

# czipfile offers a noticable improvement, especially when working with
# many smaller files.
try:
    from czipfile import ZipFile
except ImportError:
    from zipfile import ZipFile


class JarFile(object):
    """
    A light wrapper around the python :py:class:`zipfile.ZipFile` that
    enables in-memory modification.

    If `io` is provided, its contents are loaded. `io` may be a file-system
    path or a file-like object.

    As of 0.1.0, :py:class:`jawa.util.jf.JarFile` is also a context manager.

    >>> from jawa.util.jf import JarFile
    >>> with JarFile(sys.argv[1]) as jf:
    ...    print(jf.namelist())
    """
    def __init__(self, io=None):
        self.io = ZipFile(io, 'r') if io else None
        self._cache = {}
        # The ZipFile namelist() appears to re-scan on each call. Keeping track
        # ourselves more than halves iteration times.
        self._namelist = set(self.io.namelist() if io else ())
        self._o_namelist = frozenset(self._namelist)

    def namelist(self):
        """
        Returns a list of all paths in this JarFile.
        """
        return self._namelist

    def read(self, path):
        """
        Returns the contents of `path`, if it exists, otherwise `None`.
        """
        if path not in self._namelist:
            return None
        elif path in self._cache:
            return self._cache[path]
        elif self.io and path in self._o_namelist:
            return self.io.read(path)
        return None

    def write(self, path, data):
        """
        Writes `data` to `path`, overwritting any existing content.
        """
        # TODO: Evaluate using tempfile.TemporarySpooledFile to better support
        #       large files.
        self._cache[path] = data
        self._namelist.add(path)

    def save(self, path):
        """
        Saves the JarFile to `path`, which can be a file-system path or a
        file-like object.
        """
        zp_out = ZipFile(path, 'w')
        for zp_name in self._namelist:
            zp_out.writestr(zp_name, self.read(zp_name))
        zp_out.close()

    def remove(self, path):
        """
        Removes a file from the JarFile.

        >>> print jf.namelist()
        ['my_file.txt', 'that_other_file.txt', ...]
        >>> jf.remove('my_file.txt')
        >>> print jf.namelist()
        ['that_other_file.txt', ...]
        """
        self._namelist.discard(path)
        self._cache.pop(path, None)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        """
        Closes the JarFile and any underlying objects.
        """
        if self.io:
            self.io.close()

    def regex(self, regex):
        """
        Returns an iterator over every path that matches `regex`. For example,
        to get all files ending in .class that aren't in a sub-directory:

        >>> for path in jf.regex('[^/]+\.class'):
        ...    print(path)
        """
        return (p for p in self._namelist if re.match(regex, p))

    close = __exit__
