# Jawa

[![CircleCI](https://img.shields.io/circleci/project/github/TkTech/Jawa/master.svg?style=for-the-badge)](https://circleci.com/gh/TkTech/Jawa)
[![license](https://img.shields.io/github/license/tktech/jawa.svg?style=for-the-badge)](LICENCE)

Jawa is a human-friendly library for assembling, disassembling, and exploring
JVM class files. It's highly suitable for automation tasks.

*NOTE*: The assembler does _not_ currently implement Stack Maps, an
artificially complex requirement for ClassFiles generated for Java 7 and
above to properly verify (unless you turn it off with -XX:-UseSplitVerifier).
However, assembled files targeting Java 6 will still work with 7 and above.

## Documentation

API documentation & examples are available at http://jawa.tkte.ch

## Licence

Jawa is available under the MIT licence. See LICENCE.
