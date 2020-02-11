from lawu import ast
from lawu.blocks import blocks


def _basic_blocks(loader):
    cf = loader['HelloWorld']
    main = cf.methods.find_one(name='main')
    assert list(blocks(main.code.disassemble())) == [
        (0, 5),
        (8, 8)
    ]

    return

    cf = loader['LookupSwitch']
    main = cf.methods.find_one(name='main')
    assert list(blocks(main.code.disassemble())) == [
        (0, 1),
        (28, 28),
        (29, 29),
        (30, 30)
    ]

    hello_world = loader['TableSwitch']
    main = hello_world.methods.find_one(name='main')
    assert list(blocks(main.code.disassemble())) == [
        (0, 1),
        (28, 28),
        (29, 29),
        (30, 30),
        (31, 31)
    ]


def test_jump_targets(loader):
    cf = loader['LookupSwitch']
    main = cf.methods.find_one(name='main')

    assert main.code.same(ast.Code(
        max_stack=1,
        max_locals=1,
        children=[
            ast.Instruction('iconst_1'),
            ast.Instruction('lookupswitch', children=[
                ast.ConditionalJump(match=1, target='label_1'),
                ast.ConditionalJump(match=3, target='label_2'),
                ast.Jump('label_3')
            ]),
            ast.Label('label_1'),
            ast.Instruction('return'),
            ast.Label('label_2'),
            ast.Instruction('return'),
            ast.Label('label_3'),
            ast.Instruction('return')
        ]
    ))
