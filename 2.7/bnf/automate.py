alreadysetted = None
alreadycloned = None

def varlock(var, init):
    if var == None:
        return init, True
    return var, False

def varunlock(var, first):
    if first:
        return None
    return var

class State:
    pass

class Transition(State):
    label = ''
    next = None
    def __init__(self, label, next = None):
        self.label = label
        self.next = next
    def visit(self, visitor, l):
        visitor.visit_transition(self, l)
    def setLast(self, state):
        global alreadysetted
        alreadysetted, first = varlock(alreadysetted, [])
        if self in alreadysetted:
            return self
        alreadysetted.append(self)
        if self.next == None:
            self.next = state
        else:
            self.next.setLast(state)
        alreadysetted = varunlock(alreadysetted, first)
        return self
    def clone(self):
        global alreadycloned
        alreadycloned, first = varlock(alreadycloned, {})
        if self in alreadycloned.keys():
            return alreadycloned[self]
        new = Transition(self.label)
        alreadycloned[self] = new
        if self.next != None:
            new.next = self.next.clone()
        alreadycloned = varunlock(alreadycloned, first)
        return new

class Split(State):
    left = None
    right = None
    def __init__(self, left = None, right = None):
        self.left = left
        self.right = right
    def visit(self, visitor, l):
        visitor.visit_split(self, l)
    def setLast(self, state):
        global alreadysetted
        alreadysetted, first = varlock(alreadysetted, [])
        if self in alreadysetted:
            return self
        alreadysetted.append(self)
        if self.left == None:
            self.left = state
        else:
            self.left.setLast(state)
        if self.right == None:
            self.right = state
        else:
            self.right.setLast(state)
        alreadysetted = varunlock(alreadysetted, first)
        return self
    def clone(self):
        global alreadycloned
        alreadycloned, first = varlock(alreadycloned, {})
        if self in alreadycloned.keys():
            return alreadycloned[self]
        new = Split()
        alreadycloned[self] = new
        if self.left != None:
            new.left = self.left.clone()
        if self.right != None:
            new.right = self.right.clone()
        alreadycloned = varunlock(alreadycloned, first)
        return new

class Match(State):
    def visit(self, visitor, l):
        visitor.visit_match(self, l)
    def setLast(self, state):
        global alreadysetted
        alreadysetted, first = varlock(alreadysetted, [])
        if self in alreadysetted:
            return self
        alreadysetted.append(self)
        alreadysetted = varunlock(alreadysetted, first)
        return self
    def clone(self):
        global alreadycloned
        alreadycloned, first = varlock(alreadycloned, {})
        if self in alreadycloned.keys():
            return alreadycloned[self]
        alreadycloned[self] = new
        alreadycloned = varunlock(alreadycloned, first)
        return Match()

class RuleCall(State):
    name = None
    next = None
    def __init__(self, name):
        self.name = name
    def visit(self, visitor, l):
        visitor.visit_rulecall(self, l)
    def setLast(self, state):
        global alreadysetted
        alreadysetted, first = varlock(alreadysetted, [])
        if self in alreadysetted:
            return self
        alreadysetted.append(self)
        if self.next == None:
            self.next = state
        else:
            self.next.setLast(state)
        alreadysetted = varunlock(alreadysetted, first)
        return self
    def clone(self):
        global alreadycloned
        alreadycloned, first = varlock(alreadycloned, {})
        if self in alreadycloned.keys():
            return alreadycloned[self]
        new = RuleCall(self.name)
        alreadycloned[self] = new
        if self.next != None:
            new.next = self.next.clone()
        alreadycloned = varunlock(alreadycloned, first)
        return new

class RuleExit(State):
    next = None
    def visit(self, visitor, l):
        visitor.visit_ruleexit(self, l)
    def setLast(self, state):
        global alreadysetted
        alreadysetted, first = varlock(alreadysetted, [])
        if self in alreadysetted:
            return self
        alreadysetted.append(self)
        if self.next == None:
            self.next = state
        else:
            self.next.setLast(state)
        alreadysetted = varunlock(alreadysetted, first)
        return self
    def clone(self):
        global alreadycloned
        alreadycloned, first = varlock(alreadycloned, {})
        if self in alreadycloned.keys():
            return alreadycloned[self]
        new = RuleExit()
        alreadycloned[self] = new
        if self.next != None:
            new.next = self.next.clone()
        alreadycloned = varunlock(alreadycloned, first)
        return new

class Visitor:
    def match(self, rulename, s, rules):
        self.s = s
        self.pos = 0
        self.curtok = 'a'
        end = Match()
        self.current = [[RuleCall(rulename).setLast(end)]]
        self.next = []
        self.lfinal = []
        self.rules = rules
        while self.curtok and len(self.current):
            self.matched = False
            self.advance()
            for l in self.current:
                state = l[-1]
                state.visit(self, l)
            self.current = self.next
            self.next = []
        tree = None
        if (self.matched or (end in self.current)) and (not self.curtok):
            tree = ([], None)
            subtree = tree
            for e in self.lfinal:
                if isinstance(e, RuleCall):
                    newsubtree = ([], subtree)
                    subtree[0].append((e.name, newsubtree))
                    subtree = newsubtree
                elif isinstance(e, RuleExit):
                    if subtree[1]:
                        subtree = subtree[1]
                elif isinstance(e, Transition):
                    subtree[0].append((e.label, None))
        return tree
    def advance(self):
        if self.pos < len(self.s):
            self.curtok = self.s[self.pos]
            self.pos += 1
        else:
            self.curtok = ''
    def visit_transition(self, trans, l):
        if self.curtok == trans.label and trans.next:
            self.next.append(l + [trans.next])
    def visit_split(self, spl, l):
        if spl.left:
            spl.left.visit(self, l + [spl.left])
        if spl.right:
            spl.right.visit(self, l + [spl.right])
    def visit_match(self, _, l):
        self.matched = True
        self.lfinal = l
    def visit_rulecall(self, rule, l):
        if rule.name in self.rules:
            content = self.rules[rule.name].clone()
            content.setLast(RuleExit()).setLast(rule.next)
            content.visit(self, l + [content])
    def visit_ruleexit(self, rule, l):
        if rule.next:
            rule.next.visit(self, l + [rule.next])
