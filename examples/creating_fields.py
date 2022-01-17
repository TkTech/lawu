"""
An example showing how to create fields on a new class.
"""
from lawu.cf import ClassFile
from lawu.constants import String

if __name__ == '__main__':
    cf = ClassFile(this='HelloWorld')

    with cf:
        # Creating a field from a field name and descriptor
        field = cf.fields.create('BeerCount', 'I')

        # A convenience shortcut for creating static fields.
        field = cf.fields.create_static(
            'HelloWorld',
            'Ljava/lang/String;',
            String('Hello World!')
        )

    with open('HelloWorld.class', 'wb') as fout:
        cf.save(fout)
