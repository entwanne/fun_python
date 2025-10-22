class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_node(self, child):
        self.children.append(child)

    def iter_tree(self, depth_first=False):
        nodes = [(self, None, 0)]
        while nodes:
            if depth_first:
                node, parent, n = nodes.pop()
                children = reversed(node.children)
            else:
                node, parent, n = nodes.pop(0)
                children = node.children

            yield node, parent, n

            for child in children:
                nodes.append((child, node, n+1))

    def print_tree(self):
        rows = [[]]

        for node, parent, n in self.iter_tree(depth_first=True):
            node.parent = parent
            if n >= len(rows):
                l = len(rows[n - 1]) - 1
                rows.append([None] * l)
            rows[n].append(node)

            for row in rows[:n]:
                while len(row) < len(rows[n]):
                    row.append(None)
            for row in rows[n+1:]:
                while len(row) < len(rows[n]) - 1:
                    row.append(None)

        for y, row in enumerate(rows):
            if y:
                line = ''
                spaces = 0
                for x, node in enumerate(row):
                    if x:
                        spaces += 1
                    if node and node.parent is rows[y-1][x]:
                        line += ' ' * spaces + '|'
                        spaces = 0
                    else:
                        spaces += 1
                print(line)

            line = ''
            spaces = 0
            last = None

            for x, node in enumerate(row):
                if x:
                    spaces += 1
                if node:
                    char = '-' if last and last.parent is node.parent else ' '
                    line += char * spaces + node.name
                    spaces = 0
                    last = node
                else:
                    spaces += 1
            print(line)
