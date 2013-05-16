#!/usr/bin/env python3

def are_args_of_types(list_args, list_types):
    """
    are_args_of_types([4, 1.0], [int, float])        -> True
    are_args_of_types([4, 1.0], [int, int])          -> False
    are_args_of_types([4, 1],   [int, float])        -> False
    are_args_of_types([4, 1.0], [int, (int, float)]) -> True
    are_args_of_types([4, 1],   [int, (int, float)]) -> True
    """
    return all(any(isinstance(a, tt) for tt in t) if isinstance(t, set) else
               isinstance(a, t)
               for a, t in zip(list_args, list_types))

from collections import defaultdict
import inspect

template_funcs = defaultdict(list)
def template(f):
    argspec = inspect.getfullargspec(f)
    template_funcs[f.__name__].append(([argspec.annotations[a] if a in argspec.annotations else object for a in argspec.args], f))
    def decorator(*args, **kwargs):
        for type_args, f_ in template_funcs[f.__name__]:
            if are_args_of_types(args, type_args):
                return f_(*args, **kwargs)
    return decorator

@template
def addition(a : {int, float}, b : {int, float}):
    print('Addition int')
    return a + b

@template
def addition(a : str, b : str):
    print('Addition str')
    return a + b

print(addition(5, 4))
print(addition('a', 'b'))
print(addition(5.0, 1.0))
