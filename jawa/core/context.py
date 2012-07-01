# -*- coding: utf8 -*-
import os

from jawa.core.jf import JarFile
from jawa.core.cf import ClassFile


class ContextPathError(Exception):
    def __init__(self, msg, path):
        super(ContextPathError, self).__init__(msg)
        self.path = path


class Context(object):
    """
    A :class:`~jawa.core.context.Context` object exists to mimic the Java
    CLASSPATH and other environment flags & settings.

    There are important performance considerations to make when using
    paths to ``.jar`` files. When doing a class lookup, paths ending in
    ``.jar`` will be substituded with a :class:`~jawa.core.jf.JarFile` object
    which will remain in memory until removed.
    """
    def __init__(self):
        self._classpath = []

    @property
    def classpath(self):
        """
        An iterator over the currently active classpaths.
        """
        return iter(self._classpath)

    def add_classpath(self, path_or_jar):
        """
        Adds a new classpath to the current
        :class:`~jawa.core.context.Context`. The path may be a:

        * filesystem path to a ``.jar`` file,
        * filesystem path to a directory,
        * an in-memory :class:`~jawa.core.jf.JarFile`.
        """
        if path_or_jar not in self._classpath:
            self._classpath.append(path_or_jar)

    def find_class(self, class_, no_inherit=False):
        """
        Searches for the given class in the active classpath, returning a
        :class:`~jawa.core.cf.ClassFile` object or ``None`` if it was not
        found.
        """
        if not class_.endswith('.class'):
            class_ = '{}.class'.format(class_)

        for i, path in enumerate(self._classpath):
            if isinstance(path, JarFile):
                if class_ in path.namelist:
                    return path.open_class(
                        class_, context=None if no_inherit else self)
            elif os.path.isfile(path) and path.endswith('.jar'):
                self._classpath[i] = JarFile(path)
                return self.find_class(class_, no_inherit=no_inherit)
            elif os.path.isdir(path):
                final_path = class_.replace('/', os.sep)
                final_path = os.join(path, final_path)
                if os.path.isfile(final_path):
                    return ClassFile(final_path)
            else:
                raise ContextPathError(
                    'path was not a .jar or a directory', path)

        # We couldn't find the class.
        return None
