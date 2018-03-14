"""
We represents here a FSM for our regex. It will not be a general one. In \
    particular, the alphabets is different from traditionnal ones.
"""


from round_list import RoundList
from node import Node


class FSM(object):
    """FSM Finite State Machine. The methods modify the object"""

    def __init__(self,
                 alphabet=None,
                 states=None,
                 initial=0,
                 finals=None):
        """__init__ Creates a new fsm
        The empty symbol is $
        :param alphabet: the alphabet of the fsm
        :param states: the list of states in the fsm
        :param initial: the initial state
        :param finals: the final states
        :type alphabet: A list of strings
        :type states: A list of state names (int, str, ...)
        :type initial: str, int,...
        :type finals: A list of state names (int, str, ...)
        """
        if alphabet:
            self.alphabet = alphabet
        else:
            self.alphabet = ["$"]
        if states:
            self.states = states
        else:
            self.states = [0]
        self.initial = initial
        if finals:
            self.finals = finals
        else:
            self.finals = list()
        self.transitions = dict()

    def add_state(self, state: int) -> None:
        """add_state
        Add a state to the FSM
        :param state: The state to add
        :type state: int
        :return: Nothing
        :rtype: None
        """
        if state not in self.states:
            self.states.append(state)

    def get_next_state(self) -> int:
        """get_next_state
        Get a free state
        :return: A free state
        :rtype: int
        """
        return max(self.states) + 1

    def add_transition(self, s_from, s_to, t_by):
        """add_transition
        Adds a transition from s_from to s_to through "t_by" to the fsm
        :param s_from: The origin of the transition
        :param s_to: The target of the transition
        :param t_by: The symbol of the transition
        :return: Nothing
        """
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

    def add_final(self, s_final: int) -> None:
        """add_final
        Adds a final state to the fsm
        :param s_final: The final state to add
        :rtype s_final: int
        :return: Nothing
        """
        if s_final not in self.finals:
            self.finals.append(s_final)
        if s_final not in self.states:
            self.states.append(s_final)

    def __repr__(self):
        """__repr__ Gives a string representation of the fsm to be used on the
        website http://ivanzuzak.info/noam/webapps/fsm2regex/
        :return: A string representing the fsm.
        :rtype: str
        """
        res = []
        res.append("#states")
        for state in self.states:
            res.append(str(state))
        res.append("#initial")
        res.append(str(self.initial))
        res.append("#accepting")
        for final in self.finals:
            res.append(str(final))
        res.append("#alphabet")
        for letter in self.alphabet:
            if letter != "$":
                res.append(str(letter))
        res.append("#transitions")
        for s_from in self.transitions:
            for s_to in self.transitions[s_from]:
                for letter in self.transitions[s_from][s_to]:
                    res.append(str(s_from) + ":" + str(letter) + ">"
                               + str(s_to))
        return "\n".join(res)

    def create_or(self):
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

    def remove_state_cleanup(self, state):
        """remove_state_cleanup
        Cleans the fsm after a state is removed.
        If the state is a final state, we do nothing (cannot delete end state).
        :param state: The state to delete
        :type state: int, str,...
        """
        if state not in self.finals:
            for s_other in self.states:
                if s_other in self.transitions.keys() and \
                        state in self.transitions[s_other].keys():
                    del self.transitions[s_other][state]
            self.states.remove(state)

    def clean_transition(self, state):
        """clean_transition
        Removes the transitions from state. If the state is a final state, we
        do not remove the transition to itself
        :param state: The state from which transitions are removed
        :type state: int, str,...
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

    def __remove_state_sub(self, state, to_me, s_other, letter0):
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

    def remove_state(self, state):
        """remove_state
        Removes a state from the fsm. We return if something changed or not.
        This is a function for traduction to a regex.
        :param state: The state to remove
        :type state: int, str, ...
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

    def get_final_strings(self):
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

    def to_regex(self):
        """to_regex Transforms the FSM to regex
        :return: A regex equivalent to the FSM
        :rtype: str
        """
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
            return ""
        # The transitions from the initial node to itself is a kleene star
        if self.initial in self.transitions[self.initial]:
            res += "(" + \
                "".join(self.transitions[self.initial][self.initial]) + ")*"
        # Get all the equivalent paths to the final states
        temp_finals = self.get_final_strings()
        from regex_tree import RegexTree
        # ... and creates an or of all of them
        if len(temp_finals) > 1:
            return RegexTree(Node(res + "(" + ")|(".join(temp_finals) + ")"))
        return RegexTree(Node(res + ")|(".join(temp_finals)))

    def close(self):
        """close Creates a kleene star around the fsm, by linking the final
        states to the initial state with an epsilon transition"""
        for final in self.finals:
            self.add_transition(final, self.initial, "$")

    def open(self):
        """open Removes the epsilon links between the final states and the
        initial state"""
        for final in self.finals:
            if final in self.transitions.keys():
                if self.initial in self.transitions[final].keys():
                    self.transitions[final][self.initial].remove("$")

    def exists_path(self, start_node, end, path):
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

    def apply_rule(self, rule_left, rule_right):
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

    def apply_rule_sub(self, rule_left, rule_right):
        """apply_rule_sub
        Make one pass of the Horn rule transformation
        :param rule_left: left part of the horn rule
        :param rule_right: right part of the horn rule
        :return: Whether the FSM was modified
        :rtype: Boolean
        """
        # rule_left => rule_right
        # Keep track of all previous states encountered when a given node was
        # reached
        seen_before = dict()
        # Nothing was seen before
        for state in self.states:
            seen_before[state] = []
        # A stack of elements to process (DFS)
        # We use RoundLists which are list which keep track only of the last
        # elements inserted
        to_process = [(self.initial, RoundList(len(rule_left)), False)]
        # Counter to prevent the duplication of nodes
        # Should be useless for horn rules
        counter = max(self.states) + 1
        # Whether there was a modification done
        was_modified = False
        while to_process:
            current = to_process.pop()
            current_node = current[0]
            current_rl = current[1]
            should_be_processed = current[2]
            # State already reached
            if current_rl in seen_before[current_node]:
                continue
            seen_before[current_node].append(current_rl)
            current_l = current_rl.get()
            # Should we add a new link?
            if rule_left == list(map(lambda x: x[1], current_l)) and\
                    not self.exists_path(current_l[0][0],
                                         current_node,
                                         rule_right) and\
                    should_be_processed:
                prev_first = current_l[0][0]
                # Should not be useful for Horn rule. It is here for testing
                # purposes
                for i in range(len(rule_right) - 1):
                    self.add_transition(prev_first, counter, rule_right[i])
                    prev_first = counter
                    seen_before[counter] = []
                    counter += 1
                self.add_transition(prev_first, current_node, rule_right[-1])
                was_modified = True
            # Continue exploration
            if current_node in self.transitions.keys():
                for s_to in self.transitions[current_node]:
                    for letter in self.transitions[current_node][s_to]:
                        next_rl = current_rl.copy()
                        # The empty symbols should be ignored
                        if letter != "$":
                            next_rl.push((current_node, letter))
                            to_process.append((s_to, next_rl, True))
                        if letter == "$":
                            to_process.append((s_to, next_rl, False))
        return was_modified
