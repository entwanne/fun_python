import types
import sys

class MyModule(types.ModuleType):
    @property
    def x(self):
        return 10

sys.modules[__name__].__class__ = MyModule

del types, sys, MyModule
