Jawa - JVM ClassFile Library
================================

Jawa_ is a human-friendly library for assembling, disassembling, and exploring
JVM class files. It's highly suitable for automation tasks.

.. note:: This documentation is up to date as of |today|.

Why Jawa?
---------

Jawa is intended to be used very differently from most projects similar to it.
Instead of trying to produce a human-readable disassembly or nearly-compilable
Java, it's intended for people that want to dive into or automate work on JVM
bytecode. For example, Jawa has been used for:

- The automatic verification of community-uploaded plugins
- Analysis and analytics of public Android APKs (thousands at a time)
- Automatic extraction of "private" API keys embedded in Android APKs.
- Automated reverse engineering of the Minecraft server and client.

Jawa is permissively licenced under the MIT licence. You're free to use it in
any type of project should it be commercial, closed source or open source.


Getting Started
---------------

It's recommended to use the :class:`~jawa.classloader.ClassLoader` when working
with JARs/directories, as it offers a number of conveniences. Here's an example
of loading each of the classes in the Minecraft_ server.

.. code-block:: python

    from jawa.classloader import ClassLoader

    loader = ClassLoader('minecraft_server.jar')
    for class_path in loader.classes:
        cf = loader[class_path]


Alternatively you can create & load a :class:`~jawa.cf.ClassFile` directly.

.. code-block:: python

    from jawa.cf import ClassFile

    with open('HelloWorld.class') as file_in:
        cf = ClassFile(file_in)


Examples
--------

.. toctree::
    :maxdepth: 2

    examples/hello_world.rst
    examples/dism.rst


Jawa API
--------

.. toctree::
    :maxdepth: 3

    jawa

* :ref:`genindex`
* :ref:`search`

.. include:: links.rst
