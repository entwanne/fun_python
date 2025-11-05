import functools
import inspect


class deferred:
    def __init__(self, get_value):
        self.get_value = get_value

    def get(self):
        return self.get_value()

    def __repr__(self):
        return f'deferred({self.get_value!r})'


def apply(func):
    sig = inspect.signature(func)

    for param in sig.parameters.values():
        if isinstance(param.default, deferred):
            param.default._default = True

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        b = sig.bind(*args, **kwargs)
        b.apply_defaults()
        args = [
            arg.get() if isinstance(arg, deferred) and getattr(arg, '_default', False) else arg
            for arg in b.args
        ]
        kwargs = {
            name: arg.get() if isinstance(arg, deferred) and getattr(arg, '_default', False) else arg
            for name, arg in b.kwargs.items()
        }
        return func(*args, **kwargs)

    return wrapper
