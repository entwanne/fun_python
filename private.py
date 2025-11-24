import contextvars
import gc
import inspect
import weakref


class Private:
    def __init__(self):
        self._values = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return '<private>'
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        if not caller_frame:
            raise ValueError
        caller_method = getattr(owner, caller_frame.f_code.co_name, None)
        if caller_method is None or caller_method.__code__ is not caller_frame.f_code:
            raise ValueError
        return self._values[instance]

    def __set__(self, instance, value):
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        if not caller_frame:
            raise ValueError
        owner = type(instance)
        caller_method = getattr(owner, caller_frame.f_code.co_name, None)
        if caller_method is None or caller_method.__code__ is not caller_frame.f_code:
            raise ValueError
        self._values[instance] = value


class Class:
    x = Private()

    def __init__(self, x):
        self.x = x

    def get_x(self):
        return self.x


obj = Class(5)
print(obj.get_x())
#print(obj.x)
print(Class.__dict__['x']._values[obj])
