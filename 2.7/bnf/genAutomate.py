import automate

def andNodeList(*nodes):
    prev = None
    first = None
    for node in nodes:
        if prev == None:
            first = node
        else:
            prev.setLast(node)
        prev = node
    return first

def orNodeList(*nodes):
    first = None
    for node in nodes:
        if first == None:
            first = node
        else:
            first = automate.Split(first, node)
    return first

def loopNode(node):
    first = automate.Split(node)
    node.setLast(first)
    return first

def rangeNode(c1, c2):
    first = None
    for c in range(ord(c1), ord(c2) + 1):
        node = automate.Transition(chr(c))
        if first == None:
            first = node
        else:
            first = automate.Split(first, node)
    return first

"""
def rule(name, node):
    #return node
    rule = automate.RuleEnter(name)
    rule.setLast(node)
    rule.setLast(automate.RuleExit())
    return rule
    #return automate.RuleEnter(name).setLast(node).setLast(automate.RuleExit())
"""
