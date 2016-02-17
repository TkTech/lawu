#!/usr/bin/env python
# encoding: utf-8
import os

from jawa import ClassFile
from jawa.util.bytecode import Instruction, Operand


def test_hello_world():
    """
    An integration test for the complete parsing of a simple HelloWorld
    example.

    The source example is as follows:

    .. code::

        class HelloWorld {
            public static void main(String[] args) {
                System.out.println("Hello World!");
            }
        }
    """
    sample_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'HelloWorld.class'
    )
    with open(sample_path, 'rb') as fin:
        cf = ClassFile(fin)

        assert len(cf.constants) == 21
        assert len(cf.attributes) == 0
        assert len(cf.fields) == 0
        assert len(cf.methods) == 1

        main_method = cf.methods.find_one(name='main')
        assert main_method is not None

        # 0x08 for ACC_STATIC, 0x01 for ACC_PUBLIC
        assert main_method.access_flags.value == 0x9
        assert main_method.code.max_locals == 1
        assert main_method.code.max_stack == 2

        instruction_list = list(main_method.code.disassemble())
        assert instruction_list == [
            Instruction(mnemonic='getstatic', opcode=178, operands=[
                Operand(op_type=30, value=13)
            ], pos=0),
            Instruction(mnemonic='ldc', opcode=18, operands=[
                Operand(op_type=30, value=15)
            ], pos=3),
            Instruction(mnemonic='invokevirtual', opcode=182, operands=[
                Operand(op_type=30, value=21)
            ], pos=5),
            Instruction(mnemonic='return', opcode=177, operands=[], pos=8)
        ]
