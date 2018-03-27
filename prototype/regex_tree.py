"""
Representation of a regex as a Tree
"""

from typing import List, Tuple, Set, Mapping
import utils
from duplication_rule import DuplicationRule
from function import Function
from production_rule import ProductionRule
from reduced_rule import ReducedRule
from node import Node
from fsm import FSM


class RegexTree(object):
    """RegexTree Represents a regex as a synthax tree"""

    def post_processing(self) -> None:
        """post_processing
        Postprocess the tree after it was created
        """
        new_sons: List['RegexTree'] = []
        for son in self.sons:
            son.post_processing()
            # remove son if it is a function with no relation
            if son.head.is_function() and \
                    son.head.get_function().n_relations() == 0:
                continue
            # remove the son if it has no son and if it is not a function
            elif son.head.is_str() and not son.sons:
                continue
            # skip the concatenation of one son
            elif son.head.is_str() and son.head.get_str() == "." and \
                    len(son.sons) == 1:
                new_sons.append(son.sons[0])
            else:
                new_sons.append(son)
        self.sons: List['RegexTree'] = new_sons

    def __init__(self,
                 head: Node,
                 sons: List['RegexTree'] = None, name: str = "regf") -> None:
        """__init__
        Initialize the synthax tree
        :param head: The head of the tree
        :param sons: The sons of the root node
        :param name: The name of the tree
        :type head: a Node, a string representing a regex or a string \
                    for * (kleen),\
                    . (concatenation) or | (or) or anything else
        :type sons: A list of RegexTree
        :type name: str
        """
        self.name = name
        if head.is_str() and head.get_str() == "":
            # If the head is the empty string, we stop
            self.head = Node(Function([]))
            if sons:
                self.sons: List['RegexTree'] = sons[:]
            else:
                self.sons: List['RegexTree'] = []
            self.original_string = ""
        elif head.is_str() and head.get_str() not in ["|", "*", "."]:
            # We have a string representing a regex to parse
            new_head = head.get_str()
            self.init_from_string(new_head)
            self.original_string = new_head
            self.post_processing()
        else:
            self.head = head
            if sons:
                self.sons: List['RegexTree'] = sons[:]
            else:
                self.sons: List['RegexTree'] = []
            self.original_string = ""

    def add_son(self, son: 'RegexTree') -> None:
        """add_son
        Adds a son to the current node
        :param son: The son to add
        :type son: RegexTree
        """
        self.sons.append(son)

    def consume_tree(self,
                     first: str,
                     last: str,
                     counter: int) -> Tuple[List[ReducedRule], int]:
        """consume_tree
        In the creation of rules in the grammar, consumes symbols
        :param first: The first symbol in the grammar to use
        :param last: The last symbol in the grammar to use
        :param counter: A counter to prevent duplication of non-terminals
        :type first: str
        :type last: str
        :type counter: int
        :return: A couple which contains first the rules generated and then\
                    the next counter to use
        :rtype: A couple of a list of Reduced rules and an int
        """
        rules: List[ReducedRule] = []
        if not self.head.is_str():
            # It means we have a function...
            return utils.unstack(self.head.get_function().part0,
                                 [], counter, first, last)
        elif self.head.get_str() == ".":
            # When concatenation
            temp_nt = [first]
            # Creates intermediate non-terminals
            for _ in range(len(self.sons)):
                temp_nt.append("C" + str(counter))
                counter += 1
            # Consume each son separately and join them with the intermediate
            # non-terminals
            for i in range(len(self.sons)):
                temp = self.sons[i].consume_tree(temp_nt[i],
                                                 temp_nt[i+1],
                                                 counter)
                rules += temp[0]
                counter = temp[1]
            # link last intermediate to the last non-symbol
            rules.append(DuplicationRule(temp_nt[-1], "T", last))
            return (rules, counter)
        elif self.head.get_str() == "|":
            # Or node
            # Each son is consumed separately and they all have the same first
            # and last non-terminals
            for son in self.sons:
                temp = son.consume_tree(first, last, counter)
                rules += temp[0]
                counter = temp[1]
            return (rules, counter)
        elif self.head.get_str() == "*":
            # Kleene star
            # We make the first symbol go directly to the last one, to simulate
            # the empty case
            rules.append(DuplicationRule(first, "T", last))
            # Normally just one
            for son in self.sons:
                # We should end where we begin
                temp = son.consume_tree(last, last, counter)
                rules += temp[0]
                counter = temp[1]
            return (rules, counter)
        return (rules, counter)

    def push_tree(self,
                  first: str,
                  last: str,
                  counter: int,
                  end: bool = False) -> Tuple[List[ReducedRule], int]:
        """push_tree
        Push the regex on the stack of the grammar.
        :param first: The firts non-terminal to use
        :param last: The last non-terminal to use
        :param counter: A counter to prevent duplication of non-terminals
        :param end: Whether an end symbol should be added to the stack
        :type first: str
        :type last: str
        :type counter: int
        :type end: boolean
        :return: A couple which contains first the rules generated and then\
                    the next counter to use
        :rtype: A couple of a list of Reduced rules and an int
        """
        rules: List[ReducedRule] = []
        # We begin by pushing the end symbol if necessary
        if end:
            rules.append(ProductionRule(first, "Ce" + str(counter), "end"))
            first = "Ce" + str(counter)
        if not self.head.is_str():
            # i.e. we have a function
            res = utils.stack(self.head.get_function().part1,
                              counter,
                              first,
                              last)
            rules += res[0]
            counter = res[1]
            return (rules, counter)
        elif self.head.get_str() == ".":
            # Concatenation
            # Creates intermediate non-terminals
            temp_nt = [first]
            for _ in range(len(self.sons)):
                temp_nt.append("C" + str(counter))
                counter += 1
            # Consume each son separately and join them with the intermediate
            # non-terminals
            for i in range(len(self.sons)):
                temp = self.sons[i].push_tree(temp_nt[i],
                                              temp_nt[i+1],
                                              counter)
                rules += temp[0]
                counter = temp[1]
            # link last intermediate to the last non-symbol
            rules.append(DuplicationRule(temp_nt[-1], "T", last))
            return (rules, counter)
        elif self.head.get_str() == "|":
            # Or node
            # Each son is pushed separately and they all have the same first
            # and last non-terminals
            for son in self.sons:
                temp = son.push_tree(first, last, counter)
                rules += temp[0]
                counter = temp[1]
            return (rules, counter)
        elif self.head.get_str() == "*":
            # Kleene star
            # We make the first symbol go directly to the last one, to simulate
            # the empty case
            rules.append(DuplicationRule(first, "T", last))
            # Normally just one
            for son in self.sons:
                # We should end where we begin
                temp = son.push_tree(last, last, counter)
                rules += temp[0]
                counter = temp[1]
            return (rules, counter)
        return (rules, counter)


    def print_tree_sub(self, level: int = 0) -> List[str]:
        """print_tree_sub
        Recursive method to get the tree as a string
        :param level: The depth
        :return: A string representing the RegexTree as a tree
        :rtype: List[str]
        """
        res = [" " * level + "|>" + str(self.head)]
        for son in self.sons:
            res += son.print_tree_sub(level + 1)
        return res

    def print_tree(self) -> str:
        """print_tree
        Recursive method to get the tree as a string
        :param level: The depth
        :return: A string representing the RegexTree as a tree
        :rtype: str
        """
        return "\n".join(self.print_tree_sub(0))

    def __repr__(self) -> str:
        """__repr__ The string representation of the tree
        :return: A representation of the RegexTree
        :rtype: str
        """
        return self.print_tree()

    def process_init_parenthesis(self,
                                 current_stack: str,
                                 current_node: 'RegexTree',
                                 i: int,
                                 s_list: List[str]) -> int:
        """process_init_parenthesis
        Process to make when encountering an opening parenthesis
        :param current_stack: The current state of the stack
        :type current_stack: str
        :param i: The current index in the regex
        :type i: int
        :param s_list: The regex, as a list
        :type s_list: List[str]
        :return: The next index to consider
        :rtype: int
        """
        # If we have read something so far, we transform it into a
        # function and make it a son of the current node
        if current_stack != "":
            new_node = RegexTree(Node(Function(current_stack)))
            current_node.add_son(new_node)
        # Gets where the parenthesis ends
        end = get_parenthesis_after(s_list, i)
        if (s_list[end + 1] == "*" and s_list[end + 2] == "|") or \
                s_list[end + 1] == "|":
            # We have a or
            new_node = RegexTree(Node(""))
            prev_end = i + 1
            # We read all the ors
            while s_list[end + 1] == "|" or\
                    (s_list[end + 1] == "*" and s_list[end + 2] == "|"):
                temp_node = RegexTree(Node(
                    "".join(s_list[prev_end:end])))
                if s_list[end + 1] == "*":
                    temp_node.head = Node("*")
                    prev_end = end + 4
                    end = get_parenthesis_after(s_list, end + 3)
                else:
                    prev_end = end + 3
                    end = get_parenthesis_after(s_list, end + 2)
                new_node.add_son(temp_node)
            # The last or
            temp_node = RegexTree(Node("".join(s_list[prev_end:end])))
            if s_list[end + 1] == "*":
                temp_node.head = Node("*")
                i = end + 1
            else:
                i = end
            new_node.add_son(temp_node)
            new_node.head = Node("|")
            self.add_son(new_node)
        else:
            # Read what is inside the parenthesis
            new_node = RegexTree(Node("".join(s_list[i + 1:end])))
            # Read what kind of parenthesis it is
            if s_list[end + 1] == "*":
                new_node2 = RegexTree(Node("*"))
                i = end + 1
            else:

                new_node2 = RegexTree(Node("."))
                i = end
            new_node2.add_son(new_node)
            current_node.add_son(new_node2)
        return i

    def init_from_string(self, in_str: str) -> None:
        """init_from_string
        Initialize the node from a string
        :param in_str: The input string
        :type in_str: str
        :return: Nothing
        :rtype: None
        """
        # By default the head is a concatenation
        self.head = Node(".")
        self.sons: List['RegexTree'] = []
        current_node = self
        current_stack = ""
        # In case a name was given
        s_temp = in_str.split(":-")
        if len(s_temp) == 2:
            self.name = s_temp[0]
            s_preprocessed = preprocess(s_temp[1])
        else:
            s_preprocessed = preprocess(s_temp[0])
        i = 0
        s_list = list(s_preprocessed) + [""]
        while i < len(s_list) - 1:
            current_c = s_list[i]
            # If a parenthesis is found, we need to go one level further
            if current_c == '(':
                i = self.process_init_parenthesis(current_stack,
                                                  current_node,
                                                  i,
                                                  s_list)
                current_stack = ""
            elif current_c != ' ' and current_c != ")" and current_c != "(":
                # Otherwise, we simply read a caracter which will be part of the
                # next function
                current_stack += current_c
            i += 1
        # Finish to create the current node with what is left to add
        new_node = RegexTree(Node(Function(current_stack)))
        current_node.add_son(new_node)

    def n_relations(self) -> int:
        """n_relations Gives the number of relations in the function.
        Useless here, only for compatibility.
        :return: 0
        :rtype: int
        """
        return len(self.original_string)

    def generate_reduced_rules(
            self,
            counter: int,
            empty: bool = False) -> Tuple[List[ReducedRule], int]:
        """generate_reduced_rules
        Generates a set of reduced rules
        :param counter: A counter to prevent duplication of non-terminals
        :param empty: Whether to use the empty rule or not
        :type counter: int
        :type empty: bool
        :return: A tuple with rules and the new counter
        :rtype: Tuple[List[ReducedRule], int]
        """
        rules: List[ReducedRule] = []
        # We will cut the function into 3 parts and use these parts to generate
        # the rules of the grammar
        cuts = self.get_cuts()
        for cut in cuts:
            cuts2 = RegexTree(Node(cut[0])).get_cuts()
            for cut2 in cuts2:
                if empty and cut2[0] != "":
                    continue
                if not empty and cut2[1] == "":
                    continue
                # We split the rule into the three parts we are considering
                c_left = "Cleft" + str(counter)
                c_right = "Cright" + str(counter)
                c_inter = "Cinter" + str(counter)
                rules.append(DuplicationRule("C", c_left, c_right))
                res = RegexTree(Node(cut2[0])).push_tree(c_left,
                                                         "C",
                                                         counter,
                                                         end=True)
                rules += res[0]
                counter = res[1]
                res = RegexTree(Node(cut2[1])).consume_tree(c_right,
                                                            c_inter,
                                                            counter)
                rules += res[0]
                counter = res[1]
                res = RegexTree(Node(cut[1])).push_tree(c_inter,
                                                        "C",
                                                        counter,
                                                        end=False)
                rules += res[0]
                counter = res[1]
        return (rules, counter)

    def get_representation(self) -> str:
        """get_representation
        Gets a representation of the RegexTree
        :return: A representation of the RegexTree
        :rtype: str
        """
        if self.head.is_function():
            return ",".join(self.head.get_function().to_list())
        elif self.head.get_str() == ".":
            return "".join([son.get_representation() for son in self.sons])
        elif self.head.get_str() == "*":
            return "(" + "".join([son.get_representation()
                                  for son in self.sons]) + ")*"
        elif self.head.get_str() == "|":
            representation = []
            for son in self.sons:
                if son.head.is_str() and son.head.get_str() == "*":
                    representation.append(son.get_representation())
                else:
                    representation.append("(" + son.get_representation() + ")")
            return "|".join(representation)
        return ""


    def get_cuts(self) -> List[Tuple[str, str]]:
        """get_cuts
        Gets all possible cuts of the RegexTree
        :return: The possible cuts
        :rtype: List[Tuple[str, str]]
        """
        cuts = []
        if self.head.is_function():
            # For a function, simply cut between all relations
            relations = [r[0] + "-" * r[1]
                         for r in self.head.get_function().relations]
            for i in range(len(relations) + 1):
                cuts.append((",".join(relations[:i]), ",".join(relations[i:])))
            return cuts
        elif self.head.get_str() == ".":
            cuts = []
            for i in range(len(self.sons)):
                prev_cuts = self.sons[i].get_cuts()
                cuts += [(",".join([son.get_representation()
                                    for son in self.sons[:i]]) + "," +
                          prev_cut[0],
                          prev_cut[1] + "," +
                          ",".join([son.get_representation()
                                    for son in self.sons[i+1:]]))
                         for prev_cut in prev_cuts]
                cuts = list(map(replace_comma_in_tuple,
                                cuts))
            return cuts
        elif self.head.get_str() == "*":
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
        elif self.head.get_str() == "|":
            cuts = []
            for son in self.sons:
                cuts += son.get_cuts()
            return cuts
        return cuts

    def inverse(self) -> None:
        """inverse
        Inverse the regex
        :return: Nothing
        :rtype: None
        """
        if self.head.is_function():
            self.head = Node(Function(
                self.head.get_function().get_inverse_function()))
        else:
            self.sons: List['RegexTree'] = self.sons[::-1]
            for son in self.sons:
                son.inverse()

    def get_alphabet(self) -> List[str]:
        """get_alphabet
        Get an alphabet from the regex
        :return: The list of the elements in the alphabet
        :rtype: List[str]
        """
        if self.head.is_function():
            return self.head.get_function().get_all_terminals()
        else:
            s_res: Set[str] = set()
            for son in self.sons:
                s_res = s_res.union(son.get_alphabet())
        return list(s_res)

    def to_fsm(self) -> FSM:
        """to_fsm
        Transforms the regex into a Finite State Machine.
        This function modifies the regex !
        :return: The FSM corresponding to the current regex
        :rtype: FSM
        """
        alphabet = self.get_alphabet()
        alphabet.append("$")  # epsilon symbol
        states = [0]
        initial = 0
        finals: List[int] = []
        fsm = FSM(alphabet, states, initial, finals)
        self.to_fsm_sub((0, []), 1, fsm, True)
        return fsm

    def continue_final(self) -> bool:
        """continue_final
        Determines whether this node is a blocking final node or not
        :return: Whether to continue looking for final nodes
        :rtype: bool
        """
        if self.head.is_function():
            return False
        if self.head.get_str() == "*":
            # We need to continue as we may have an empty sequence
            return True
        if self.head.get_str() == ".":
            res = True
            # All need to continue
            for son in self.sons:
                res &= son.continue_final()
            return res
        if self.head.get_str() == "|":
            res = False
            # At least one needs to continue
            for son in self.sons:
                res |= son.continue_final()
            return res
        return False

    def need_jump(self) -> bool:
        """need_jump
        Say if we should integrate a new state in the FSM when processing a dot
        :return: Whether to introduce a new state or not
        :rtype: bool
        """
        if self.head.is_function():
            return True
        if self.head.get_str() == "*":
            return False
        if self.head.get_str() == ".":
            res = False
            for son in self.sons:
                res |= son.need_jump()
            return res
        if self.head.get_str() == "|":
            res = False
            for son in self.sons:
                res |= son.need_jump()
            return res
        return False

    def or_star(self) -> bool:
        """or_star
        Says, when we have a OR head, whether the OR could have a choice between
        empty string, except if the next one is also a OR
        :return: See above
        :rtype: bool
        """
        if self.head.is_function():
            return False
        if self.head.get_str() == "*":
            return True
        if self.head.get_str() == ".":
            res = False
            for son in self.sons:
                # Could be optimized
                res |= son.or_star()
            return res
        if self.head.get_str() == "|":
            return False
        return False

    def to_fsm_sub_dot(self,
                       limits: Tuple[int, List[int]],
                       counter: int,
                       fsm: FSM,
                       is_final: bool) -> int:
        """to_fsm_sub_dot
        Transforms a node which is a concatenation into a FSM
        :param limits: Limits of the FSM, of the form (first node, lasts nodes)
        :type limits: Tuple[int, List[int]]
        :param counter: A counter to prevent duplication of states
        :type counter: int
        :param fsm: The FSM which is beeing built
        :type fsm: FSM
        :param is_final: Whether the node is final or not
        :type is_final: bool
        :return: A new counter, to prevent duplication
        :rtype: int
        """
        first = limits[0]
        lasts = limits[1]
        last_final = len(self.sons) + 1
        if is_final:
            for last_final in range(len(self.sons) - 1, -1, -1):
                if not self.sons[last_final].continue_final():
                    break
        jumps = list(range(counter, counter + len(self.sons) - 1))
        counter = counter + len(self.sons) - 1
        prev_first = first
        for i in range(len(self.sons) - 1):
            if self.sons[i].need_jump():
                counter = self.sons[i].to_fsm_sub((prev_first,
                                                   [jumps[i]]),
                                                  counter,
                                                  fsm,
                                                  i >= last_final)
                prev_first = jumps[i]
            else:
                counter = self.sons[i].to_fsm_sub((prev_first,
                                                   [prev_first]),
                                                  counter,
                                                  fsm,
                                                  i >= last_final)
        if not lasts:
            lasts = [counter]
            counter += 1
            counter = self.sons[-1].to_fsm_sub((prev_first,
                                                lasts),
                                               counter,
                                               fsm, is_final)
        return counter

    def to_fsm_sub(self,
                   limits: Tuple[int, List[int]],
                   counter: int,
                   fsm: FSM,
                   is_final: bool):
        """to_fsm_sub
        Transforms a node into a FSM
        :param limits: Limits of the FSM, of the form (first node, lasts nodes)
        :type limits: Tuple[int, List[int]]
        :param counter: A counter to prevent duplication of states
        :type counter: int
        :param fsm: The FSM which is beeing built
        :type fsm: FSM
        :param is_final: Whether the node is final or not
        :type is_final: bool
        :return: A new counter, to prevent duplication
        :rtype: int
        """
        first = limits[0]
        lasts = limits[1]
        if self.head.is_function():
            l_f = self.head.get_function().to_list()
            prev_state = first
            for i in range(len(l_f) - 1):
                fsm.add_transition(prev_state, counter, l_f[i])
                prev_state = counter
                counter += 1
            for last in lasts:
                fsm.add_transition(prev_state, last, l_f[-1])
                if is_final:
                    fsm.add_final(last)
        elif self.head.get_str() == ".":
            return self.to_fsm_sub_dot((first, lasts), counter, fsm, is_final)
        elif self.head.get_str() == "*":
            new_lasts = lasts[:]
            new_lasts.append(first)
            for son in self.sons:
                counter = son.to_fsm_sub((first, new_lasts),
                                         counter,
                                         fsm,
                                         is_final)
        elif self.head.get_str() == "|":
            for son in self.sons:
                if son.or_star():
                    fsm.add_transition(first, counter, "$")
                    counter = son.to_fsm_sub((counter, lasts),
                                             counter + 1,
                                             fsm,
                                             is_final)
                else:
                    counter = son.to_fsm_sub((first, lasts),
                                             counter + 1,
                                             fsm,
                                             is_final)
        return counter


def get_parenthesis_after(s_list: List[str],
                          begin: int) -> int:
    """get_parenthesis_after
    Gets the closing parenthesis which is at position begin
    :param s: The string to consider
    :type s_list: List[str]
    :param begin: The opening parenthesis
    :type begin: int
    :return: The index of the closing parenthesis
    :rtype: int
    """
    # Considered well parenthesis
    counter = 1
    for i in range(begin + 1, len(s_list)):
        if s_list[i] == "(":
            counter += 1
        elif s_list[i] == ")":
            counter -= 1
        if counter == 0:
            return i
    return -1


def preprocess(s_in: str) -> str:
    """preprocess
    Preprocessed the given string to parse. It mainly adds parenthesis to
    help the parsing
    :param s_in: The string to preprocess
    :type s_in: str
    :return: The processed string
    :rtype: str
    """
    res = []
    max_i = len(s_in)
    for i in range(max_i):
        # Detect a|, |a and a* and change them to (a)|, |(a) and (a)*
        if i + 1 < len(s_in) and \
                s_in[i + 1] in ["|", "*"] and \
                s_in[i] != ")" and\
                s_in[i] != "*" and s_in[i] != "|":
            res.append("(")
            res.append(s_in[i])
            res.append(")")
        elif i - 1 >= 0 and \
                s_in[i - 1] == "|" and s_in[i] != "(":
            res.append("(")
            res.append(s_in[i])
            res.append(")")
        else:
            res.append(s_in[i])
    return "".join(res)


def replace_comma_in_tuple(tuple_in: Tuple[str, str]) -> Tuple[str, str]:
    """replace_comma_in_tuple
    If a tuple contains a string containing only a comma, then it is
    replaced by the empty string
    :param x: The tuple to consider
    :type x: Tuple[str, str]
    :return: A new tuple, without the lonely commas
    :rtype: Tuple[str, str]
    """
    res0 = tuple_in[0]
    if res0 == ",":
        res0 = ""
    res1 = tuple_in[1]
    if res1 == ",":
        res1 = ""
    return (res0, res1)
