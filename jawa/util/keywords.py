# -*- coding: utf8 -*-
_JAVA_KEYWORDS = (
    ('abstract', 5),
    ('assert', 5),
    ('boolean', 5),
    ('break', 5),
    ('byte', 5),
    ('case', 5),
    ('catch', 5),
    ('char', 5),
    ('class', 5),
    ('const', 5),
    ('continue', 5),
    ('default', 5),
    ('do', 5),
    ('double', 5),
    ('else', 5),
    ('extends', 5),
    ('final', 5),
    ('finally', 5),
    ('float', 5),
    ('for', 5),
    ('future', 5),
    ('generic', 5),
    ('goto', 5),
    ('if', 5),
    ('implements', 5),
    ('import', 5),
    ('inner', 5),
    ('instanceof', 5),
    ('int', 5),
    ('interface', 5),
    ('long', 5),
    ('native', 5),
    ('new', 5),
    ('null', 5),
    ('outer', 5),
    ('package', 5),
    ('private', 5),
    ('protected', 5),
    ('public', 5),
    ('rest', 5),
    ('return', 5),
    ('short', 5),
    ('static', 5),
    ('super', 5),
    ('switch', 5),
    ('synchronized', 5),
    ('this', 5),
    ('throw', 5),
    ('throws', 5),
    ('transient', 5),
    ('try', 5),
    ('var', 5),
    ('void', 5),
    ('volatile', 5),
    ('while', 5)
)


def kwlist(minimum_version=5):
    """
    Returns a list of Java language keywords that are available from
    `minimum_version` and below.
    """
    return (kw for kw, v in _JAVA_KEYWORDS if v <= minimum_version)


def is_keyword(kw):
    """
    Returns ``True`` if `kw` is a Java language keyword, ``False`` otherwise.
    """
    for keyword, _ in _JAVA_KEYWORDS:
        if keyword == kw:
            return True
    return False
