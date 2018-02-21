from duplication_rule import DuplicationRule
from function import Function
from utils import stack, unstack


class MultipleInputFunction (Function):
    """MultipleInputFunction
    Represents a multiple input function
    """

    def __init__(self, relations, name, n_inputs):
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
        if type(n_inputs) == int:
            self.n_inputs = n_inputs
            self.inputs = set(range(n_inputs - 1))
        else:
            self.n_inputs = max(n_inputs)
            self.inputs = set(n_inputs)

    def to_string(self):
        """to_string Gives the string representation of the function"""
        return self.name + " :- " + \
            " -> ".join([r[0] + '-' * r[1] for r in self.relations]) +\
            " " + str(self.n_inputs) + " inputs"

    def get_part0_combinations(self, i, j):
        """get_part0_combinations
        Function for implementation purposes
        :param i: Begin
        :param j: End
        """
        if i >= j:
            return [[]]
        temp = []
        for p in self.get_part0_combinations(i+1, j):
            # if i >= self.n_inputs - 1:
            if i not in self.inputs:
                temp.append([self.part0[i]] + p)
            temp.append([self.part0[i] + "_IN"] + p)
        return temp

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
        for p in self.get_part0_combinations(i, j+1):
            temp = unstack(p,
                           self.part0,
                           temp_counter,
                           "D" + str(temp_counter),
                           "Cback" + str(temp_counter + self.n_relations() + 1))
            counter = temp[1]
            rules = rules + temp[0]
        counter = max(counter, temp_counter)
        counter += 1
        part1_temp = [p + "_IN" for p in self.part1[j+1:]]
        temp = stack(part1_temp,
                     counter,
                     "Cback" + str(temp_counter + self.n_relations() + 1),
                     "C")
        counter = temp[1]
        rules = rules + temp[0]
        return (rules, counter)

    def generate_reduced_rules(self, counter, empty=False):
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
            for j in range(max(i, self.n_inputs - 1), self.n_relations()):
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
