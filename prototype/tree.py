from function import Function


class Tree(object):

    def __init__(self, data, sons=[]):
        if type(data) == str:
            self.init_from_string(data)
        else:
            self.data = data[:]
            self.sons = sons[:]

    def add_son(self, son):
        self.sons.append(son)

    def is_leave(self):
        return len(self.sons) == 0

    def get_paths_to_leaves(self):
        if self.is_leave():
            return [self.data]
        res = []
        for son in self.sons:
            for paths in son.get_paths_to_leaves():
                res += [self.data + x for x in paths]
        return res

    def print_tree(self, level=0):
        res = [" " * level + "|>" + str(self.data)]
        for son in self.sons:
            res += son.print_tree(level + 1)
        if level == 0:
            return '\n'.join(res)
        else:
            return res

    def __repr__(self):
        return self.print_tree()

    def init_from_string(self, s):
        self.data = []
        self.sons = []
        current_node = self
        nodes = []
        current_stack = ""
        for c in s:
            if c == '(':
                new_node = Tree([])
                current_node.add_son(new_node)
                nodes.append(current_node)
                current_node = new_node
            elif c == ';':
                current_node.data = Function(current_stack).to_list()
                current_node = nodes.pop()
                new_node = Tree([])
                current_node.add_son(new_node)
                nodes.append(current_node)
                current_node = new_node
                current_stack = ""
            elif c == ')':
                current_node.data = Function(current_stack).to_list()
                current_node = nodes.pop()
                current_stack = ""
            elif c != ' ':
                current_stack += c
        self.data = Function(current_stack).to_list()
