"""
An example showing how to create fields on a new class.
"""
from jawa import ClassFile

if __name__ == '__main__':
    cf = ClassFile.create('HelloWorld')

    # Creating a field from a field name and descriptor
    field = cf.fields.create('BeerCount', 'I')

    # A convienience shortcut for creating static fields.
    field = cf.fields.create_static(
        'HelloWorld',
        'Ljava/lang/String;',
        cf.constants.create_string('Hello World!')
    )

    with open('HelloWorld.class', 'wb') as fout:
        cf.save(fout)
