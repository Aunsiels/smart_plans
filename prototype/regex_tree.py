import utils
from duplication_rule import DuplicationRule
from function import Function
from production_rule import ProductionRule
import function


class RegexTree(object):

    def post_processing(self):
        new_sons = []
        for son in self.sons:
            if type(son.head) == function.Function and \
                    son.head.n_relations() == 0:
                continue
            else:
                son.post_processing()
                new_sons.append(son)
        self.sons = new_sons

    def __init__(self, head, sons=[], name="regf"):
        self.name = name
        if type(head) == str and head == "":
            self.head = Function([])
            self.sons = sons[:]
            self.original_string = ""
        elif type(head) == str and head != "|" and head != "*" and head != ".":
            self.init_from_string(head)
            self.original_string = head
            self.post_processing()
        else:
            self.head = head
            self.sons = sons[:]
            self.original_string = ""

    def add_son(self, son):
        self.sons.append(son)

    def consume_tree(self, first, last, counter):
        rules = []
        if type(self.head) != str:
            return utils.unstack(self.head.part0, [], counter, first, last)
        elif self.head == ".":
            temp_nt = [first]
            for _ in range(len(self.sons)):
                temp_nt.append("C" + str(counter))
                counter += 1
            for i in range(len(self.sons)):
                temp = self.sons[i].consume_tree(temp_nt[i],
                                                 temp_nt[i+1],
                                                 counter)
                rules += temp[0]
                counter = temp[1]
                rules.append(DuplicationRule(temp_nt[-1], "T", last))
            return (rules, counter)
        elif self.head == "|":
            for son in self.sons:
                temp = son.consume_tree(first, last, counter)
                rules += temp[0]
                counter = temp[1]
            return (rules, counter)
        elif self.head == "*":
            rules.append(DuplicationRule(first, "T", last))
            # Normally just one
            for son in self.sons:
                temp = son.consume_tree(last, last, counter)
                rules += temp[0]
                counter = temp[1]
            return (rules, counter)

    def push_tree(self, first, last, counter, end=False):
        rules = []
        if end:
            rules.append(ProductionRule(first, "Ce" + str(counter), "end"))
            first = "Ce" + str(counter)
        if type(self.head) != str:
            res = utils.stack(self.head.part1, counter, first, last)
            rules += res[0]
            counter = res[1]
            return (rules, counter)
        elif self.head == ".":
            temp_nt = [first]
            for _ in range(len(self.sons)):
                temp_nt.append("C" + str(counter))
                counter += 1
            for i in range(len(self.sons)):
                temp = self.sons[i].push_tree(temp_nt[i],
                                              temp_nt[i+1],
                                              counter)
                rules += temp[0]
                counter = temp[1]
                rules.append(DuplicationRule(temp_nt[-1], "T", last))
            return (rules, counter)
        elif self.head == "|":
            for son in self.sons:
                temp = son.push_tree(first, last, counter)
                rules += temp[0]
                counter = temp[1]
            return (rules, counter)
        elif self.head == "*":
            rules.append(DuplicationRule(first, "T", last))
            # Normally just one
            for son in self.sons:
                temp = son.push_tree(last, last, counter)
                rules += temp[0]
                counter = temp[1]
            return (rules, counter)

    def get_parenthesis_after(self, s, begin):
        # Considered well parenthesis
        counter = 1
        for i in range(begin + 1, len(s)):
            if s[i] == "(":
                counter += 1
            elif s[i] == ")":
                counter -= 1
            if counter == 0:
                return i

    def print_tree(self, level=0):
        """print_tree
        Recursive method to get the tree as a string
        :param level: The depth
        """
        res = [" " * level + "|>" + str(self.head)]
        for son in self.sons:
            res += son.print_tree(level + 1)
        if level == 0:
            return '\n'.join(res)
        else:
            return res

    def __repr__(self):
        """__repr__ The string representation of the tree"""
        return self.print_tree()

    def preprocess(self, s):
        res = []
        for i in range(len(s)):
            if i + 1 < len(s) and \
                    (s[i + 1] == "|" or s[i+1] == "*") and s[i] != ")":
                res.append("(")
                res.append(s[i])
                res.append(")")
            elif i - 1 >= 0 and \
                    s[i - 1] == "|" and s[i] != "(":
                res.append("(")
                res.append(s[i])
                res.append(")")
            else:
                res.append(s[i])
        return "".join(res)

    def init_from_string(self, s):
        """init_from_string
        Initialize the node from a string
        :param s: the string
        """
        self.head = "."
        self.sons = []
        current_node = self
        current_stack = ""
        s = s.split(":-")
        if len(s) == 2:
            self.name = s[0]
            s = self.preprocess(s[1])
        else:
            s = self.preprocess(s[0])
        i = 0
        s = list(s) + [""]
        while i < len(s):
            c = s[i]
            if c == '(':
                if current_stack != "":
                    new_node = RegexTree(Function(current_stack))
                    current_node.add_son(new_node)
                end = self.get_parenthesis_after(s, i)
                if (s[end + 1] == "*" and s[end + 2] == "|") or \
                        s[end + 1] == "|":
                    new_node = RegexTree([])
                    prev_end = i + 1
                    while s[end + 1] == "|" or\
                            (s[end + 1] == "*" and s[end + 2] == "|"):
                        temp_node = RegexTree("".join(s[prev_end:end]))
                        if s[end + 1] == "*":
                            temp_node.head = "*"
                            prev_end = end + 4
                            end = self.get_parenthesis_after(s, end + 3)
                        else:
                            prev_end = end + 3
                            end = self.get_parenthesis_after(s, end + 2)
                        new_node.add_son(temp_node)
                    temp_node = RegexTree("".join(s[prev_end:end]))
                    if s[end + 1] == "*":
                        temp_node.head = "*"
                        i = end + 1
                    else:
                        i = end
                    new_node.add_son(temp_node)
                    new_node.head = "|"
                    self.add_son(new_node)
                elif s[end + 1] == "*":
                    new_node = RegexTree("".join(s[i + 1: end]))
                    new_node.head = "*"
                    current_node.add_son(new_node)
                    i = end + 1
                current_stack = ""
            elif c != ' ':
                current_stack += c
            i += 1
        # if current_stack != "":
        new_node = RegexTree(Function(current_stack))
        current_node.add_son(new_node)

    def n_relations(self):
        """n_relations Gives the number of relations in the function"""
        return 0

    def generate_reduced_rules(self, counter, empty=False):
        rules = []
        cuts = self.get_cuts()
        for cut in cuts:
            t_temp = RegexTree(cut[0])
            t2 = RegexTree(cut[1])
            cuts2 = t_temp.get_cuts()
            for cut2 in cuts2:
                if empty and cut2[0] != "":
                    continue
                if not empty and cut2[1] == "":
                    continue
                t0 = RegexTree(cut2[0])
                t1 = RegexTree(cut2[1])
                res = t0.push_tree("C", "C", counter, end=True)
                rules += res[0]
                counter = res[1]
                res = t1.consume_tree("C", "C", counter)
                rules += res[0]
                counter = res[1]
                res = t2.push_tree("C", "C", counter, end=False)
                rules += res[0]
                counter = res[1]
        return (rules, counter)

    def get_representation(self):
        if type(self.head) == Function:
            return ",".join(self.head.to_list())
        elif self.head == ".":
            return "".join([son.get_representation() for son in self.sons])
        elif self.head == "*":
            return "(" + "".join([son.get_representation()
                                  for son in self.sons]) + ")*"
        elif self.head == "|":
            representation = []
            for son in self.sons:
                if type(son.head) == str and son.head == "*":
                    representation.append(son.get_representation())
                else:
                    representation.append("(" + son.get_representation() + ")")
            return "|".join(representation)

    def get_cuts(self):
        cuts = []
        if type(self.head) == Function:
            relations = [r[0] + "-" * r[1] for r in self.head.relations]
            for i in range(len(relations) + 1):
                cuts.append((",".join(relations[:i]), ",".join(relations[i:])))
            return cuts
        elif self.head == ".":
            cuts = []
            for i in range(len(self.sons)):
                prev_cuts = self.sons[i].get_cuts()
                cuts += [("".join([son.get_representation()
                                   for son in self.sons[:i]]) + prev_cut[0],
                          prev_cut[1] + "".join([son.get_representation()
                                                 for son in self.sons[i+1:]]))
                         for prev_cut in prev_cuts]
            return cuts
        elif self.head == "*":
            prev_cuts = self.sons[0].get_cuts()
            cuts = []
            cuts.append(("", self.get_representation()))
            cuts.append((self.get_representation(), self.get_representation()))
            for prev_cut in prev_cuts:
                if prev_cut[0].strip() != "" and prev_cut[1].strip() != "":
                    cuts.append((self.get_representation() + prev_cut[0],
                                 prev_cut[1] + self.get_representation()))
            cuts.append((self.get_representation(), ""))
            return cuts
        elif self.head == "|":
            cuts = []
            for son in self.sons:
                cuts += son.get_cuts()
            return cuts

    def inverse(self):
        if type(self.head) == Function:
            self.head = Function(self.head.get_inverse_function())
        else:
            self.sons = self.sons[::-1]
            for son in self.sons:
                son.inverse()


def test():
    from consommation_rule import ConsommationRule
    from end_rule import EndRule
    from indexed_grammar import IndexedGrammar
    from rules import Rules
    t0 = RegexTree(Function("b,a"))
    t1 = RegexTree(Function("a"))
    t2 = RegexTree(Function("a"))
    t3 = RegexTree(Function("b"))
    t4 = RegexTree("|", [t0, t1])
    t5 = RegexTree("*", [t4])
    t6 = RegexTree(".", [t2, t5, t3])
    temp = t6.consume_tree("C", "C", 0)
    temp[0].append(ProductionRule("S", "C1000", "end"))
    temp[0].append(ProductionRule("C1000", "C1001", "b"))
    temp[0].append(ProductionRule("C1001", "C1002", "a"))
    temp[0].append(ProductionRule("C1002", "C", "a"))
    temp[0].append(EndRule("T", "epsilon"))
    temp[0].append(ConsommationRule("end", "C", "T"))
    for r in temp[0]:
        print(r)
    print(IndexedGrammar(Rules(temp[0])).is_empty())
