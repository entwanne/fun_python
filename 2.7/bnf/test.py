#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import automate as aut, genAutomate as gen
from interpretor import *
import sys

end = aut.Match()

rules = {}

rules['chiffre'] = gen.rangeNode('0', '9')
test = gen.loopNode(aut.RuleCall('chiffre'))
rules['number'] = gen.andNodeList(aut.RuleCall('chiffre'), test)
rules['final'] = gen.andNodeList(gen.orNodeList(aut.Transition('-'), None), gen.orNodeList(aut.RuleCall('number'), gen.andNodeList(aut.Transition('('), aut.RuleCall('expr'), aut.Transition(')'))))
rules['op3'] = gen.orNodeList(aut.RuleCall('final'), gen.andNodeList(aut.RuleCall('final'), aut.Transition('^'), aut.RuleCall('op3')))
rules['op2'] = gen.orNodeList(aut.RuleCall('op3'), gen.andNodeList(aut.RuleCall('op3'), gen.orNodeList(aut.Transition('*'), aut.Transition('/')), aut.RuleCall('op2')))
rules['op1'] = gen.orNodeList(aut.RuleCall('op2'), gen.andNodeList(aut.RuleCall('op2'), gen.orNodeList(aut.Transition('+'), aut.Transition('-')), aut.RuleCall('op1')))
rules['expr'] = aut.RuleCall('op1')

def get_chiffre(l):
    return ord(l[0]) - ord('0')

def get_number(l):
    n = 0
    for i in l:
        n = n * 10 + i
    return n

def get_op1(l):
    if len(l) == 1:
        return l[0]
    if l[1] == '+':
        return l[0] + l[2]
    elif l[1] == '-':
        return l[0] - l[2]

def get_op2(l):
    if len(l) == 1:
        return l[0]
    if l[1] == '*':
        return l[0] * l[2]
    elif l[1] == '/':
        return l[0] / l[2]

def get_op3(l):
    if len(l) == 1:
        return l[0]
    if l[1] == '^':
        return l[0] ** l[2]

def get_final(l):
    mul = 1
    if l[0] == '-':
        mul = -1
        l = l[1:]
    if len(l) == 1:
        return mul * l[0]
    else:
        return mul * l[1]

def get_expr(l):
    return l[0]

def run(s):
    v = aut.Visitor()
    tree = v.match('expr', s, rules)
    print (True if tree else False)
    if tree:
        i = Interpretor()
        i.bind('chiffre', get_chiffre)
        i.bind('number', get_number)
        i.bind('op1', get_op1)
        i.bind('op2', get_op2)
        i.bind('op3', get_op3)
        i.bind('final', get_final)
        i.bind('expr', get_expr)

        print i.interpret(tree)[0]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        print 'Usage: %s expression' % sys.argv[0]
