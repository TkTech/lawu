.. include:: links.rst

Jawa - JVM ClassFile Library
================================

Jawa_ is a pure-python library for examining and disassembling JVM (Java)
class files.

.. note:: This documentation is up to date as of |today|.

Getting Jawa
------------

Jawa_ is not yet available on PyPi as it is still being developed. That said, breaking
changes are rare and installation from Github is very easy. To install::

    pip install git+https://github.com/TkTech/Jawa.git

Why Jawa?
---------

First, some background. Jawa is the successor project to "Solum", a library
written during the early days of Minecraft to facilitate automated contextual
disassembly of the Minecraft JARs with each release. This tool was able to
extract new block types, new network packets (and their structure) and other
similar interesting tidbits automatically any time a new release was made. This
drastically simplified our efforts to reverse engineer and document Minecraft
and its protocol (an effort which continues `to this day`_).

This means that Jawa is intended to be used very differently from most projects
similar to it. Instead of trying to produce a human-readable disassembly or
nearly-compilable Java, it's intended for people that want to dive into or
automate work on JVM bytecode. For example, Jawa has been used for:

- The automatic verification of community-uploaded plugins
- Analysis and analytics of public Android APKs (thousands at a time)

Fast forward a few years. There are new toys on the block like `Krakatau`_
which came out a few years after Solum. Krakatau is great disasembler &
decompiler, but it's API was not designed for humans and is not considered
"Pythonic". It does not follow PEP8, it is sparesly commented and poorly
documented. This makes it very hard to work with when all you want to do is
open up a Python shell and dive into a ClassFile.

Unlike most projects of its kind (like `Krakatau`_) Jawa is also very
permissively licenced under the MIT licence. You're free to use it in any
type of project should it be commercial, closed source or open source.


Basic Examples
--------------

.. toctree::
    :maxdepth: 2
    :glob:

    examples/*

Jawa Core API
-------------

.. toctree::
    :maxdepth: 2

    jawa
    jawa.attributes
    jawa.util


.. _to this day: http://wiki.vg
.. _Krakatau: https://github.com/Storyyeller/Krakatau
