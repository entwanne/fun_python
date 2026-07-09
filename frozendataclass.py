import inspect
from typing import Self


def frozendataclass(cls):
    name = cls.__name__
    qualname = cls.__qualname__
    bases = list(cls.__bases__)
    annotations = inspect.get_annotations(cls, format=inspect.Format.FORWARDREF)

    signature = inspect.Signature(
        inspect.Parameter(
            field,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=annotation,
        )
        for field, annotation in annotations.items()
    )

    def cls_init(self, *args, **kwargs):
        fields = frozendict(signature.bind(*args, **kwargs).arguments)
        super.__init__(self, frozendict, fields)

    cls_init.__name__ = '__init__'
    cls_init.__qualname__ = f'{qualname}.__init__'
    cls_init.__signature__ = signature.replace(
        parameters=(
            inspect.Parameter('self', inspect.Parameter.POSITIONAL_OR_KEYWORD),
            *signature.parameters.values(),
        ),
    )

    def cls_repr(self) -> str:
        args = ', '.join(f'{name}={value!r}' for name, value in self.__dict__.items())
        return f'{name}({args})'

    cls_repr.__name__ = '__repr__'
    cls_repr.__qualname__ = f'{qualname}.__repr__'

    def cls_dict(self) -> frozendict:
        return super.__self__.__get__(self)

    def cls_get(name):
        def get(self):
            return self.__dict__[name]

        return get

    properties = {
        name: property(cls_get(name))
        for name in annotations
    }

    bases[bases.index(object)] = super
    return type(
        name,
        tuple(bases),
        {
            **properties,
            '__slots__': (),
            '__init__': cls_init,
            '__repr__': cls_repr,
            '__signature__': signature,
            '__qualname__': qualname,
            '__dict__': property(cls_dict),
            '__self__': None,
            '__self_class__': None,
            '__thisclass__': None,
        },
    )


#from dataclasses import dataclass as frozendataclass


@frozendataclass
class Point:
    x: int
    y: int


p = Point(3, 4)
#help(Point)
print(p)
print(p.__dict__)
print(p.x)
