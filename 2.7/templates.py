#!/usr/bin/env python3

def is_args_of_types(args, types_lists):
    return all([any(isinstance(arg, targ) for targ in types_list) if isinstance(types_list, set) else isinstance(arg, types_list) for (arg, types_list) in zip(args, types_lists)])

def check_types(*types_lists):
    def decorator(f):
        def g(*args, **kwargs):
            if is_args_of_types(args, types_lists):
                return f(*args, **kwargs)
            raise TypeError
        return g
    return decorator

templates_funcs = {}
def register_template(*types_lists):
    def decorator(f):
        """
        name = f.__name__
        if name in templates_funcs:
            templates_funcs[name][types_lists] = f
        else:
            templates_funcs[name] = {types_lists : f}
        """
        templates_funcs.setdefault(f.__name__, {})[types_lists] = f
        return f
    return decorator

def template(f):
    def g(*args, **kwargs):
        try:
            for types_lists, g in templates_funcs[f.__name__].items():
                if is_args_of_types(args, types_lists):
                    return g(*args, **kwargs)
        except:
            raise TypeError
    return g

@check_types(int, {float, int})
def myfunc(a, b):
    return a + b

@register_template(int, int)
def myfunc2(a, b):
    print('Addition d\'ints')
    return a + b

@register_template(str, str)
def myfunc2(a, b):
    print('Addition de strings')
    return a + b

@template
def myfunc2():
    pass

print(myfunc(4, 8.))

print(myfunc2(4, 8))
print(myfunc2('a', 'b'))
