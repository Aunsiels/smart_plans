"""
We represents here a FSM for our regex. It will not be a general one. In \
    particular, the alphabets is different from traditionnal ones.
"""


from typing import List, Any
from round_list import RoundList
from node import Node


class FSM(object):
    """FSM Finite State Machine. The methods modify the object"""

    def __init__(self,
                 alphabet: List[str] = None,
                 states: List[Any] = None,
                 initial: Any = 0,
                 finals: List[Any] = None) -> None:
        """__init__ Creates a new fsm
        The empty symbol is $
        :param alphabet: the alphabet of the fsm
        :param states: the list of states in the fsm
        :param initial: the initial state
        :param finals: the final states
        :type alphabet: A list of strings
        :type states: A list of state names (Any, str, ...)
        :type initial: str, Any,...
        :type finals: A list of state names (Any, str, ...)
        """
        if alphabet:
            self.alphabet = list(map(lambda x: x.replace("-", "m"), alphabet))
        else:
            self.alphabet = ["$"]
        if states:
            self.states = states
        else:
            self.states = []
        self.initial = initial
        self.states.append(initial)
        self.states = list(set(self.states))
        if finals:
            self.finals = finals
        else:
            self.finals = list()
        self.transitions = dict()

    def add_state(self, state: Any) -> None:
        """add_state
        Add a state to the FSM
        :param state: The state to add
        :type state: Any
        :return: Nothing
        :rtype: None
        """
        if state not in self.states:
            self.states.append(state)

    def get_next_state(self) -> Any:
        """get_next_state
        Get a free state
        :return: A free state
        :rtype: Any
        """
        return max(self.states) + 1

    def add_transition(self,
                       s_from: Any,
                       s_to: Any,
                       t_by: str) -> None:
        """add_transition
        Adds a transition from s_from to s_to through "t_by" to the fsm
        :param s_from: The origin of the transition
        :param s_to: The target of the transition
        :param t_by: The symbol of the transition
        :return: Nothing
        """
        t_by = t_by.replace("-", "m")
        if s_from not in self.states:
            self.states.append(s_from)
        if s_to not in self.states:
            self.states.append(s_to)
        if t_by not in self.alphabet:
            self.alphabet.append(t_by)
        if s_from in self.transitions.keys():
            if s_to in self.transitions[s_from].keys():
                if t_by not in self.transitions[s_from][s_to]:
                    self.transitions[s_from][s_to].append(t_by)
            else:
                self.transitions[s_from][s_to] = [t_by]
        else:
            self.transitions[s_from] = dict()
            self.transitions[s_from][s_to] = [t_by]

    def add_final(self, s_final: Any) -> None:
        """add_final
        Adds a final state to the fsm
        :param s_final: The final state to add
        :rtype s_final: Any
        :return: Nothing
        """
        if s_final not in self.finals:
            self.finals.append(s_final)
        if s_final not in self.states:
            self.states.append(s_final)

    def __transform_state(self, state):
        if state == (-1, -1):
            return "init"
        return str(state).replace(", ", "").replace("(", "").replace(")", "")

    def __repr__(self) -> str:
        """__repr__ Gives a string representation of the fsm to be used on the
        website http://ivanzuzak.info/noam/webapps/fsm2regex/
        :return: A string representing the fsm.
        :rtype: str
        """
        res = []
        res.append("#states")
        for state in set(map(self.__transform_state, self.states)):
            res.append(state)
        res.append("#initial")
        res.append(self.__transform_state(self.initial))
        res.append("#accepting")
        for final in self.finals:
            res.append(self.__transform_state(final))
        res.append("#alphabet")
        for letter in self.alphabet:
            if letter != "$":
                res.append(str(letter))
        res.append("#transitions")
        for s_from in self.transitions:
            for s_to in self.transitions[s_from]:
                for letter in self.transitions[s_from][s_to]:
                    res.append(self.__transform_state(s_from) + ":" +
                               str(letter) + ">"
                               + self.__transform_state(s_to))
        return "\n".join(res)

    def create_or(self) -> None:
        """create_or Method used in the transformation to a regex tree. If
        several transition exist between two states x and y, then we create a
        transition which is the or of all others"""
        for s_from in self.transitions:
            for s_to in self.transitions[s_from]:
                if len(self.transitions[s_from][s_to]) > 1:
                    # Replace all previous transitions
                    self.transitions[s_from][s_to] = \
                        ["(" +
                         ")|(".join(
                             self.transitions[s_from][s_to]) +
                         ")"]

    def remove_state_cleanup(self, state: Any) -> None:
        """remove_state_cleanup
        Cleans the fsm after a state is removed.
        If the state is a final state, we do nothing (cannot delete end state).
        :param state: The state to delete
        :type state: Any, str,...
        """
        if state not in self.finals:
            for s_other in self.states:
                if s_other in self.transitions.keys() and \
                        state in self.transitions[s_other].keys():
                    del self.transitions[s_other][state]
            self.states.remove(state)

    def clean_transition(self, state: Any):
        """clean_transition
        Removes the transitions from state. If the state is a final state, we
        do not remove the transition to itself
        :param state: The state from which transitions are removed
        :type state: Any, str,...
        """
        to_remove = []
        for s_remove in self.transitions[state]:
            # We do not want to remove transitions to itself to final nodes
            if s_remove != state:
                to_remove.append(s_remove)
        for s_remove in to_remove:
            del self.transitions[state][s_remove]
        if state not in self.finals:
            del self.transitions[state]

    def __remove_state_sub(self,
                           state: Any,
                           to_me: List[str],
                           s_other: Any,
                           letter0: str) -> bool:
        """__remove_state_sub
        A subfunction for remove_state_sub
        :param state: The current state
        :param to_me: transition to me
        :param s_other: Another state
        :param letter0: A letter of the alphabet
        :return:
        """
        res = False
        for s_to in self.transitions[state]:
            for letter1 in self.transitions[state][s_to]:
                if not to_me and s_to != state:
                    # To link to itself, simply concatenate
                    self.add_transition(s_other,
                                        s_to,
                                        letter0 + "," + letter1)
                    res = True
                elif s_to != state:
                    # If there is a link to itself, we have a
                    # a kleene star
                    for letter2 in to_me:
                        self.add_transition(s_other, s_to,
                                            letter0 +
                                            ",(" + letter2 +
                                            ")*" +
                                            letter1)
                        res = True
        return res

    def remove_state(self, state: Any) -> bool:
        """remove_state
        Removes a state from the fsm. We return if something changed or not.
        This is a function for traduction to a regex.
        :param state: The state to remove
        :type state: Any, str, ...
        :return: Whether something was modified
        :rtype: Boolean
        """
        # At the beginning nothing changed...
        res = False
        if state in self.transitions:
            for s_other in self.states:
                if s_other != state and s_other in self.transitions.keys() and \
                        state in self.transitions[s_other].keys():
                    # Links to the states itself
                    to_me = self.transitions[state].setdefault(state, [])
                    # We look for paths of the type x -> state -> y to be able
                    # to recreate it as it will be deleted
                    for letter0 in self.transitions[s_other][state]:
                        res |= self.__remove_state_sub(state,
                                                       to_me,
                                                       s_other,
                                                       letter0)
            self.clean_transition(state)

        self.remove_state_cleanup(state)
        return res

    def get_final_strings(self) -> List[str]:
        """get_final_strings Once all non-initial or non-final nodes have been
        removed from the fsm, creates the equivalent regex for each final node
        :return: A list containing the equivalent regex for each final state
        :rtype: A list of states
        """
        temp_finals = []
        for final in self.finals:
            if final in self.transitions[self.initial]:
                # Only one transition in this case
                if self.initial == final:
                    # Normally, there is only one node between self.initial and
                    # final
                    temp_finals.append("(" + "".join(
                        self.transitions[self.initial][final]) + ")*")
                else:
                    temp_finals.append("".join(
                        self.transitions[self.initial][final]))
                    # If there is a link to itself, we have a kleene star
                    if final in self.transitions.keys() and\
                            final in self.transitions[final].keys():
                        temp_finals[-1] += "(" + \
                            "".join(self.transitions[final][final]) +\
                            ")*"
        return temp_finals

    def __minus_relation(self, relation):
        count = relation.count("m") + 1
        return relation.replace("m", "") + "m" * (count % 2)

    def __get_reachables(self, s_from):
        reachables = set()
        to_process = [s_from]
        reachables.add(s_from)
        while to_process:
            current = to_process.pop()
            for s_to in self.transitions.setdefault(current, dict()):
                if "$" in self.transitions[current][s_to] and \
                        s_to not in reachables:
                    to_process.append(s_to)
                    reachables.add(s_to)
        reachables.remove(s_from)
        return reachables

    def remove_epsilon_transitions(self):
        alphabet = self.alphabet[:]
        states = self.states[:]
        initial = self.initial
        finals = self.finals[:]
        fsm = FSM(alphabet, states, initial, finals)
        for state in states:
            for s_to in self.transitions.setdefault(state, dict()):
                for a in self.transitions[state][s_to]:
                    if a != "$":
                        fsm.add_transition(state, s_to, a)
            reachables = self.__get_reachables(state)
            for final in finals:
                if final in reachables:
                    fsm.add_final(state)
                    break
            for state_temp in reachables:
                for s_to in self.transitions.setdefault(state_temp, dict()):
                    for a in self.transitions[state_temp][s_to]:
                        if a != "$":
                            fsm.add_transition(state, s_to, a)
        return fsm

    def get_palindrome_fsm(self, query="", weak=False, sub_functions=False):
        # Not sure it works well with epsilon transitions
        self.close()
        fsm_no_e = self.remove_epsilon_transitions()
        alphabet = fsm_no_e.alphabet[:]
        states = []
        for x in fsm_no_e.states:
            for y in fsm_no_e.states:
                states.append((x, y))
        initial = (-1, -1)
        finals = [(x, x) for x in fsm_no_e.states]
        # finals = [(x, x) for x in fsm_no_e.finals]
        # Compensate an epsilon between a final and a initial
        # for final in fsm_no_e.finals:
        #     finals.append((final, fsm_no_e.initial))
        #     finals.append((fsm_no_e.initial, final))
        fsm = FSM(alphabet, states, initial, finals)
        if sub_functions:
            finals_no_e = fsm_no_e.states
        else:
            finals_no_e = fsm_no_e.finals
        for q in finals_no_e:
            if query == "":
                fsm.add_transition(initial, (fsm_no_e.initial, q), "$")
            else:
                # Ends with query
                for p in fsm_no_e.states:
                    if q in fsm_no_e.transitions.setdefault(p, dict()) and\
                            query in fsm_no_e.transitions[p][q]:
                        fsm.add_transition(initial, (fsm_no_e.initial, p), "$")
                if weak:
                    for p in fsm_no_e.transitions.setdefault(fsm_no_e.initial,
                                                             dict()):
                        if query in fsm_no_e.transitions[fsm_no_e.initial][p]:
                            fsm.add_transition(initial, (p, q), "$")

        for p in fsm_no_e.states:
            for s in fsm_no_e.states:
                for r in fsm_no_e.transitions.setdefault(p, dict()):
                    for a in fsm_no_e.transitions[p][r]:
                        for q in fsm_no_e.transitions.setdefault(s, dict()):
                            if fsm_no_e.__minus_relation(a) in\
                                    fsm_no_e.transitions[s][q]:
                                fsm.add_transition((p, q), (r, s), a)
        return fsm

    def is_empty(self):
        to_process = []
        visited = set()
        to_process.append(self.initial)
        visited.add(self.initial)
        while to_process:
            current = to_process.pop()
            for x in self.transitions.setdefault(current, dict()):
                if x in self.finals:
                    return False
                if x not in visited:
                    visited.add(x)
                    to_process.append(x)
        return True

    def find_word(self):
        to_process = []
        visited = set()
        to_process.append((self.initial, []))
        visited.add(self.initial)
        while to_process:
            current, l = to_process.pop()
            d = self.transitions.setdefault(current, dict())
            for x in d:
                if x in self.finals:
                    print(self)
                    return l + [d[x]]
                if x not in visited:
                    visited.add(x)
                    to_process.append((x, l + [d[x]]))
        return None

    def to_regex(self) -> Any:
        """to_regex Transforms the FSM to regex
        :return: A regex equivalent to the FSM
        :rtype: RegexTree
        """
        from regex_tree import RegexTree
        temp_states = self.states[:]
        # We remove the states in the fsm one after the other.
        for state in temp_states:
            # Remove multiple transitions between two nodes
            self.create_or()
            # We do not remove the initial or the final states
            if state != self.initial and state not in self.finals:
                self.remove_state(state)
        self.create_or()
        cont = True
        # While there are modifications of the fsm, we continue
        # Converges ? Need a loop ?
        while cont:
            cont = False
            # For all final nodes, we want to keep only out transitions to
            # itself
            for final in self.finals:
                if final != self.initial:
                    cont |= self.remove_state(final)
                    self.create_or()
        res = ""
        # Nothing to do here
        if self.initial not in self.transitions:
            return RegexTree(Node(""))
        # The transitions from the initial node to itself is a kleene star
        if self.initial in self.transitions[self.initial]:
            res += "(" + \
                "".join(self.transitions[self.initial][self.initial]) + ")*"
        # Get all the equivalent paths to the final states
        temp_finals = self.get_final_strings()
        # ... and creates an or of all of them
        if len(temp_finals) > 1:
            return RegexTree(Node(res + "(" + ")|(".join(temp_finals) + ")"))
        return RegexTree(Node(res + ")|(".join(temp_finals)))

    def close(self) -> None:
        """close Creates a kleene star around the fsm, by linking the final
        states to the initial state with an epsilon transition"""
        for final in self.finals:
            self.add_transition(final, self.initial, "$")

    def open(self) -> None:
        """open Removes the epsilon links between the final states and the
        initial state"""
        for final in self.finals:
            if final in self.transitions.keys():
                if self.initial in self.transitions[final].keys():
                    self.transitions[final][self.initial].remove("$")

    def exists_path(self,
                    start_node: Any,
                    end: Any,
                    path: List[str]) -> bool:
        """exists_path
        Does the given path between two nodes exists?
        :param start_node: The starting node
        :param end: The ending node
        :param path: The path to consider
        :return: Whether the path l exists between start and end
        :rtype: Boolean
        """
        # Contains the nodes reached so far
        # It is a kind of BFS
        starts = [start_node]
        for rel in path:
            next_starts = []
            for start in starts:
                if start in self.transitions:
                    for s_to in self.transitions[start]:
                        if rel in self.transitions[start][s_to]:
                            next_starts.append(s_to)
            starts = next_starts
        return end in starts

    def apply_rule(self,
                   rule_left: List[str],
                   rule_right: List[str]) -> bool:
        """apply_rule
        Apply a Horn rule
        :param rule_left: left part of the horn rule
        :param rule_right: right part of the horn rule
        :return: Whether the FSM was modified
        :rtype: Boolean
        """
        # rule_left => rule_right Horn Rule
        was_modified = False
        # While there are modifications, we continue
        while self.apply_rule_sub(rule_left, rule_right):
            was_modified = True
            continue
        return was_modified

    def apply_rule_sub(self,
                       rule_left: List[str],
                       rule_right: List[str]) -> bool:
        """apply_rule_sub
        make one pass of the horn rule transformation
        :param rule_left: left part of the horn rule
        :param rule_right: right part of the horn rule
        :return: whether the fsm was modified
        :rtype: boolean
        """
        # rule_left => rule_right
        # keep track of all previous states encountered when a given node was
        # reached
        seen_before = dict()
        # nothing was seen before
        for state in self.states:
            seen_before[state] = []
        # a stack of elements to process (dfs)
        # we use roundlists which are list which keep track only of the last
        # elements inserted
        to_process = [(self.initial, RoundList(len(rule_left)), False)]
        # counter to prevent the duplication of nodes
        # should be useless for horn rules
        counter = max(self.states) + 1
        # whether there was a modification done
        was_modified = False
        while to_process:
            current = to_process.pop()
            current_node = current[0]
            current_rl = current[1]
            should_be_processed = current[2]
            # state already reached
            if current_rl in seen_before[current_node]:
                continue
            seen_before[current_node].append(current_rl)
            current_l = current_rl.get()
            # should we add a new link?
            if rule_left == list(map(lambda x: x[1], current_l)) and\
                    not self.exists_path(current_l[0][0],
                                         current_node,
                                         rule_right) and\
                    should_be_processed:
                prev_first = current_l[0][0]
                # should not be useful for horn rule. it is here for testing
                # purposes
                for i in range(len(rule_right) - 1):
                    self.add_transition(prev_first, counter, rule_right[i])
                    prev_first = counter
                    seen_before[counter] = []
                    counter += 1
                self.add_transition(prev_first, current_node, rule_right[-1])
                was_modified = True
            # continue exploration
            if current_node in self.transitions.keys():
                for s_to in self.transitions[current_node]:
                    for letter in self.transitions[current_node][s_to]:
                        next_rl = current_rl.copy()
                        # the empty symbols should be ignored
                        if letter != "$":
                            next_rl.push((current_node, letter))
                            to_process.append((s_to, next_rl, True))
                        if letter == "$":
                            to_process.append((s_to, next_rl, False))
        return was_modified

    def accepts(self, word):
        if len(word) == 0:
            return self.initial in self.finals
        to_process = [self.initial]
        for rel in word:
            next_process = set()
            for x in to_process:
                for y in self.transitions.setdefault(x, dict()):
                    if rel in self.transitions[x][y]:
                        next_process.add(y)
                        for z in self.__get_reachables(y):
                            next_process.add(z)
            to_process = next_process
        return len(to_process.intersection(set(self.finals))) > 0

    def make_dangie_ready(self):
        # was_modified = True
        # counter = 0
        # while was_modified:
        #     print(counter)
        #     counter += 1
        #     was_modified = self.process_dangie()
        # return self.remove_epsilon_transitions()
        in_edges = dict()
        out_edges = dict()
        processed = set()
        to_process = []
        self.close()
        fsm = self.remove_epsilon_transitions()
        finals = set(fsm.finals[:])
        alphabet = set(fsm.alphabet[:])
        for state in fsm.states:
            in_edges[state] = dict()
            out_edges[state] = dict()
            for a in fsm.alphabet:
                in_edges[state][a] = []
                out_edges[state][a] = []
        for first in fsm.transitions:
            for second in fsm.transitions[first]:
                for a in fsm.transitions[first][second]:
                    opposite = get_opposite(a)
                    if first not in in_edges[second][a]:
                        in_edges[second][a].append(first)
                    if second not in out_edges[first][a]:
                        out_edges[first][a].append(second)
                    if opposite not in alphabet:
                        continue
                    for state in in_edges[first][opposite]:
                        if (state, second) not in processed:
                            to_process.append((state, second))
                            processed.add((state, second))
                    for state in out_edges[second][opposite]:
                        if (first, state) not in processed:
                            to_process.append((first, state))
                            processed.add((first, state))
        while to_process:
            current = to_process.pop()
            first = current[0]
            second = current[1]
            if first == second:
                continue
            if second in finals:
                finals.add(first)
            for a in out_edges[second]:
                for state in out_edges[second][a]:
                    if state not in out_edges[first][a]:
                        out_edges[first][a].append(state)
                    if first not in in_edges[state][a]:
                        in_edges[state][a].append(first)
                    opposite = get_opposite(a)
                    if opposite in alphabet:
                        for begin in in_edges[first][opposite]:
                            if (begin, state) not in processed:
                                to_process.append((begin, state))
                                processed.add((begin, state))
                        for end in out_edges[state][opposite]:
                            if (first, end) not in processed:
                                to_process.append((first, end))
                                processed.add((first, end))
        alphabet = list(alphabet)
        states = fsm.states[:]
        initial = fsm.initial
        finals = list(finals)
        new_fsm = FSM(alphabet, states, initial, finals)
        for begin in out_edges:
            for a in out_edges[begin]:
                for end in out_edges[begin][a]:
                    new_fsm.add_transition(begin, end, a)
        return new_fsm


    def process_dangie(self) -> bool:
        # keep track of all previous states encountered when a given node was
        # reached
        seen_before = dict()
        # nothing was seen before
        for state in self.states:
            seen_before[state] = []
        # a stack of elements to process (dfs)
        # we use roundlists which are list which keep track only of the last
        # elements inserted
        to_process = [(self.initial, RoundList(2), False)]
        # whether there was a modification done
        was_modified = False
        while to_process:
            current = to_process.pop()
            current_node = current[0]
            current_rl = current[1]
            should_be_processed = current[2]
            # state already reached
            if current_rl in seen_before[current_node]:
                continue
            seen_before[current_node].append(current_rl)
            current_l = current_rl.get()
            # should we add a new link?
            if is_palindrome(current_l) and\
                    not self.exists_path(current_l[0][0],
                                         current_node,
                                         "$") and\
                    should_be_processed:
                prev_first = current_l[0][0]
                # should not be useful for horn rule. it is here for testing
                # purposes
                self.add_transition(prev_first, current_node, "$")
                was_modified = True
            # continue exploration
            if current_node in self.transitions.keys():
                for s_to in self.transitions[current_node]:
                    for letter in self.transitions[current_node][s_to]:
                        next_rl = current_rl.copy()
                        # the empty symbols should be ignored
                        if letter != "$":
                            next_rl.push((current_node, letter))
                            to_process.append((s_to, next_rl, True))
                        if letter == "$":
                            to_process.append((s_to, next_rl, False))
        return was_modified


def get_opposite(r):
    if r[-1] == "m":
        return r[:-1]
    else:
        return r + "m"


def are_opposite(r0, r1):
    return r0 == r1 + "m" or r1 == r0 + "m"


def is_palindrome(l):
    left = l[0][1]
    right = l[1][1]
    if len(l) != 2:
        return False
    if "_IN" in left:
        return False
    if "_IN" in right:
        right = right.replace("_IN", "_OUT")
    return left == right + "m" or left + "m" == right
