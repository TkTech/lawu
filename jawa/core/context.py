# -*- coding: utf8 -*-
import os
import re

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

        In the case of a ``.jar`` file, it will be opened and replaced by a
        :class:`~jawa.core.jf.JarFile`.
        """
        if path_or_jar in self._classpath:
            pass
        elif isinstance(path_or_jar, JarFile):
            self._classpath.append(path_or_jar)
        elif os.path.isfile(path_or_jar) and path_or_jar.endswith('.jar'):
            self._classpath.append(JarFile(path_or_jar))
        else:
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
                # The path is a .jar file already opened in our container.
                if class_ in path.namelist:
                    return path.open_class(
                        class_,
                        context=None if no_inherit else self
                    )
            else:
                # The path is plain directory (usually an expanded .jar).
                final_path = class_.replace('/', os.sep)
                final_path = os.join(path, final_path)
                if os.path.isfile(final_path):
                    return ClassFile(
                        final_path,
                        context=None if no_inherit else self
                    )
        # We couldn't find the class.
        return None

    def all_classes(self, no_inherit=False):
        """
        Iterates over all classes available in the classpaths.

        .. warning:: The classpaths can contain many thousands of classes,
                     use this method sparingly.
        """
        for path in self._classpath:
            # We have a JarFile which supports this already, use it.
            if isinstance(path, JarFile):
                for cf in path.all_classes(
                    context=None if no_inherit else self):
                    yield cf
                continue

            # We have a directory root of a package.
            for root, dirs, files in os.walk(path):
                for file_ in (f for f in files if f.endswith('.class')):
                    yield ClassFile(
                        os.path.join(root, file_),
                        context=None if no_inherit else self
                    )

    def regex(self, regex, no_inherit=False):
        """
        Iterates over all classes available in the classpaths, whose path
        matches `regex`.

        .. warning:: The classpaths can contain many thousands of classes,
                     use this method sparingly.
        """
        for path in self._classpath:
            # We have a JarFile which supports this already, use it.
            if isinstance(path, JarFile):
                for file_ in path.regex(regex):
                    yield path.open_class(
                        file_, context=None if no_inherit else self)
                continue

            # We have a directory root of a package.
            for root, dirs, files in os.walk(path):
                for file_ in (f for f in files if f.endswith('.class')):
                    raise NotImplementedError()
