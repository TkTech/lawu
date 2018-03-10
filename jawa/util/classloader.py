# -*- coding: utf-8 -*-
import io
import os
import os.path
import typing
from itertools import repeat
from zipfile import ZipFile
from collections import OrderedDict
from contextlib import contextmanager

from jawa.cf import ClassFile


def _walk(path, follow_links=False, maximum_depth=None):
    """A modified os.walk with support for maximum traversal depth."""
    root_level = path.rstrip(os.path.sep).count(os.path.sep)
    for root, dirs, files in os.walk(path, followlinks=follow_links):
        yield root, dirs, files
        if maximum_depth is None:
            continue

        if root_level + maximum_depth <= root.count(os.path.sep):
            del dirs[:]


class ClassLoader(object):
    """Emulate the Java ClassPath.

    Provides utilities for managing a java classpath as well as loading
    classes from those paths.

    :param follow_symlinks: True if symlinks should be followed when traversing
                            filesystem directories. [default: False]
    :type follow_symlinks: True
    :param maximum_depth: The maximum sub-directory depth when traversing
                          filesystem directories. If set to `None` no limit
                          will be enforced. [default: 20]
    :type maximum_depth: Long or None.
    :param max_cache: The maximum number of ClassFile's to store in the cache.
                      If set to 0, the cache will be unlimited. [default: 50]
    :type max_cache: Long
    :param klass: The class to use when constructing ClassFiles.
    :type klass: ClassFile or subclass.
    :param bytecode_transforms: Default transforms to apply when disassembling
                                a method.
    """
    def __init__(self, *, follow_symlinks: bool=False, maximum_depth: int=20,
                 max_cache: int=50, klass=ClassFile, bytecode_transforms=None):
        #: A mapping of all known classes to their source location.
        self.path_map = {}
        self.follow_symlinks = follow_symlinks
        self.maximum_depth = maximum_depth
        self.max_cache = max_cache
        self.class_cache = OrderedDict()
        self.klass = klass
        self.transforms = transforms or []

    def add_path(self, *paths):
        """Add a new path to the class loader.

        If the given `path` is a directory, it is traversed up to the maximum
        set depth and all files under it are added to the class loader lookup
        table.

        If the given `path` is a .jar or .zip file it will be opened and the
        file index added to the class loader lookup table.

        :param paths: Any number of paths to either a ZIP/JAR or a directory to
                      be added to the classpath.
        :type paths: unicode
        """
        for path in paths:
            # We're adding an archive to the classpath so we want to open it,
            # get the index, and unpack it into our path map.
            if path.lower().endswith(('.zip', '.jar')):
                zf = ZipFile(path, 'r')
                self.path_map.update(zip(zf.namelist(), repeat(zf)))
            elif os.path.isdir(path):
                walker = _walk(
                    path,
                    follow_links=self.follow_symlinks,
                    maximum_depth=self.maximum_depth
                )
                for root, dirs, files in walker:
                    for file_ in files:
                        path_full = os.path.join(root, file_)
                        path_suffix = os.path.relpath(path_full, path)
                        self.path_map[path_suffix] = path_full

    def load(self, path: str) -> ClassFile:
        """Load the class at `path` and return it.

        :param path: Fully-qualified path to a ClassFile.
        """
        try:
            full_path = self.path_map[path]
        except KeyError:
            raise FileNotFoundError()

        # Try to refresh the class from the cache, loading it from disk
        # if not found.
        try:
            r = self.class_cache.pop(path)
        except KeyError:
            # The entry in the path is an on-disk location.
            if isinstance(full_path, str):
                with open(full_path, 'rb') as fio:
                    r = self.klass(fio)
            else:
                # It's 2x as fast to read the entire file at once using
                # read and wrapping it in a StringIO then it is to just
                # ZipFile.open() it...
                with io.BytesIO(full_path.read(path)) as zip_in:
                    r = self.klass(zip_in)

        r.classloader = self
        # Even if it was found re-set the key to update the OrderedDict
        # ordering.
        self.class_cache[path] = r

        # If the cache is enabled remove every item over N started from
        # the least-used.
        if self.max_cache > 0:
            to_pop = max(len(self.class_cache) - self.max_cache, 0)
            for _ in repeat(None, to_pop):
                self.class_cache.popitem(last=False)

        return r

    @contextmanager
    def load_asset(self, path: str) -> typing.IO:
        """Load the asset at `path` and return a read-only file-like object.

        .. note::

            This method must always be used as a context manager to ensure file
            handles are closed properly.

        :param path: Fully-qualified path to an asset.
        """
        try:
            full_path = self.path_map[path]
        except KeyError:
            raise FileNotFoundError()

        if isinstance(full_path, str):
            with open(full_path, 'rb') as fio:
                yield fio
        else:
            with full_path.open(path, 'r') as fio:
                yield fio

    def clear(self):
        """Erase all stored paths and all cached classes."""
        self.path_map.clear()
        self.class_cache.clear()
