Implemented Attributes
======================

Standard attributes are defined in `Section 4.7 - Attributes`_. In addition to
these attributes, various compilers, debuggers, obfuscators, and other tools
may insert additional unknown attributes into a :class:`~jawa.cf.ClassFile`.

Not all standard attributes are currently implemented. When an unknown
attribute is encountered, an :class:`~jawa.attribute.UnknownAttribute` object
is created instead.

jawa.attributes.code module
---------------------------

.. automodule:: jawa.attributes.code
    :members:
    :undoc-members:
    :show-inheritance:

jawa.attributes.constant_value module
-------------------------------------

.. automodule:: jawa.attributes.constant_value
    :members:
    :undoc-members:
    :show-inheritance:

jawa.attributes.source_file module
----------------------------------

.. automodule:: jawa.attributes.source_file
    :members:
    :undoc-members:
    :show-inheritance:


.. _Section 4.7 - Attributes: https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html#jvms-4.7
