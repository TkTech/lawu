from jawa.blocks import basic_blocks


def test_basic_blocks(loader):
    cf = loader['HelloWorld']
    main = cf.methods.find_one(name='main')
    assert list(basic_blocks(main.code.disassemble())) == [
        (0, 5),
        (8, 8)
    ]

    cf = loader['LookupSwitch']
    main = cf.methods.find_one(name='main')
    assert list(basic_blocks(main.code.disassemble())) == [
        (0, 1),
        (28, 28),
        (29, 29),
        (30, 30)
    ]

    hello_world = loader['TableSwitch']
    main = hello_world.methods.find_one(name='main')
    assert list(basic_blocks(main.code.disassemble())) == [
        (0, 1),
        (28, 28),
        (29, 29),
        (30, 30),
        (31, 31)
    ]
