#!/usr/bin/env python2

from mod import *
import inspect, linecache

#print inspect.getsource(titi)

a = A()
old = inspect.getsource(A.method)
print old
print a.method()
def tutu(self):
    print 'tutu'
    return
A.method = tutu
new = inspect.getsource(A.method)
print new
print a.method()

#print inspect.getmembers(A)

src = inspect.getsource(A)
print src

def indent(s):
    for i, c in enumerate(s):
        if c != ' ' and c != '\t':
            break
    return s[:i]

tabs = indent(old)
new = '\n'.join(tabs + l for l in new.split('\n'))

newsrc = src.replace(old, new)
print newsrc

print '========================================='

with open('mod2.py', 'w') as f:
    f.write(src)
import mod2
print inspect.getsource(mod2.A)

with open('mod2.py', 'w') as f:
    f.write(newsrc)
from os import unlink
unlink('mod2.pyc')
reload(mod2)

a = mod2.A()
a.tutu()
linecache.checkcache()
print inspect.getsource(mod2.A)
