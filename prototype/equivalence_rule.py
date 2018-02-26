# This is for experiment purposes, it does not work

import re
from function import Function


class EquivalenceRule (object):
    """Rule Represent an equivalence rule"""

    def __init__(self, l0, l1, name):
        """__init__
        Initializes the class
        :param l0: one side of the equivalence
        :param l1: the other side of the equivalence
        """
        self.relations = [0, 0]
        self.minus_relations = [0, 0]
        self.init_from_list(l0, 0)
        self.init_from_list(l1, 1)
        self.l0 = [r[0] + "-" * r[1] for r in self.relations[0]]
        self.l1 = [r[0] + "-" * r[1] for r in self.relations[1]]
        self.name = name

    def init_from_list(self, relations, side):
        """init_from_list
        Initializes the function from a list of relations
        :param l_relations:
        """
        # We separate the relation name from its direction by counting "-"
        self.relations[side] = [(re.sub("-", "", r), r.count("-") % 2)
                                for r in relations]
        # We cache the inverse relations
        self.minus_relations[side] = [(re.sub("-", "", r), (r.count("-") + 1)
                                       % 2)
                                      for r in relations]

    def n_relations(self):
        """n_relations Gives the number of relations in the function"""
        return len(self.relations[0]) + len(self.relations[1])

    def __repr__(self):
        """__repr__ Representation of the Equivalence Rule"""
        return self.to_string()

    def to_string(self):
        """to_string Gives the string representation of the function"""
        return self.name + " :- " + \
            " -> ".join([r[0] + '-' * r[1] for r in self.relations[0]]) +\
            " <=> " +\
            " -> ".join([r[0] + '-' * r[1] for r in self.relations[1]])

    def transform_function_set(self, functions):
        """transform_function_set
        Transform the function to create new ones with the equivalence
        included
        :param functions: a set of functions
        """
        final_functions = set()
        to_process = []
        counter = 0
        # We initialize the stack of function to process. The elements have the
        # form (function, start, length_first)
        for function in functions:
            l_function = function.to_list()
            to_process.append((l_function, 0, len(l_function)))
            final_functions.add(Function(l_function, "f" + str(counter)))
            counter += 1
        # We process the functions
        while len(to_process) != 0:
            function = to_process.pop()
            # If we go too far
            if function[1] >= function[2]:
                continue
            # Do we need to consider longer functions?
            if len(self.l0) + function[1] > len(function[0]) or \
                    len(self.l1) + function[1] > len(function[0]):
                for f_temp in functions:
                    to_process.append((function[0] + f_temp.to_list(),
                                       function[1],
                                       function[2]))
            # First l0
            if len(self.l0) + function[1] <= len(function[0]):
                if function[0][function[1]:function[1] + len(self.l0)] == \
                        self.l0:
                    final_functions.add(Function(function[0][:function[1]] +
                                                 self.l1 +
                                                 function[0][function[1] +
                                                             len(self.l0):],
                                                 "f" + str(counter)))
                    counter += 1
            # Same for l1
            if len(self.l1) + function[1] <= len(function[0]):
                if function[0][function[1]:function[1] + len(self.l1)] == \
                        self.l1:
                    final_functions.add(Function(function[0][:function[1]] +
                                                 self.l0 +
                                                 function[0][function[1] +
                                                             len(self.l1):],
                                                 "f" + str(counter)))
                    counter += 1
            # Add one step futher
            to_process.append((function[0],
                               function[1] + 1,
                               function[2]))
        return list(final_functions)

    def get_all_terminals(self):
        """get_all_terminals Returns all terminals used and their opposite"""
        s0 = set([r[0] for r in self.relations[0]])
        s1 = set([r[0] + 'm' for r in self.relations[0]])
        s2 = set([r[0] for r in self.relations[1]])
        s3 = set([r[0] + 'm' for r in self.relations[1]])
        return s0.union(s1).union(s2).union(s3)
