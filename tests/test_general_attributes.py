# -*- coding: utf-8 -*-
from jawa.attribute import get_attribute_classes


def test_mandatory_attributes():
    for parser_class in get_attribute_classes().values():
        assert hasattr(parser_class, 'ADDED_IN'), (
            'Attribute parser missing mandatory ADDED_IN property'
        )
        assert hasattr(parser_class, 'MINIMUM_CLASS_VERSION'), (
            'Attribute parser missing mandatory MINIMUM_CLASS_VERSION '
            'property'
        )
