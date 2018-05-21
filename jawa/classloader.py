import io
import os
import os.path
from typing import IO, Callable, Iterable, Set, Iterator
from itertools import repeat
from zipfile import ZipFile
from collections import OrderedDict
from contextlib import contextmanager

from jawa.cf import ClassFile
from jawa.constants import ConstantPool, ConstantClass


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

    :param sources: Optional sources to pass into update().
    :param max_cache: The maximum number of ClassFile's to store in the cache.
                      If set to 0, the cache will be unlimited. [default: 50]
    :type max_cache: Long
    :param klass: The class to use when constructing ClassFiles.
    :type klass: ClassFile or subclass.
    :param bytecode_transforms: Default transforms to apply when disassembling
                                a method.
    """
    def __init__(self, *sources, max_cache: int=50, klass=ClassFile,
                 bytecode_transforms: Iterable[Callable]=None):
        self.path_map = {}
        self.max_cache = max_cache
        self.class_cache = OrderedDict()
        self.bytecode_transforms = bytecode_transforms or []
        self.klass = klass

        if sources:
            self.update(*sources)

    def __getitem__(self, path: str) -> ClassFile:
        return self.load(path)

    def __contains__(self, path: str) -> bool:
        if path in self.path_map:
            return True
        elif path + '.class' in self.path_map:
            return True
        return False

    def update(self, *sources, follow_symlinks: bool=False,
               maximum_depth: int=20):
        """Add one or more ClassFile sources to the class loader.

        If a given source is a directory path, it is traversed up to the
        maximum set depth and all files under it are added to the class loader
        lookup table.

        If a given source is a .jar or .zip file it will be opened and the
        file index added to the class loader lookup table.

        If a given source is a ClassFile or a subclass, it's immediately
        added to the class loader lookup table and the class cache.

        :param sources: One or more ClassFile sources to be added.
        :param follow_symlinks: True if symlinks should be followed when
                                traversing filesystem directories.
                                [default: False]
        :param maximum_depth: The maximum sub-directory depth when traversing
                              filesystem directories. If set to `None` no limit
                              will be enforced. [default: 20]
        """
        for source in sources:
            if isinstance(source, self.klass):
                self.path_map[source.this.name.value] = source
                self.class_cache[source.this.name.value] = source
                continue

            # Explicit cast to str to support Path objects.
            source = str(source)
            if source.lower().endswith(('.zip', '.jar')):
                zf = ZipFile(source, 'r')
                self.path_map.update(zip(zf.namelist(), repeat(zf)))
            elif os.path.isdir(source):
                walker = _walk(
                    source,
                    follow_links=follow_symlinks,
                    maximum_depth=maximum_depth
                )
                for root, dirs, files in walker:
                    for file_ in files:
                        path_full = os.path.join(root, file_)
                        path_suffix = os.path.relpath(path_full, source)
                        self.path_map[path_suffix] = path_full

    @contextmanager
    def open(self, path: str, mode: str='r') -> IO:
        """Open an IO-like object for `path`.

        .. note::

            Mode *must* be either 'r' or 'w', as the underlying objects
            do not understand the full range of modes.

        :param path: The path to open.
        :param mode: The mode of the file being opened, either 'r' or 'w'.
        """
        entry = self.path_map.get(path)
        if entry is None:
            raise FileNotFoundError()

        if isinstance(entry, str):
            with open(entry, 'rb' if mode == 'r' else mode) as source:
                yield source
        elif isinstance(entry, ZipFile):
            yield io.BytesIO(entry.read(path))
        else:
            raise NotImplementedError()

    def load(self, path: str) -> ClassFile:
        """Load the class at `path` and return it.

        Load will attempt to load the file at `path` and `path` + .class
        before failing.

        :param path: Fully-qualified path to a ClassFile.
        """
        # Try to refresh the class from the cache, loading it from disk
        # if not found.
        try:
            r = self.class_cache.pop(path)
        except KeyError:
            with self.open(f'{path}.class') as source:
                r = self.klass(source)

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

    def clear(self):
        """Erase all stored paths and all cached classes."""
        self.path_map.clear()
        self.class_cache.clear()

    def dependencies(self, path: str) -> Set[str]:
        """Returns a set of all classes referenced by the ClassFile at
        `path` without reading the entire ClassFile.

        This is an optimization method that does not load a complete ClassFile,
        nor does it add the results to the ClassLoader cache.

        :param path: Fully-qualified path to a ClassFile.
        """
        return set(c.name.value for c in self.search_constant_pool(
            path=path,
            type_=ConstantClass
        ))

    def search_constant_pool(self, *, path: str, **options):
        """Partially load the class at `path`, yield all matching constants
        from the ConstantPool.

        This is an optimization method that does not load a complete ClassFile,
        nor does it add the results to the ClassLoader cache.

        :param path: Fully-qualified path to a ClassFile.
        :param options: A list of options to pass into `ConstantPool.find()`
        """
        with self.open(f'{path}.class') as source:
            # Skip over the magic, minor, and major version.
            source.read(8)
            pool = ConstantPool()
            pool.unpack(source)
            yield from pool.find(**options)

    @property
    def classes(self) -> Iterator[str]:
        """Yield the name of all classes discovered in the path map."""
        yield from (
            c[:-6]
            for c in self.path_map.keys() if c.endswith('.class')
        )
