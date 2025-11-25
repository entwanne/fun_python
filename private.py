import contextvars
import functools
import inspect
import weakref
import types


class Private:
    def __init__(self):
        self._var = contextvars.ContextVar('_var')

    def __set_name__(self, owner, name):
        self.name = name
        context = contextvars.copy_context()
        old_getattribute = owner.__getattribute__

        def get_patched(method):
            @functools.wraps(method)
            def patched(*args, **kwargs):
                def wrapper():
                    self._var.set(self._var.get(weakref.WeakKeyDictionary()))
                    return method(*args, **kwargs)
                return context.run(wrapper)
            return patched

        def getattribute(self, name):
            attr = old_getattribute(self, name)
            if not isinstance(attr, types.MethodType):
                return attr

            return get_patched(attr)

        owner.__getattribute__ = getattribute
        old_init = owner.__init__
        owner.__init__ = get_patched(old_init)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            return self._var.get()[instance]
        except (LookupError, KeyError):
            raise AttributeError(self.name) from None

    def __set__(self, instance, value):
        try:
            self._var.get()[instance] = value
        except LookupError:
            raise AttributeError(self.name) from None


class Class:
    x = Private()

    def __init__(self, x):
        self.x = x

    def get_x(self):
        return self.x


obj = Class(5)
obj2 = Class(1)
print(obj.get_x())
print(obj2.get_x())
#print(Class.__dict__['x']._values[obj])
#obj.x = 0
#print(obj.x)
#print(dict(Class.x._var.get()))
