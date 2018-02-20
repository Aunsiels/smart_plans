from consommation_rule import ConsommationRule
from production_rule import ProductionRule
from duplication_rule import DuplicationRule
from function import Function
from fake_tree_function import FakeTreeFunction


class TreeFunction(object):
    """TreeFunction Represents a tree function"""

    def __init__(self, data, sons=[], name="tf"):
        """__init__
        Initialize a tree function. For now, the order of the nodes which are
        not the head is not important.
        :param head: The head of the tree. It is a Function (linear function)
        :param others:
        :param name:
        """
        self.name = name
        if type(data) == str:
            self.init_from_string(data)
        else:
            self.data = data
            self.sons = sons[:]
        self.head = self.data
        self.others = [Function(x) for x in self.get_paths_to_leaves()]
        self.part0 = self.head.part0
        self.part1 = self.head.part1

    def set_data(self, data):
        self.data = data
        self.head = self.data
        self.part0 = self.head.part0
        self.part1 = self.head.part1
        self.others = [Function(x) for x in self.get_paths_to_leaves()]

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

    def get_paths_to_leaves(self, level=0):
        """get_paths_to_leaves Get all paths to the leaves"""
        if self.is_leave():
            if level == 0:
                return []
            return [self.data.get_inverse_function()]
        res = []
        for son in self.sons:
            l_relations = self.data.get_inverse_function()
            for paths in son.get_paths_to_leaves(level + 1):
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
                current_node.set_data(Function(current_stack))
                current_node = nodes.pop()
                new_node = TreeFunction(Function([]))
                current_node.add_son(new_node)
                nodes.append(current_node)
                current_node = new_node
                current_stack = ""
            elif c == ')':
                current_node.set_data(Function(current_stack))
                current_node = nodes.pop()
                current_stack = ""
            elif c != ' ':
                current_stack += c
        self.set_data(Function(current_stack))

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
                temp = stack(["end"] + self.others[i].part0 + also,
                             counter,
                             "CD" + str(initial_counter + i),
                             "C")
                counter = temp[1]
                rules = rules + temp[0]
        return (rules, counter)

    def generate_fake_tree_functions(self, counter, empty=False):
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
                                      new_others)
                temp = ft.generate_reduced_rules(counter)
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


def unstack(u_relations, all_relations, counter, start, end):
    """unstack
    Unstack the given relation from the stack by using reduced forms
    :param u_relations: The relations to unstack
    :param all_relations: All the relations used
    :param counter: Counter to avoid collision
    :param start: the starting non-terminal
    :param end: the ending non-terminal
    """
    rules = []
    if len(u_relations) != 0:
        rules.append(DuplicationRule(start,
                                     "T",
                                     "C" + str(counter)))
    else:
        rules.append(DuplicationRule(start,
                                     "T",
                                     end))
    temp_counter = counter
    if len(u_relations) > 1:
        rules.append(ConsommationRule(u_relations[0],
                                      "C" + str(counter),
                                      "C" + str(counter + 1)))
        counter += 1
    elif len(u_relations) == 1:
        rules.append(ConsommationRule(u_relations[0],
                                      "C" + str(counter),
                                      end))
    for x in range(1, len(u_relations) - 1):
        rules.append(ConsommationRule(u_relations[x],
                                      "C" + str(counter),
                                      "C" + str(counter + 1)))
        counter += 1
    if len(u_relations) > 1:
        rules.append(ConsommationRule(u_relations[-1],
                                      "C" + str(counter),
                                      end))
    for x in range(len(all_relations)):
        temp_counter += 1
    counter = max(temp_counter, counter)
    counter += 1
    return (rules, counter)


def stack(s_relations, counter, start, end):
    """stack
    Stack the given relations on the stack using reduced rules.
    :param s_relations: The relations to stack
    :param counter: The counter to avoid collisions
    :param start: The starting non-terminal
    :param end: The ending non-terminal
    """
    rules = []
    if len(s_relations) == 0:
        rules.append(DuplicationRule(start,
                                     "T",
                                     end))
    elif len(s_relations) == 1:
        rules.append(ProductionRule(start,
                                    end,
                                    s_relations[0]))
    else:
        rules.append(ProductionRule(start,
                                    "A" + str(counter),
                                    s_relations[0]))
    for x in range(1, len(s_relations) - 1):
        rules.append(ProductionRule("A" + str(counter),
                                    "A" + str(counter + 1),
                                    s_relations[x]))
        counter += 1
    if len(s_relations) > 1:
        rules.append(ProductionRule("A" + str(counter),
                                    end,
                                    s_relations[-1]))
    counter += 1
    return (rules, counter)
