# -*- coding: utf8 -*-
import os

from jawa.core.jf import JarFile


class Context(object):
    """
    A :class:`~jawa.core.context.Context` object exists to mimic the Java
    CLASSPATH and other environment flags & settings.
    """
    def __init__(self):
        self._classpath = set()

    @property
    def classpath(self):
        """
        Returns a list of the currently active classpaths, which may be a
        filesystem path (as a str) or a :class:`~jawa.core.jf.JarFile`.
        """
        return list(self._classpath)

    def add_classpath(self, path_or_jar):
        """
        Adds a new classpath to the current
        :class:`~jawa.core.context.Context`. The path may be a literal
        filesystem path, or an in-memory :class:`~jawa.core.jf.JarFile`.
        """
        self._classpath.add(path_or_jar)

    def find_class(self, class_, no_inherit=False):
        """
        Searches for the given class in the active classpath, returning a
        :class:`~jawa.core.cf.ClassFile` object or ``None`` if it was not
        found.
        """
        if not class_.endswith('.class'):
            class_ = '{}.class'.format(class_)

        for path in self.classpath:
            if isinstance(path, JarFile):
                if class_ in path.namelist:
                    return path.open_class(
                        class_, context=None if no_inherit else self)
                continue
            elif os.path.isfile(path) and path.endswith('.jar'):
                raise NotImplementedError()
            elif os.path.isfile(path):
                raise ValueError('not a directory or a JAR')
            elif os.path.isdir(path):
                raise NotImplementedError()

        return None
