# -*- coding: utf-8 -*-
from jawa.attribute import get_attribute_classes


def test_mandatory_attributes():
    required_properities = ['ADDED_IN', 'MINIMUM_CLASS_VERSION']
    for name, class_ in get_attribute_classes().items():
        for p in required_properities:
            assert hasattr(class_, p), (
                '{name} parser missing mandatory {p} property'.format(
                    name=name,
                    p=p
                )
            )


def test_attribute_naming():
    for name, class_ in get_attribute_classes().items():
        if hasattr(class_, 'ATTRIBUTE_NAME'):
            continue

        assert class_.__name__.endswith('Attribute'), (
            '{name} parser does not follow naming convention and does'
            ' not explicity set it.'.format(name=name)
        )
