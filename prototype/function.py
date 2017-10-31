import re
from consommation_rule import ConsommationRule
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
        """init_from_string
        Initialization if a string description is given
        :param l_string: the string describing the function, in a prolog-like
        form (f :- r1, r2, rn.
        """
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
        self.part0 = [r[0] + 'm' * r[1] for r in self.relations]
        self.part1 = [r[0] + 'm' * r[1] for r in self.minus_relations]

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

    def generate_middle_rules(self):
        rules = []
        for i in range(self.n_relations()):
            for j in range(i, self.n_relations()):
                rules.append(self.generate_middle_rules_sub(i, j))
        return rules

    def generate_middle_rules_sub(self, i, j):
        """generate_middle_rules
        Generate the general middle rules
        :param i: The beginning index
        :param j: The ending symbol
        """
        part0 = [r[0] + 'm' * r[1] for r in self.relations]
        part1 = [r[0] + 'm' * r[1] for r in self.minus_relations]
        part1.reverse()
        new_rule = "p(["
        new_rule += ", ".join(part0[i:j+1])
        new_rule += "|R], Counter, L) "
        new_rule += " :- p("
        new_rule += "["
        new_rule += ", ".join(part1[self.n_relations() - i:])
        new_rule += "], Counter - 1, L1), length(L1, K), p("
        if j != self.n_relations() - 1:
            new_rule += "["
            new_rule += ", ".join(part1[:self.n_relations() - j - 1])
            new_rule += "|R]"
        else:
            new_rule += "R"
        new_rule += ", Counter - K - 1, L2), "
        new_rule += "append(L1, [\"" + self.name + "\"|L2], L)."
        return new_rule

    def generate_left_reduced_rules(self, counter):
        """generate_left_reduced_rules
        Generates the reduced left rules as describe in the paper.
        :param counter: counter used to be sure we do not duplicate
        non-terminals. So, it MUST be update after the function.
        :return A couple (rules, counter) containing the generated rules and the
        new counter value
        """
        rules = []
        for i in range(1, self.n_relations() + 1):
            temp = unstack(self.part0[0:i],
                           self.part0,
                           counter,
                           "C",
                           "Cback" + str(counter + self.n_relations() + 1))
            counter = temp[1]
            rules = rules + temp[0]
            temp = stack(self.part1[i:],
                         counter,
                         "Cback" + str(counter),
                         "C")
            counter = temp[1]
            rules = rules + temp[0]
        return (rules, counter)

    def generate_right_reduced_rules(self, counter):
        """generate_right_reduced_rules
        Generates the reduced right rules as describe in the paper.
        :param counter: counter used to be sure we do not duplicate
        non-terminals. So, it MUST be update after the function.
        :return A couple (rules, counter) containing the generated rules and the
        new counter value
        """
        rules = []
        for i in range(1, self.n_relations()):
            rules.append(DuplicationRule("C",
                                         "A" + str(counter),
                                         "D" + str(counter)))
            temp_counter = counter
            temp = stack(["end"] + self.part1[:i],
                         counter,
                         "A" + str(counter),
                         "C")
            counter = temp[1]
            rules = rules + temp[0]
            temp = unstack(self.part0[i:self.n_relations()],
                           self.part0,
                           temp_counter,
                           "D" + str(temp_counter),
                           "C")
            counter = temp[1]
            rules = rules + temp[0]
            counter = max(counter, temp_counter)
            counter += 1
        return (rules, counter)

    def generate_general_reduced_rules(self, counter, i, j):
        """generate_general_reduced_rules
        Generate a middle rule, starting at ci and ending at cj
        :param counter: The counter to avoid collision
        :param i: index of the first relation
        :param j: index of the last relation
        """
        rules = []
        rules.append(DuplicationRule("C",
                                     "A" + str(counter),
                                     "D" + str(counter)))
        temp_counter = counter
        temp = stack(["end"] + self.part1[:i],
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

    def generate_reduced_rules(self, counter):
        """generate_reduced_rules
        Generates both left and right reduced rules
        :param counter: counter used to be sure we do not duplicate
        non-terminals. So, it MUST be update after the function.
        :return A couple (rules, counter) containing the generated rules and the
        new counter value
        """
        # l_rules = self.generate_left_reduced_rules(counter)
        # counter = l_rules[1]
        # r_rules = self.generate_right_reduced_rules(counter)
        # return (l_rules[0] + r_rules[0], r_rules[1])
        rules = []
        for i in range(0, self.n_relations()):
            for j in range(i, self.n_relations()):
                temp = self.generate_general_reduced_rules(counter, i, j)
                rules = rules + temp[0]
                counter = temp[1]
        return (rules, counter)

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
        """get_last Gets the last relation of the function"""
        return self.relations[-1][0] + 'm' * self.relations[-1][1]


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
