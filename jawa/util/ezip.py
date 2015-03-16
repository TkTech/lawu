# -*- coding: utf8 -*-
import re

# czipfile offers a noticable improvement, especially when working with
# many smaller files.
try:
    from czipfile import ZipFile
except ImportError:
    from zipfile import ZipFile

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import BytesIO
        StringIO = BytesIO


class EditableZipFile(object):
    def __init__(self, io=None):
        """
        A light wrapper around the python :py:class:`zipfile.ZipFile` that
        enables in-memory modification.

        If `io` is provided, its contents are loaded. `io` may be a file-system
        path or a file-like object.
        """
        self.io = ZipFile(io, 'r') if io else None
        self._cache = {}
        # The ZipFile namelist() appears to re-scan on each call. Keeping track
        # ourselves more than halves iteration times.
        self._namelist = set(self.io.namelist() if io else ())
        self._o_namelist = frozenset(self._namelist)

    @property
    def namelist(self):
        """
        Returns a list of all paths in this ZipFile.
        """
        return self._namelist

    def read(self, path):
        """
        Returns the contents of `path` if it exists, returning `None` if it
        does not.
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
        Saves the ZipFile to `path`, which can be a file-system path or a
        file-like object.
        """
        zp_out = ZipFile(path, 'w')
        for zp_name in self._namelist:
            zp_out.writestr(zp_name, self.read(zp_name))
        zp_out.close()

    def remove(self, path):
        """
        Removes a file from the ZipFile.
        """
        self._namelist.discard(path)
        self._cache.pop(path, None)

    def open(self, path, mode='r'):
        if mode == 'r':
            return StringIO(self.read(path))
        elif mode == 'w':
            out = StringIO()

            class ctx(object):
                def __enter__(self_):
                    return out

                def __exit__(self_, *exc_info):
                    self.write(path, out.getvalue())
                    out.close()

            return ctx()
        else:
            raise ValueError('expected r or w')

        class ctx(object):
            def __enter__(self):
                return self

            def __exit__(self, *exc_info):
                pass

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        """
        Closes the ZipFile and any underlying objects.
        """
        if self.io:
            self.io.close()

    def regex(self, regex):
        """
        Returns an iterator over every path that matches `regex`.
        """
        for p in self._namelist:
            if re.match(regex, p):
                yield p

    def directory_tree(self):
        """
        Returns a (potentially multilevel) dict representing the file
        hierarchy.
        """
        root = {}

        # Sort the paths by depth with the shortest occuring first.
        paths = [p.split('/') for p in self.namelist]
        paths.sort(key=lambda x: len(x))

        for path in paths:
            complete_path = '/'.join(path)

            path_root = root
            while len(path) > 1:
                path_part = path.pop(0)
                path_root = path_root.setdefault(path_part, {})
            path_root[path[0]] = complete_path

        return root

    close = __exit__
