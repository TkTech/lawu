from lawu import ast


def test_try_catch(loader):
    cf = loader['TryCatch']

    m = cf.methods.find_one(name='test')

    assert m.code == ast.Code(
        max_locals=3,
        max_stack=2,
        children=[
            ast.TryCatch(
                'catch_1',
                'java/lang/ArithmeticException',
                children=[
                    ast.TryCatch(
                        'catch_2',
                        'java/lang/Exception',
                        children=[
                            ast.Finally(
                                'catch_3',
                                children=[
                                    ast.Instruction('iconst_1'),
                                    ast.Instruction('iconst_0'),
                                    ast.Instruction('idiv'),
                                    ast.Instruction('istore_1')
                                ]
                            )
                        ]
                    )
                ]
            ),
            ast.Instruction('return'),
            ast.Label('catch_1'),
            ast.Instruction('astore_1'),
            ast.Instruction('return'),
            ast.Label('catch_2'),
            ast.Instruction('astore_1'),
            ast.Instruction('return'),
            ast.Label('catch_3'),
            ast.Instruction('astore_2'),
            ast.Instruction('return')
        ]
    )
