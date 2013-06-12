#!/usr/bin/env python3

# Find the smallest mask which doesn't change 9with and) the numbers

from random import randrange
from functools import reduce
from sys import stdin

NB_PLAYERS = 2
MAX = 256
numbers = [randrange(0, MAX) for _ in range(NB_PLAYERS)]
solution = reduce(lambda x, y: x | y, numbers)

#print(numbers)
#print(bin(solution))

for s in stdin:
    choice = int(s, base=0)
    if choice == solution:
        print('Win')
        break
    matchs = 0
    for n in numbers:
        if (n & choice) == n:
            matchs += 1
    print('Match with %d numbers' % matchs)
