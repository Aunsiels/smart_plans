import re
from production_rule import ProductionRule
from consommation_rule import ConsommationRule


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
        return self.to_string()

    def to_string(self):
        """to_string Gives the string representation of the function"""
        return self.name + " :- " + \
            " -> ".join([r[0] + '-' * r[1] for r in self.relations[0]]) +\
            " <=> " +\
            " -> ".join([r[0] + '-' * r[1] for r in self.relations[1]])

    def generate_non_minus(self, counter):
        part0 = [0, 0]
        part0[0] = [r[0] + 'm' * r[1] for r in self.relations[0]]
        part0[1] = [r[0] + 'm' * r[1] for r in self.relations[1]]
        rules = []
        rules.append(ConsommationRule(part0[0][0], "C", "C" + str(counter)))
        for i in range(1, len(part0[0])):
            rules.append(ConsommationRule(part0[0][i], "C" + str(counter),
                                          "C" + str(counter + 1)))
            counter += 1
        for i in range(len(part0[1]) - 1, 0, -1):
            rules.append(ProductionRule("C" + str(counter),
                                        "C" + str(counter + 1),
                                        part0[1][i]))
            counter += 1
        rules.append(ProductionRule("C" + str(counter),
                                    "C",
                                    part0[1][0]))
        counter += 1
        rules.append(ConsommationRule(part0[1][0], "C", "C" + str(counter)))
        for i in range(1, len(part0[1])):
            rules.append(ConsommationRule(part0[1][i], "C" + str(counter),
                                          "C" + str(counter + 1)))
            counter += 1
        for i in range(len(part0[0]) - 1, 0, -1):
            rules.append(ProductionRule("C" + str(counter),
                                        "C" + str(counter + 1),
                                        part0[0][i]))
            counter += 1
        rules.append(ProductionRule("C" + str(counter),
                                    "C",
                                    part0[0][0]))
        counter += 1
        return (rules, counter)

    def generate_minus(self, counter):
        part0 = [0, 0]
        part0[0] = [r[0] + 'm' * r[1] for r in self.minus_relations[0]]
        part0[0].reverse()
        part0[1] = [r[0] + 'm' * r[1] for r in self.minus_relations[1]]
        part0[1].reverse()
        rules = []
        rules.append(ConsommationRule(part0[0][0], "C", "C" + str(counter)))
        for i in range(1, len(part0[0])):
            rules.append(ConsommationRule(part0[0][i], "C" + str(counter),
                                          "C" + str(counter + 1)))
            counter += 1
        for i in range(len(part0[1]) - 1, 0, -1):
            rules.append(ProductionRule("C" + str(counter),
                                        "C" + str(counter + 1),
                                        part0[1][i]))
            counter += 1
        rules.append(ProductionRule("C" + str(counter),
                                    "C",
                                    part0[1][0]))
        counter += 1
        rules.append(ConsommationRule(part0[1][0], "C", "C" + str(counter)))
        for i in range(1, len(part0[1])):
            rules.append(ConsommationRule(part0[1][i], "C" + str(counter),
                                          "C" + str(counter + 1)))
            counter += 1
        for i in range(len(part0[0]) - 1, 0, -1):
            rules.append(ProductionRule("C" + str(counter),
                                        "C" + str(counter + 1),
                                        part0[0][i]))
            counter += 1
        rules.append(ProductionRule("C" + str(counter),
                                    "C",
                                    part0[0][0]))
        counter += 1
        return (rules, counter)

    def generate_reduced_rules(self, counter):
        l_rules = self.generate_minus(counter)
        counter = l_rules[1]
        r_rules = self.generate_non_minus(counter)
        return (l_rules[0] + r_rules[0], r_rules[1])

    def get_all_terminals(self):
        """get_all_terminals Returns all terminals used and their opposite"""
        s0 = set([r[0] for r in self.relations[0]])
        s1 = set([r[0] + 'm' for r in self.relations[0]])
        s2 = set([r[0] for r in self.relations[1]])
        s3 = set([r[0] + 'm' for r in self.relations[1]])
        return s0.union(s1).union(s2).union(s3)
