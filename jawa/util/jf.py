# -*- coding: utf8 -*-
import re

# czipfile offers a noticable improvement, especially when working with
# many smaller files.
try:
    from czipfile import ZipFile
except ImportError:
    from zipfile import ZipFile


class JarFile(object):
    """
    A light wrapper around the python ZipFile, that transparently adds
    in-memory editing of files. This is because ZipFile's extract is unsafe
    on almost all versions of Python, and does not support modifying an
    existing file.

    Saving generates a new JAR, saving any `write()`s made, and copying over
    any non-deleted files from the JAR given in `__init__`. Thus, if memory
    or performance are critical and you know you will only ever append,
    you may want to do this yourself.
    """
    def __init__(self, io=None):
        """
        Constructs a new JarFile, or loads an existing one if `io` is provided.
        `io` may be a file-system path or a file-like object.
        """
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
        return (p for p in self._namelist if re.match(regex, p))

    close = __exit__
