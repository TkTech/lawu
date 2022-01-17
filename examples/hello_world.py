"""
An example showing how to create a "Hello World" class from scratch.
"""
from lawu.cf import ClassFile
from lawu.assemble import assemble
from lawu.constants import String

cf = ClassFile(this='HelloWorld')

main = cf.methods.create('main', '([Ljava/lang/String;)V', code=True)
main.access_flags.acc_static = True
main.code.max_locals = 1
main.code.max_stack = 2

with cf:
    main.code.assemble(assemble([
        ('getstatic', cf.constants.create_field_ref(
            'java/lang/System',
            'out',
            'Ljava/io/PrintStream;'
        )),
        ('ldc', String('Hello World!')),
        ('invokevirtual', cf.constants.create_method_ref(
            'java/io/PrintStream',
            'println',
            '(Ljava/lang/String;)V'
        )),
        ('return',)
    ]))

with open('HelloWorld.class', 'wb') as fout:
    cf.save(fout)
