#!/usr/bin/env python2
# -*- coding: utf-8 -*-

def decorator_set_flag(f, flag, value = None):
    f = staticmethod(f)
    setattr(f.__func__, flag, value)
    return f

def init(f):
    return decorator_set_flag(f, 'decorator.init')

def method(f):
    return decorator_set_flag(f, 'decorator.method')

#class Decorator(types.TypeType):
class Decorator(type):
    # Création d'un nouvel objet (instanciation de Decorator)
    def __new__(self, class_, *args, **kwargs):
        # Décorations nécessaires pour un bon fonctionnement (l'ordre est important)
        if hasattr(self, 'necessary_decorators'):
            for t in self.necessary_decorators:
                if not isinstance(t, tuple):
                    t = (t,)
                # Complète le tuple si nécessaire pour obtenir un (decorator, args, kwargs)
                if len(t) < 3:
                    t += ([], {})[len(t) - 1:]
                d, a, k = t[:3]
                # Si la décoration n'a pas déjà été faîte
                if not self.isdecoratedby(class_, d):
                    class_ = d(class_, *a, **k)
        # On enregistre les paramètres supplémentaires (l'obligatoire étant la classe à décorer)
        self.args, self.kwargs = args, kwargs
        # On définit la nouvelle classe (notre classe décorée, héritant de la classe à décorer)
        class Decorated(class_):
            # Surcharge l'__init__ de la classe pour pouvoir opérer la décoration
            def __init__(self_, *args, **kwargs):
                # Respecte l'initialisation héritée
                super(Decorated, self_).__init__(*args, **kwargs)
                self_.__baseclass__ = class_
                # Fonction supplémentaire d'initialisation
                init_func = None
                for name in dir(self):
                    try:
                        f = getattr(self, name)
                        if hasattr(f, 'decorator.init'):
                            init_func = f
                            break
                    except AttributeError:
                        continue
                if init_func:
                    # Appelle l'initialisation avec l'objet et les précédents args & kwargs enregistrés
                    init_func(self_, *self.args, **self.kwargs)
        # Enregistre la classe courante Decorated associée à la classe décoratrice (pour pouvoir la retrouver dans l'arbre d'héritage)
        if not hasattr(Decorated, '__decorating_classes__'):
            Decorated.__decorating_classes__ = {}
        Decorated.__decorating_classes__[self] = Decorated
        # Met en place toutes les méthodes supplémentaires dans la classe Decorated
        for name in dir(self):
            try:
                f = getattr(self, name)
                if hasattr(f, 'decorator.method'):
                    setattr(Decorated, name, f)
            except AttributeError:
                pass
        return Decorated

    @staticmethod
    def currentclass(decorating_class, obj):
        return obj.__decorating_classes__[decorating_class]

    @staticmethod
    def super(decorating_class, obj):
        "Permet de remonter l'arbre d'héritage en fonction d'un décorateur plutôt que d'une classe parente"
        #class_ = obj.__decorating_classes__[decorating_class]
        class_ = Decorator.currentclass(decorating_class, obj)
        return super(class_, obj)

    # Étendre pour que le 2ème paramètre puisse être un tuple de classes
    @staticmethod
    def isdecoratedby(obj, decorating_class):
        "Savoir si un objet ou oune classe est décorée"
        if not hasattr(obj, '__decorating_classes__'):
            return False
        return decorating_class in obj.__decorating_classes__


if __name__ == '__main__':
    # Exemple d'utilisation, décoration de l'int
    class MyDecorator(Decorator):
        # Cette fonction sera appelée à chaque instanciation d'objet
        # Le paramètre s devra être passé à la construction du décorateur
        @init
        def __init__(self, s):
            print self, s

        # Celle-ci deviendra une méthode de la classe
        @method
        def my_new_method(self):
            print 'My method :', self

    myInt = MyDecorator(int, 'toto')
    a = myInt(42)
    print a + 2
    a.my_new_method()
