import re
from duplication_rule import DuplicationRule
import sys
from utils import stack, unstack


class Function (object):
    """Function
    Represents a linear function
    """

    def init_from_list(self, relations):
        """init_from_list
        Initializes the function from a list of relations
        :param l_relations:
        """
        relations = list(filter(lambda x: len(x) > 0, relations))
        if ("$" in relations or "$m" in relations) and \
                len(relations) > relations.count("$") + relations.count("$m"):
            relations = list(filter(lambda x: x != "$" and x != "$m",
                                    relations))
        # We separate the relation name from its direction by counting "-"
        self.relations = [(re.sub("-", "", r), r.count("-") % 2)
                          for r in relations]
        # We cache the inverse relations
        self.minus_relations = [(re.sub("-", "", r), (r.count("-") + 1) % 2)
                                for r in relations]

    def get_sub_functions(self):
        res = []
        for i in range(1, len(self.relations)):
            f_temp = Function([], self.name + "sub" + str(i))
            f_temp.relations = self.relations[:i]
            f_temp.minus_relations = self.minus_relations[:i]
            f_temp.n_relations = self.n_relations
            f_temp.part0 = self.part0[:i]
            f_temp.part1 = self.part1[:i]
            res.append(f_temp)
        return res


    def init_from_string(self, l_string, name):
        """init_from_string
        Initialization if a string description is given
        :param l_string: the string describing the function, in a prolog-like
        form (f :- r1, r2, rn.
        """
        l0 = l_string.split(":-")
        if len(l0) > 2 or len(l0) == 0:
            sys.exit("Wrong line: " + l_string)
        if len(l0) == 2:
            self.name = re.sub("\s+", ",", l0[0].strip())
            relations = [re.sub("\s+", ",", s.strip())
                         for s in re.sub("\.", "", l0[1]).split(",")]
            if len(relations) == 0:
                sys.exit("No relation: " + l_string)
        else:
            self.name = name
            relations = [re.sub("\s+", ",", s.strip())
                         for s in re.sub("\.", "", l0[0]).split(",")]
            if len(relations) == 0:
                sys.exit("No relation: " + l_string)
        self.init_from_list(relations)

    def __init__(self, relations, name="f", outputs=None):
        """__init__
        Creates the function represented by a sequence of relations
        :param relations: the sequence of relations in the function, inverse
        relations are represented with a -, e.g. r-
        :param name: The name of the function
        """
        self.name = ""
        if type(relations) == str and len(relations.strip()) > 0:
            self.init_from_string(relations, name)
        elif type(relations) == list:
            self.name = name
            self.init_from_list(relations)
        elif type(relations) == Function:
            self.name = relations.name
            self.relations = relations.relations
            self.minus_relations = relations.minus_relations
        else:
            self.relations = []
            self.minus_relations = []
        self.part0 = [r[0] + 'm' * r[1] for r in self.relations]
        self.part1 = [r[0] + 'm' * r[1] for r in self.minus_relations]
        self.n_inputs = 1
        self.inputs = set()
        if outputs is None:
            self.outputs = [len(self.part0) - 1]
        else:
            self.outputs = list(outputs)

    def get_inverse_function(self, symbol="-"):
        """get_inverse_function Get the list representation of the inverse
        function"""
        return [r[0] + symbol * r[1] for r in self.minus_relations[::-1]]

    def to_list(self, symbol="-"):
        """to_list Gives the list representation of the function"""
        return [r[0] + symbol * r[1] for r in self.relations]

    def n_relations(self):
        """n_relations Gives the number of relations in the function"""
        return len(self.relations)

    def __repr__(self):
        """__repr__ String representation of a function"""
        return self.to_string()

    def __eq__(self, other):
        return self.relations == other.relations and \
            self.n_inputs == other.n_inputs

    def __neq__(self, other):
        return self.relations != other.relations or \
            self.n_inputs != other.n_inputs

    def __hash__(self):
        return hash(frozenset(self.relations))

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
        """generate_middle_rules Generates Prolog middle rules"""
        rules = []
        for i in range(self.n_relations()):
            for j in range(i, self.n_relations()):
                rules.append(self.generate_middle_rules_sub(i, j))
        return rules

    def generate_middle_rules_sub(self, i, j):
        """generate_middle_rules_sub
        Generates the general middle rules
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
                temp = self.generate_general_reduced_rules(counter, i, j)
                rules = rules + temp[0]
                counter = temp[1]
        if empty:
            temp = self.generate_general_reduced_rules(counter, 0, -1)
            rules = rules + temp[0]
            counter = temp[1]
        return (rules, counter)

    def generate_palindrome_rules(self, counter, susie=False):
        rules = []
        temp = stack(self.part1,
                     counter,
                     "Cforward",
                     "Cforward")
        counter = temp[1]
        rules = rules + temp[0]
        last = "Cbackward"
        if susie:
            last = "Cend"
        temp = unstack(self.part0,
                       self.part0,
                       counter,
                       "Cbackward",
                       last)
        counter = temp[1]
        rules = rules + temp[0]
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
                                               '-' * r[1]
                                               for r in self.relations]) + ".\n"

    def get_last(self):
        """get_last Gets the last relation of the function"""
        return self.relations[-1][0] + '-' * self.relations[-1][1]

    def get_prolog_rules(self):
        """get_prolog_rules generates the prolog rules"""
        return self.generate_middle_rules()

    def add_to_fsm(self, fsm):
        """add_to_fsm
        Adds the function to an FSM
        :param fsm: The fsm to which we add the function
        :return: The FSM
        """
        final = fsm.get_next_state()
        if fsm.finals:
            final = fsm.finals[0]
        fsm.add_final(final)
        current = fsm.initial
        for i in range(len(self.relations) - 1):
            next_node = fsm.get_next_state()
            if i in self.inputs:
                fsm.add_transition(current,
                                   next_node,
                                   self.relations[i][0] + "_IN" +
                                   self.relations[i][1] * "m")
            else:
                fsm.add_transition(current,
                                   next_node,
                                   self.relations[i][0] + "_OUT" +
                                   self.relations[i][1] * "m")
            current = next_node
            if i in self.outputs:
                fsm.add_final(next_node)
        last = len(self.relations) - 1
        # Normally this is stupid...
        if last in self.inputs:
            fsm.add_transition(current,
                               final,
                               self.relations[last][0] + "_IN" +
                               self.relations[last][1] * "m")
        else:
            fsm.add_transition(current,
                               final,
                               self.relations[last][0] + "_OUT" +
                               self.relations[last][1] * "m")
        return fsm
