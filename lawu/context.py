from contextvars import ContextVar

_class_context: ContextVar = ContextVar('class_context')


def class_context():
    class_stack = _class_context.get(None)
    if class_stack is None:
        lst = []
        _class_context.set(lst)
        return lst
    return class_stack


def current_class_context():
    class_stack = class_context()
    if class_stack:
        return class_stack.pop()
