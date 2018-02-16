from consommation_rule import ConsommationRule
from production_rule import ProductionRule
from duplication_rule import DuplicationRule


class TreeFunction(object):
    """TreeFunction Represents a tree function"""

    def __init__(self, head, others, name="tf"):
        self.head = head
        self.others = others
        self.part0 = head.part0
        self.part1 = head.part1

    def __repr__(self):
        return "HEAD : " + str(self.head) + " OTHERS : " + str(self.others)

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

    def generate_splitting(self, counter, first_nt):
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
            for i in range(len(self.others)):
                temp = stack(["end"] + self.others[i].part1,
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
        start = "CH" + str(counter)
        max_i = self.n_relations()
        if empty:
            max_i = 1
        for i in range(0, max_i):
            for j in range(i, self.n_relations()):
                temp = self.generate_general_reduced_rules(counter, i, j, start)
                rules = rules + temp[0]
                counter = temp[1]
        if empty:
            temp = self.generate_general_reduced_rules(counter, 0, -1, start)
            rules = rules + temp[0]
            counter = temp[1]
        temp = self.generate_splitting(counter, start)
        counter = temp[1]
        rules = rules + temp[0]
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
