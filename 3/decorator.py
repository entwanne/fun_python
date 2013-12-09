#!/usr/bin/env python

def _method_flag_setter(flag, value=None):
    def decorator(func):
        setattr(func, flag, value)
        return staticmethod(func)
    return decorator

method = _method_flag_setter('_decorator_method')


class Decorator(type):
    def __new__(cls, baseclass, *args, **kwargs):
        class Decorated(baseclass):
            def __new__(cls_, *args_, **kwargs_):
                obj = super().__new__(cls_, *args_, **kwargs_)
                if hasattr(cls, '__decorated_init__') and callable(cls.__decorated_init__):
                    cls.__decorated_init__(obj, *args, **kwargs)
                return obj
        Decorated._decorating_classes = dict(getattr(baseclass, '_decorating_classes', {}))
        Decorated._decorating_classes[cls] = Decorated
        for name in dir(cls):
            method = getattr(cls, name, None)
            if method is not None:
                if hasattr(method, '_decorator_method'):
                    setattr(Decorated, name, method)
        return Decorated

    @classmethod
    def currentclass(cls, decorated):
        return decorated._decorating_classes[cls]

    @classmethod
    def super(cls, decorated):
        return super(cls.currentclass(decorated), decorated)

    @classmethod
    def decoratorof(cls, decorated):
        return cls in getattr(decorated, '_decorating_classes', {})
        

if __name__ == '__main__':
    class MyDecorator(Decorator):
        def __decorated_init__(self, s):
            print(self, s)
        @method
        def my_new_method(self):
            print('My method:', self)
        @method
        def __add__(self, other):
            print('addition')
            return MyDecorator.super(self).__add__(other)
    class MyDecorator2(Decorator):
        def __decorated_init__(self, s):
            print(self, s)
        @method
        def my_new_method(self):
            MyDecorator2.super(self).my_new_method()
            print('My super method:', self)

    MyInt = MyDecorator(int, 'toto')
    a = MyInt(42)
    print(a + 2)
    a.my_new_method()

    #MyInt2 = MyDecorator(MyInt, 'tutu')
    #b = MyInt2(42)
    #print(b + 2)
    #b.my_new_method()

    MyInt3 = MyDecorator2(MyInt, 'tutu')
    c = MyInt3(42)
    print(c + 2)
    c.my_new_method()

    print(MyDecorator.decoratorof(MyInt))
    print(MyDecorator2.decoratorof(MyInt))
    print(MyDecorator.decoratorof(a))
    print(MyDecorator2.decoratorof(a))
    print(MyDecorator.decoratorof(MyInt3))
    print(MyDecorator2.decoratorof(MyInt3))
    print(MyDecorator.decoratorof(c))
    print(MyDecorator2.decoratorof(c))
