Generating Classes From Scratch - Hello World!
==============================================

A simple example of the classic "Hello World!" program. This example will
generate a ClassFile equivalent to this Java:

.. code-block:: java

    class HelloWorld {
        public static void main(String[] args) {
            System.out.println("Hello World!");
        }
    }

.. literalinclude:: ../../examples/hello_world.py

Our example can then be run in the standard JVM:

.. code-block:: text

    $ python hello_world.py
    $ java HelloWorld                                                                                                                                                                                                                                   develop
    Hello World!