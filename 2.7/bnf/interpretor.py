class Interpretor:
    bindings = {}
    def bind(self, name, func):
        self.bindings[name] = func
    def unbind(self, name):
        del self.bindings[name]
    def interpret(self, tree):
        l = tree[0]
        for i in range(len(l)):
            if l[i][1] == None or not l[i][0] in self.bindings:
                l[i] = l[i][0]
            else:
                l[i] = self.bindings[l[i][0]](self.interpret(l[i][1]))
        return l
