# This is for experiment purposes, it does not work

import re
from function import Function


class HornRule (object):
    """Rule Represent an equivalence rule"""

    def __init__(self, l0, l1, name):
        """__init__
        Initializes the class
        :param l0: one side of the equivalence
        :param l1: the other side of the equivalence
        """
        self.relations = [0, 0]
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
            " => " +\
            " -> ".join([r[0] + '-' * r[1] for r in self.relations[1]])
