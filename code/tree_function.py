from duplication_rule import DuplicationRule
from function import Function
from fake_tree_function import FakeTreeFunction
from utils import stack, unstack
from graphviz import Digraph


class TreeFunction(object):
    """TreeFunction Represents a tree function"""

    def __init__(self, data, sons=[], name="tf"):
        """__init__
        Initialize a tree function.
        :param head: The head of the tree. It is a Function (linear function)
        :param sons: The sons trees
        :param name: The name of the function
        """
        self.name = name
        if type(data) == str:
            self.init_from_string(data)
        else:
            self.data = data
            self.sons = sons[:]
        self.head = self.data
        self.others = [Function(x) for x in self.get_paths_to_leaves()]
        if len(self.others) == 0:
            self.others.append(Function([]))
        self.part0 = self.head.part0
        self.part1 = self.head.part1

    def save_gif(self, filename):
        dot = Digraph("G", filename=filename, format='gif')
        counter = 0
        dot.node(str(counter), str(self.data))
        to_process = []
        for son in self.sons:
            to_process.append((counter, son))
        counter += 1
        while len(to_process) != 0:
            current = to_process.pop()
            dot.node(str(counter), str(current[1].data))
            dot.edge(str(current[0]), str(counter))
            for son in current[1].sons:
                to_process.append((counter, son))
            counter += 1
        dot.render(filename)

    def set_data(self, data):
        """set_data
        Set the data value of the current node
        :param data: The data
        """
        self.data = data
        self.head = self.data
        self.part0 = self.head.part0
        self.part1 = self.head.part1
        self.others = [Function(x) for x in self.get_paths_to_leaves()]
        if len(self.others) == 0:
            self.others.append(Function([]))

    def get_all_nodes(self):
        """get_all_nodes Returns all the nodes in the tree"""
        res = [self.data]
        for son in self.sons:
            res += son.get_all_nodes()
        return res

    def add_son(self, son):
        """add_son
        Adds a son tree to this node
        :param son: A tree
        """
        self.sons.append(son)
        self.others = self.get_all_nodes()

    def is_leave(self):
        """is_leave Gives if we are in a leave"""
        return len(self.sons) == 0

    def get_paths_to_leaves(self, level=0, symbol="-"):
        """get_paths_to_leaves Get all paths to the leaves"""
        if self.is_leave():
            if level == 0:
                return []
            return [self.data.get_inverse_function(symbol)]
        res = []
        for son in self.sons:
            l_relations = self.data.get_inverse_function(symbol)
            for paths in son.get_paths_to_leaves(level + 1, symbol):
                if level > 0:
                    res.append(l_relations + paths)
                else:
                    res.append(paths)
        return res

    def print_tree(self, level=0):
        """print_tree
        Recursive method to get the tree as a string
        :param level: The depth
        """
        res = [" " * level + "|>" + str(self.data)]
        for son in self.sons:
            res += son.print_tree(level + 1)
        if level == 0:
            return '\n'.join(res)
        else:
            return res

    def __repr__(self):
        """__repr__ The string representation of the tree"""
        return self.print_tree()

    def init_from_string(self, s):
        """init_from_string
        Initialize the node from a string
        :param s: the string
        """
        self.data = []
        self.sons = []
        current_node = self
        nodes = []
        current_stack = ""
        s = s.split(":-")
        if len(s) == 2:
            self.name = s[0]
            s = s[1]
        else:
            s = s[0]
        for c in s:
            if c == '(':
                new_node = TreeFunction(Function([]))
                current_node.add_son(new_node)
                nodes.append(current_node)
                current_node = new_node
            elif c == ';':
                if current_stack == "":
                    raise ValueError
                current_node.set_data(Function(current_stack))
                current_node = nodes.pop()
                new_node = TreeFunction(Function([]))
                current_node.add_son(new_node)
                nodes.append(current_node)
                current_node = new_node
                current_stack = ""
            elif c == ')':
                if current_stack == "":
                    raise ValueError
                current_node.set_data(Function(current_stack))
                current_node = nodes.pop()
                current_stack = ""
            elif c != ' ':
                current_stack += c
        if current_stack == "":
            raise ValueError
        self.set_data(Function(current_stack, name=self.name))

    def n_relations(self):
        """n_relations Gives the number of relations in the function"""
        return self.head.n_relations()

    def generate_general_reduced_rules(self, counter, i, j, start):
        """generate_general_reduced_rules
        Generate a middle rule, starting at ci and ending at cj
        :param counter: The counter to avoid collision
        :param i: index of the first relation
        :param j: index of the last relation
        """
        rules = []
        rules.append(DuplicationRule(start,
                                     "A" + str(counter),
                                     "D" + str(counter)))
        temp_counter = counter
        temp = stack(["end"],  # + self.part1[:i],
                     counter + 1,
                     "A" + str(counter),
                     "C")
        counter = temp[1]
        rules = rules + temp[0]
        temp = unstack(self.part0[i:j+1],
                       self.part0,
                       temp_counter,
                       "D" + str(temp_counter),
                       "Cback" + str(temp_counter + self.n_relations() + 1))
        counter = temp[1]
        rules = rules + temp[0]
        counter = max(counter, temp_counter)
        counter += 1
        temp = stack(self.part1[j+1:],
                     counter,
                     "Cback" + str(temp_counter + self.n_relations() + 1),
                     "C")
        counter = temp[1]
        rules = rules + temp[0]
        return (rules, counter)

    def generate_splitting(self, counter, first_nt, also):
        """generate_splitting
        Generate the splitting for the branches
        :param counter: The first index to use to generate rules
        :param first_nt: the first non terminal of the tree (the head)
        """
        rules = []
        initial_counter = counter
        if len(self.others) == 0:
            rules.append(DuplicationRule("C", "T", first_nt))
        elif len(self.others) == 1:
            rules.append(DuplicationRule("C", "CD" + str(counter), first_nt))
        else:
            rules.append(DuplicationRule("C",
                                         "CD" + str(counter),
                                         "K" + str(counter + 1)))
            counter += 1
            for i in range(len(self.others) - 2):
                rules.append(DuplicationRule("K" + str(counter),
                                             "CD" + str(counter),
                                             "K" + str(counter + 1)))
                counter += 1
            rules.append(DuplicationRule("K" + str(counter),
                                         "CD" + str(counter),
                                         first_nt))
        # Stacking
        for i in range(len(self.others)):
            temp = stack(["end"] + self.others[i].part0[::-1] + also,
                         counter,
                         "CD" + str(initial_counter + i),
                         "C")
            counter = temp[1]
            rules = rules + temp[0]
        return (rules, counter)

    def generate_fake_tree_functions(self, counter, empty=False):
        """generate_fake_tree_functions
        Generate all the rules which have part of the sons in it.
        :param counter: A counter to avoid duplicate
        :param empty: Whether to use C[sigma] -> ... or not.
        """
        rules = []
        for f_other in self.others:
            other = f_other.to_list()
            for end in range(1, len(other) + 1):
                new_others = []
                for f_other1 in self.others:
                    other1 = f_other1.to_list()
                    last = 0
                    for e in range(end):
                        last = e
                        if other[e] != other1[e]:
                            break
                        last = e + 1
                    if last != 0:
                        new_others.append(([x + "-"
                                           for x in other[end-1:last-1:-1]] +
                                           other1[last:])[::-1])
                    else:
                        new_others.append(([x + "-" for x in other[end-1::-1]] +
                                           other1[last:])[::-1])
                # TODO Something is not clear with those FakeTreeFunctions
                ft = FakeTreeFunction([x + "-" for x in other[:end]]
                                      + self.head.to_list(),
                                      new_others)
                temp = ft.generate_reduced_rules(counter, empty)
                rules += temp[0]
                counter = temp[1]
        return (rules, counter)

    def generate_reduced_rules(self, counter, empty=False):
        """generate_reduced_rules
        Generates both left and right reduced rules
        :param counter: counter used to be sure we do not duplicate
        non-terminals. So, it MUST be update after the function.
        :return A couple (rules, counter) containing the generated rules and the
        new counter value
        """
        rules = []
        max_i = self.n_relations()
        if empty:
            max_i = 1
        for i in range(0, max_i):
            for j in range(i, self.n_relations()):
                start = "CH" + str(counter)
                temp = self.generate_general_reduced_rules(counter, i, j, start)
                rules = rules + temp[0]
                counter = temp[1]
                temp = self.generate_splitting(counter, start, self.part1[:i])
                counter = temp[1]
                rules = rules + temp[0]
        if empty:
            start = "CH" + str(counter)
            temp = self.generate_general_reduced_rules(counter, 0, -1, start)
            rules = rules + temp[0]
            counter = temp[1]
            temp = self.generate_splitting(counter, start, self.part1[:0])
            counter = temp[1]
            rules = rules + temp[0]
        temp = self.generate_fake_tree_functions(counter, empty)
        rules += temp[0]
        counter = temp[1]
        return (rules, counter)

    def generate_middle_rule_prolog(self, i, j):
        part0 = [r[0] + 'm' * r[1] for r in self.data.relations]
        part1 = [r[0] + 'm' * r[1] for r in self.data.minus_relations]
        part1.reverse()
        new_rule = "p(["
        new_rule += ", ".join(part0[i:j+1])
        new_rule += "|R], Counter, L) "
        new_rule += " :- "
        paths_leaves = self.get_paths_to_leaves(symbol="m")
        counter = 0
        reduction = ""
        if len(paths_leaves) == 0:
            new_rule += " p("
            new_rule += "["
            new_rule += ", ".join(part1[self.n_relations() - i:])
            new_rule += "], Counter - 1, L0), length(L0, K0),"
            reduction = " - K0"
            counter += 1
        else:
            for idx in range(len(paths_leaves)):
                path = paths_leaves[idx]
                new_rule += " p("
                new_rule += "["
                new_rule += ", ".join(path +
                                      part1[self.n_relations() - i:])
                new_rule += "], Counter - 1 " +\
                    reduction + ", L" + str(counter) + "), length(L" +\
                    str(counter) + ", K" +\
                    str(counter) + "),"
                reduction += " - K" + str(counter)
                counter += 1
        new_rule += " p("
        if j != self.n_relations() - 1:
            new_rule += "["
            new_rule += ", ".join(part1[:self.n_relations() - j - 1])
            new_rule += "|R]"
        else:
            new_rule += "R"
        new_rule += ", Counter - 1 " + reduction + ", L" + str(counter) + "), "
        if counter == 1:
            new_rule += "append(L0, [\"" + self.name + "\"|L1], L)."
        else:
            new_rule += "LTEMP0 = [\"(\"], "
            for idx in range(counter):
                if idx == 0:
                    new_rule += "append(LTEMP" + str(idx) +\
                        ", L" + str(idx) + ", LTEMP" + str(idx + 1) +\
                        "), "
                else:
                    new_rule += "append(LTEMP" + str(idx) +\
                        ", [\";\"|L" + str(idx) + "], LTEMP" + str(idx + 1) +\
                        "), "
            new_rule += "append(LTEMP" + str(counter) +\
                ", [\")" + self.name + "\"|L" + str(counter) + "], L)."
        return new_rule

    def generate_fake_tree_functions_prolog(self):
        """generate_fake_tree_functions_prolog Rules from fake trees in
        prolog"""
        rules = []
        for f_other in self.others:
            other = f_other.to_list()
            for end in range(1, len(other) + 1):
                new_others = []
                for f_other1 in self.others:
                    other1 = f_other1.to_list()
                    last = 0
                    for e in range(end):
                        last = e
                        if other[e] != other1[e]:
                            break
                        last = e + 1
                    if last != 0:
                        new_others.append(([x + "-"
                                           for x in other[end-1:last-1:-1]] +
                                           other1[last:])[::-1])
                    else:
                        new_others.append(([x + "-" for x in other[end-1::-1]] +
                                           other1[last:])[::-1])
                ft = FakeTreeFunction([x + "-" for x in other[:end]]
                                      + self.head.to_list(),
                                      new_others, name=self.name)
                rules += ft.get_prolog_rules()
        return rules

    def get_prolog_rules(self):
        rules = []
        max_i = self.n_relations()
        for i in range(0, max_i):
            for j in range(i, self.n_relations()):
                rules.append(self.generate_middle_rule_prolog(i, j))
        rules += self.generate_fake_tree_functions_prolog()
        return rules
