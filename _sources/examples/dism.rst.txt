Disassembly - A Simple javap Clone
==================================

`Javap`_ is the defacto Java disassembler and is included when you installed
the Oracle JDK. We can make a simple clone very easily using Jawa:

.. literalinclude:: ../../examples/disassemble.py

If we try this out on a HelloWorld class, our output will look like:

.. code-block:: text

    $ python disassemble.py --class-path ../tests/data HelloWorld                                                                                                                                                                                          develop
    ; ---------------------------------------------- constant pool
    ; -------------------------------------------------- total: 21
    ; 0001: <UTF8(index=1, value='HelloWorld'>)
    ; 0002: <ConstantClass(index=2, name=<UTF8(index=1, value='HelloWorld'>))>
    ...
    ; ----------------------------------------------------- fields
    ; --------------------------------------------------- total: 0
    ; ---------------------------------------------------- methods
    ; --------------------------------------------------- total: 1
    acc_public acc_static void main(java/lang/String[]) {
      0000 [0xB2]       getstatic <- C[13]
      0003 [0x12]             ldc <- C[15]
      0005 [0xB6]   invokevirtual <- C[21]
      0008 [0xB1]          return <-
    }


.. _Javap: https://docs.oracle.com/javase/8/docs/technotes/tools/windows/javap.html
