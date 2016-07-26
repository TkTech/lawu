.. include:: links.rst

Jawa - JVM ClassFile Library
================================

Jawa_ is a pure-python library for examining and disassembling JVM (Java)
class files.

.. note:: This documentation is up to date as of |today|.

Getting Jawa
------------

Jawa_ is now available on pypi. You can install the latest release with:

    pip install jawa

Alternatively, you can install the latest work directly from github:

    pip install git+https://github.com/TkTech/Jawa.git

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

Unlike most projects of its kind (like `Krakatau`_) Jawa is also very
permissively licenced under the MIT licence. You're free to use it in any
type of project should it be commercial, closed source or open source.


Basic Examples
--------------

.. toctree::
    :maxdepth: 2

    examples/index

Jawa API
--------

.. toctree::
    :maxdepth: 2

    jawa
    attributes/index
    util/index


* :ref:`genindex`


.. _to this day: http://wiki.vg
.. _Krakatau: https://github.com/Storyyeller/Krakatau
