.. include:: /links.rst

Working With Jar Files
======================

Almost all JVM applications are packaged as a ``.jar`` archive. Jawa_ provides
convienient reading, editing, and creation of ``.jar`` files via
:class:`~jawa.core.jf.JarFile`.

Basic Reading
-------------
Lets open a ``.jar`` archive and print the path of all its files::

   from jawa.core.jf import JarFile

   with JarFile('myjar.jar') as jf:
        for path in jf.namelist:
            print path

Basic Writing
-------------
Writing (and overwritting, if the file already exists) is also simple::

    from jawa.core.jf import JarFile

    with JarFile() as jf:
        jf.write('assets/about.txt', 'My Program (c) 2010')

Reading Classes
---------------
Loading a :class:`~jawa.core.cf.ClassFile` directly from a ``.jar`` is also
simple::

    from jawa.core.jf import JarFile

    with JarFile('myjar.jar') as jf:
        for path in jf.regex('*\.class'):
            cf = jf.open_class(path)
            print(cf.superclass)

Since the above example (loading all the classes in a ``.jar``) is so common,
there is also a handy shortcut::

    from jawa.core.jf import JarFile

    with JarFile('myjar.jar') as jf:
        for cf in jf.all_classes():
            print(cf.superclass)

Saving
------
Any changes you make must be explicitly saved, or your changes will be lost::

    from jawa.core.jf import JarFile

    with JarFile() as jf:
        jf.write('assets/about.txt', 'My Program (c) 2010')
        jf.save('myjar.jar')