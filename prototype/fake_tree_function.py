from duplication_rule import DuplicationRule
from function import Function
from utils import stack, unstack


class FakeTreeFunction(object):
    """FakeTreeFunction Represents a faketree function -  For implementation
    purposes"""

    def __init__(self, head, others, name="tf"):
        """__init__
        Initialize a fake tree function. For now, the order of the nodes which
        are not the head is not important.
        :param head: The head of the tree. It is a path
        :param others: The other paths
        :param name:
        """
        self.head = Function(head)
        self.others = [Function(x) for x in others]
        self.part0 = self.head.part0
        self.part1 = self.head.part1
        self.name = name

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

    def generate_reduced_rules(self, counter, empty=False):
        """generate_reduced_rules
        Generates both left and right reduced rules
        :param counter: counter used to be sure we do not duplicate
        non-terminals. So, it MUST be update after the function.
        :return A couple (rules, counter) containing the generated rules and the
        new counter value
        """
        rules = []
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
        # TODO Do I need it?
        if empty:
            start = "CH" + str(counter)
            temp = self.generate_general_reduced_rules(counter, 0, -1, start)
            rules = rules + temp[0]
            counter = temp[1]
            temp = self.generate_splitting(counter, start, self.part1[:0])
            counter = temp[1]
            rules = rules + temp[0]
        return (rules, counter)
