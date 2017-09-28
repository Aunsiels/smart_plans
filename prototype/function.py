import re
from consommation_rule import ConsommationRule
from end_rule import EndRule
from production_rule import ProductionRule
from duplication_rule import DuplicationRule
import sys


class Function (object):
    """Function
    Represents a linear function
    """

    def init_from_list(self, relations):
        """init_from_list
        Initializes the function from a list of relations
        :param l_relations:
        """
        # We separate the relation name from its direction by counting "-"
        self.relations = [(re.sub("-", "", r), r.count("-") % 2)
                          for r in relations]
        # We cache the inverse relations
        self.minus_relations = [(re.sub("-", "", r), (r.count("-") + 1) % 2)
                                for r in relations]

    def init_from_string(self, l_string):
        l0 = l_string.split(":-")
        if len(l0) != 2:
            sys.exit("Wrong line: " + l_string)
        self.name = re.sub("\s+", ",", l0[0].strip())
        relations = [re.sub("\s+", ",", s.strip())
                     for s in re.sub("\.", "", l0[1]).split(",")]
        if len(relations) == 0:
            sys.exit("No relation: " + l_string)
        self.init_from_list(relations)

    def __init__(self, relations, name):
        """__init__
        Creates the function represented by a sequence of relations
        :param relations: the sequence of relations in the function, inverse
        relations are represented with a -, e.g. r-
        :param name: The name of the function
        """
        if type(relations) == str:
            self.init_from_string(relations)
        else:
            self.name = name
            self.init_from_list(relations)

    def n_relations(self):
        """n_relations Gives the number of relations in the function"""
        return len(self.relations)

    def __repr__(self):
        return self.to_string()

    def to_string(self):
        """to_string Gives the string representation of the function"""
        return self.name + " :- " + \
            " -> ".join([r[0] + '-' * r[1] for r in self.relations])

    def generate_left_rules(self):
        """generate_left_rules
        Generates the left rules as described in the paper, in non-reduced form
        Here the output is a prolog rule
        """
        part0 = [r[0] + 'm' * r[1] for r in self.relations]
        part1 = [r[0] + 'm' * r[1] for r in self.minus_relations]
        part1.reverse()
        rules = []
        # for i in range(self.n_relations() + 1): # With loops
        for i in range(1, self.n_relations() + 1):
            if i != 0:
                new_rule = "p(["
                new_rule += ", ".join(part0[:i])
                new_rule += "|R], Counter, [\"" + self.name + "\"|L]) :- "
            else:
                new_rule = "p(R, Counter, [\"" + self.name + "\"|L]) :- "
            if i != self.n_relations():
                new_rule += "p(["
                new_rule += ", ".join(part1[:self.n_relations() - i])
                new_rule += "|R], Counter - 1, L)."
            else:
                new_rule += "p(R, Counter - 1, L)."
            rules.append(new_rule)
        return rules

    def generate_right_rules(self):
        """generate_right_rules
        Generates the right rules as described in the paper, in non-reduced form
        Here the output is a prolog rule
        """
        part0 = [r[0] + 'm' * r[1] for r in self.relations]
        part1 = [r[0] + 'm' * r[1] for r in self.minus_relations]
        part1.reverse()
        rules = []
        # for i in range(1, self.n_relations() + 1): # With loops
        for i in range(1, self.n_relations()):
            if i != self.n_relations():
                new_rule = "p(["
                new_rule += ", ".join(part0[i:])
                new_rule += "|R], Counter, L) "
            else:
                new_rule = "p(R, Counter, L) "
            new_rule += " :- p(["
            new_rule += ", ".join(part1[self.n_relations() - i:])
            new_rule += "], Counter - 1, L1), length(L1, K), " + \
                "p(R, Counter - K - 1, L2), "
            new_rule += "append(L1, [\"" + self.name + "\"|L2], L)."
            rules.append(new_rule)
        return rules

    def generate_left_reduced_rules(self, counter):
        """generate_left_reduced_rules
        Generates the reduced left rules as describe in the paper.
        :param counter: counter used to be sure we do not duplicate
        non-terminals. So, it MUST be update after the function.
        :return A couple (rules, counter) containing the generated rules and the
        new counter value
        """
        part0 = [r[0] + 'm' * r[1] for r in self.relations]
        part1 = [r[0] + 'm' * r[1] for r in self.minus_relations]
        rules = []
        for i in range(1, self.n_relations() + 1):
            rules.append(ConsommationRule(part0[0], "C", "B" + str(counter)))
            if 1 != self.n_relations():
                rules.append(DuplicationRule("B" + str(counter),
                                             "A" + str(counter),
                                             "C" + str(counter + 1)))
                rules.append(EndRule("A" + str(counter), part0[0]))
                counter += 1
            else:
                rules.append(DuplicationRule("B" + str(counter),
                                             "A" + str(counter),
                                             "Cback" + str(counter)))
                rules.append(EndRule("A" + str(counter), part0[0]))
            for x in range(1, self.n_relations() - 1):
                if x < i:
                    rules.append(ConsommationRule(part0[x],
                                                  "C" + str(counter),
                                                  "B" + str(counter)))
                    rules.append(DuplicationRule("B" + str(counter),
                                                 "A" + str(counter),
                                                 "C" + str(counter + 1)))
                    rules.append(EndRule("A" + str(counter), part0[x]))
                else:
                    rules.append(DuplicationRule("C" + str(counter),
                                                 "A" + str(counter),
                                                 "C" + str(counter + 1)))
                    rules.append(EndRule("A" + str(counter), part0[x]))
                counter += 1
            if 1 != self.n_relations():
                if i == self.n_relations():
                    rules.append(ConsommationRule(part0[-1],
                                                  "C" + str(counter),
                                                  "B" + str(counter)))
                    rules.append(DuplicationRule("B" + str(counter),
                                                 "A" + str(counter),
                                                 "Cback" + str(counter)))
                    rules.append(EndRule("A" + str(counter), part0[-1]))
                else:
                    rules.append(DuplicationRule("C" + str(counter),
                                                 "A" + str(counter),
                                                 "Cback" + str(counter)))
                    rules.append(EndRule("A" + str(counter), part0[-1]))
            rules.append(DuplicationRule("Cback" + str(counter),
                                         "Cback" + str(counter + 1),
                                         "T"))
            counter += 1
            counter += 1
            for x in range(i, self.n_relations()):
                rules.append(ProductionRule("Cback" + str(counter - 1),
                                            "Cback" + str(counter),
                                            part1[x]))
                counter += 1
            rules.append(DuplicationRule("Cback" + str(counter - 1),
                                         "C",
                                         "T"))
            counter += 1
        return (rules, counter)

    def generate_right_reduced_rules(self, counter):
        """generate_right_reduced_rules
        Generates the reduced right rules as describe in the paper.
        :param counter: counter used to be sure we do not duplicate
        non-terminals. So, it MUST be update after the function.
        :return A couple (rules, counter) containing the generated rules and the
        new counter value
        """
        part0 = [r[0] + 'm' * r[1] for r in self.relations]
        part1 = [r[0] + 'm' * r[1] for r in self.minus_relations]
        rules = []
        for i in range(1, self.n_relations()):
            rules.append(ConsommationRule(part0[i], "C", "B" + str(counter)))
            rules.append(DuplicationRule("B" + str(counter),
                                         "A" + str(counter),
                                         "D" + str(counter)))
            temp_counter = counter
            rules.append(ProductionRule("A" + str(counter),
                                        "A" + str(counter + 1),
                                        "end"))
            counter += 1
            for x in range(i - 1):
                rules.append(ProductionRule("A" + str(counter),
                                            "A" + str(counter + 1),
                                            part1[x]))
                counter += 1
            rules.append(ProductionRule("A" + str(counter),
                                        "C",
                                        part1[i - 1]))
            counter += 1
            if i != self.n_relations() - 1:
                rules.append(DuplicationRule("D" + str(temp_counter),
                                             "E" + str(temp_counter),
                                             "C" + str(temp_counter)))
            else:
                rules.append(DuplicationRule("D" + str(temp_counter),
                                             "E" + str(temp_counter),
                                             "C"))
            temp_counter2 = temp_counter
            for x in range(i + 1, self.n_relations() - 1):
                rules.append(ConsommationRule(part0[x],
                                              "C" + str(temp_counter),
                                              "C" + str(temp_counter + 1)))
                temp_counter += 1
            if i != self.n_relations() - 1:
                rules.append(ConsommationRule(part0[-1],
                                              "C" + str(temp_counter),
                                              "C"))
            for x in range(self.n_relations()):
                rules.append(DuplicationRule("E" + str(temp_counter2),
                                             "F" + str(temp_counter2),
                                             "E" + str(temp_counter2 + 1)))
                rules.append(EndRule("F" + str(temp_counter2), part0[x]))
                temp_counter2 += 1
            rules.append(EndRule("E" + str(temp_counter2), "epsilon"))
            counter = max(temp_counter, counter)
            counter = max(counter, temp_counter2)
            counter += 1
        return (rules, counter)

    def generate_reduced_rules(self, counter):
        """generate_reduced_rules
        Generates both left and right reduced rules
        :param counter: counter used to be sure we do not duplicate
        non-terminals. So, it MUST be update after the function.
        :return A couple (rules, counter) containing the generated rules and the
        new counter value
        """
        l_rules = self.generate_left_reduced_rules(counter)
        counter = l_rules[1]
        r_rules = self.generate_right_reduced_rules(counter)
        return (l_rules[0] + r_rules[0], r_rules[1])

    def get_all_terminals(self):
        """get_all_terminals Returns all terminals used and their opposite"""
        s0 = set([r[0] for r in self.relations])
        s1 = set([r[0] + 'm' for r in self.relations])
        return s0.union(s1)

    def get_prolog(self):
        """get_prolog Generate a string which represents the function as a
        prolog rule"""
        return self.name + " :- " + ", ".join([r[0] +
                                               'm' * r[1]
                                               for r in self.relations]) + ".\n"

    def get_last(self):
        return self.relations[-1][0] + 'm' * self.relations[-1][1]


def test():
    """test Performs some basic tests"""
    relations = ['a', 'b--', 'c-']
    f = Function(relations, "f1")
    print("The function is:")
    print(f.to_string())
    assert(f.n_relations() == 3)
    print("Rules:")
    print(f.generate_left_rules())
    print(f.generate_right_rules())
    print("Left reduced rules")
    left_red = f.generate_left_reduced_rules(0)
    for rule in left_red[0]:
        print(rule)
    print(left_red[1])
    print("Right reduced rules")
    right_red = f.generate_right_reduced_rules(0, ["a", "b", "c", "am", "bm",
                                                   "cm"])
    for rule in right_red[0]:
        print(rule)
    print(right_red[1])
    print("All is good")


# test()
