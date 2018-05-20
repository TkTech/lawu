"""
Implemented Attributes
======================

In addition to standard JVM attributes various compilers, debuggers, and other
tools may insert additional unknown attributes into a :class:`~jawa.cf
.ClassFile`.

Not all standard attributes are currently implemented. When an unknown
attribute is encountered, an :class:`~jawa.attribute.UnknownAttribute` object
is created instead. This UnknownAttribute retains the name and content of the
original attribute, allowing you to parse it yourself or to simply pass it
through.
"""