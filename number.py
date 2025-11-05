#!/usr/bin/env python3

# Gérer autres opérations : pow, and, or, etc.

class Object:
    @staticmethod
    def getobject(i):
        if isinstance(i, Object):
            return i
        if isinstance(i, int) or isinstance(i, float):
            return Number(i)
        if isinstance(i, list):
            return Numbers(i)
        raise TypeError
    def __call__(self, **kwargs):
        return self
    def __radd__(self, other):
        return self.__add__(other)
    def __rsub__(self, other):
        return -self.__sub__(other)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __pos__(self):
        return self
    def __neg__(self):
        return -1 * self

class Number(Object):
    value = 0
    def __init__(self, value = 0):
        self.value = value
    def __add__(self, other):
        other = self.getobject(other)
        if not isinstance(other, Number):
            return NotImplemented
        return Number(self.value + other.value)
    def __sub__(self, other):
        other = self.getobject(other)
        if not isinstance(other, Number):
            return NotImplemented
        return Number(self.value - other.value)
    def __mul__(self, other):
        other = self.getobject(other)
        if not isinstance(other, Number):
            return NotImplemented
        return Number(self.value * other.value)
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return repr(self.value)

class Numbers(Object):
    values = []
    def __init__(self, values = []):
        self.values = [self.getobject(v) for v in values]
    def __call__(self, **kwargs):
        return Numbers([v() for v in self.values])
    def __add__(self, other):
        try:
            return Numbers([v + other for v in self.values])
        except:
            return NotImplemented
    def __sub__(self, other):
        try:
            return Numbers([v - other for v in self.values])
        except:
            return NotImplemented
    def __mul__(self, other):
        try:
            return Numbers([v * other for v in self.values])
        except:
            return NotImplemented
    def __repr__(self):
        return repr(self.values)
    def __str__(self):
        return str(self.values)
        

class Variable(Object):
    value = None
    def __init__(self, name = 'var'):
        self.name = name
    def __call__(self, **kwargs):
        if self.name in kwargs:
            v = Variable(self.name)
            v.value = self.getobject(kwargs[self.name])
            return v()
        return self
    def setValue(self, value):
        self.value = self.getobject(value)
    def __add__(self, other):
        if self.value != None:
            return self.value + other
        try:
            return Addition(self, self.getobject(other))
        except:
            return NotImplemented
    def __sub__(self, other):
        if self.value != None:
            return self.value - other
        try:
            return -Addition(self, self.getobject(other))
        except:
            return NotImplemented
    def __mul__(self, other):
        if self.value != None:
            return self.value * other
        try:
            return Multiplication(self, self.getobject(other))
        except:
            return NotImplemented
    def __repr__(self):
        if self.value != None:
            return '(' + self.name + ':' + repr(self.value) + ')'
        return self.name
    def __str__(self):
        return repr(self)

class Operation(Object):
    def __add__(self, other):
        try:
            return Addition(self, self.getobject(other))
        except:
            return NotImplemented
    def __sub__(self, other):
        try:
            return -Addition(self, self.getobject(other))
        except:
            return NotImplemented
    def __mul__(self, other):
        try:
            return Multiplication(self, self.getobject(other))
        except:
            return NotImplemented
    def factorize(self): pass

class _Addition(Operation):
    def __init__(self, left, right):
        self.left, self.right = left, right
    def __call__(self, **kwargs):
        return (self.left)(**kwargs) + (self.right)(**kwargs)
    def __repr__(self):
        return str(self.left) + ' + ' + str(self.right)
    def __str__(self):
        return str(self.left) + ' + ' + str(self.right)

class _Multiplication(Operation):
    def __init__(self, left, right):
        self.left, self.right = left, right
    def __call__(self, **kwargs):
        return (self.left)(**kwargs) * (self.right)(**kwargs)
    def __repr__(self):
        return repr(self.left) + ' * ' + repr(self.right)
    def __str__(self):
        return str(self.left) + ' * ' + str(self.right)

def Addition(left, right):
    if isinstance(left, Number) and left.value == 0:
        return right
    if isinstance(right, Number) and right.value == 0:
        return left
    return _Addition(left, right)

def Multiplication(left, right):
    if isinstance(left, Number):
        if left.value == 0:
            return left
        if left.value == 1:
            return right
    if isinstance(right, Number):
        if right.value == 0:
            return right
        if right.value == 1:
            return left
    return _Multiplication(left, right)

if __name__ == '__main__':
    # Bugs sur les multiplications entre variables
    t = Variable('t')
    u = Variable('u') 
    expr = t * 5 + 2 + u
    print(expr)
    print('expr:', expr())
    print('expr(t = 0):', expr(t = 0))
    print('expr(t = 1):', expr(t = 1))
    print('expr(t = 2 * u):', expr(t = 2 * u))
    print('expr(t = 1, u = 2):', expr(t = 1, u = 2))
    print('expr(t = 1)(u = 2):', expr(t = 1)(u = 2))
    print('expr(t = 1)(u = 2):', expr(t = 1)(u = 2))
    print('expr(t = [0, 1, 2]):', expr(t = [0, 1, 2]))
    print('expr(t = [0, 1, 2], u = [0, 10]):', expr(t = [0, 1, 2], u = [0, 10]))
    v = Variable('v') 
    expr = u * t + v
    print(expr)
    print(expr(u=1, v=0))
