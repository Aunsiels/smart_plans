from round_list import RoundList
from node import Node


class FSM(object):
    """FSM Finite State Machine. The methods modify the object"""

    def __init__(self,
                 alphabet=["$"],
                 states=[0],
                 initial=0,
                 finals=[],
                 transitions=dict()):
        """__init__ Creates a new fsm
        The empty symbol is $
        :param alphabet: the alphabet of the fsm
        :param states: the list of states in the fsm
        :param initial: the initial state
        :param finals: the final states
        :param transitions: The transitions, as a dict of dict of lists of\
            alphabets symbols
        :type alphabet: A list of strings
        :type states: A list of state names (int, str, ...)
        :type initial: str, int,...
        :type finals: A list of state names (int, str, ...)
        :type transitions: A map from a state to a map from state to \
            a list of alphabet symbole. transition[x][y] is the list of\
            transitions from x to y
        """
        self.alphabet = alphabet
        self.states = states
        self.initial = initial
        self.finals = finals
        self.transitions = transitions

    def add_state(self, x):
        if x not in states:
            self.states.append(x)

    def get_next_state(self):
        return max(self.states) + 1

    def add_transition(self, x, y, a):
        """add_transition
        Adds a transition from x to y through a to the fsm
        :param x: The origin of the transition
        :param y: The target of the transition
        :param a: The symbol of the transition
        :return: Nothing
        """
        if x not in self.states:
            self.states.append(x)
        if y not in self.states:
            self.states.append(y)
        if a not in self.alphabet:
            self.alphabet.append(a)
        if x in self.transitions.keys():
            if y in self.transitions[x].keys():
                if a not in self.transitions[x][y]:
                    self.transitions[x][y].append(a)
            else:
                self.transitions[x][y] = [a]
        else:
            self.transitions[x] = dict()
            self.transitions[x][y] = [a]

    def add_final(self, x):
        """add_final
        Adds a final state to the fsm
        :param x: The final state to add
        :rtype x: int, str,...
        :return: Nothing
        """
        if x not in self.finals:
            self.finals.append(x)
        if x not in self.states:
            self.states.append(x)

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
        for a in self.alphabet:
            if a != "$":
                res.append(str(a))
        res.append("#transitions")
        for x in self.transitions.keys():
            for t in self.transitions[x].keys():
                for a in self.transitions[x][t]:
                    res.append(str(x) + ":" + str(a) + ">" + str(t))
        return "\n".join(res)

    def create_or(self):
        """create_or Method used in the transformation to a regex tree. If
        several transition exist between two states x and y, then we create a
        transition which is the or of all others"""
        for x in self.transitions.keys():
            for y in self.transitions[x].keys():
                if len(self.transitions[x][y]) > 1:
                    # Replace all previous transitions
                    self.transitions[x][y] = ["(" +
                                              ")|(".join(
                                                  self.transitions[x][y]) +
                                              ")"]

    def remove_state_cleanup(self, state):
        """remove_state_cleanup
        Cleans the fsm after a state is removed.
        If the state is a final state, we do nothing (cannot delete end state).
        :param state: The state to delete
        :type state: int, str,...
        """
        if state not in self.finals:
            for s in self.states:
                if s in self.transitions.keys() and \
                        state in self.transitions[s].keys():
                    del self.transitions[s][state]
            self.states.remove(state)

    def clean_transition(self, state):
        """clean_transition
        Removes the transitions from state. If the state is a final state, we
        do not remove the transition to itself
        :param state: The state from which transitions are removed
        :type state: int, str,...
        """
        to_remove = []
        for y in self.transitions[state]:
            # We do not want to remove transitions to itself to final nodes
            if y != state:
                to_remove.append(y)
        for y in to_remove:
            del self.transitions[state][y]
        if state not in self.finals:
            del self.transitions[state]

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
        if state in self.transitions.keys():
            for s in self.states:
                if s != state and s in self.transitions.keys() and \
                        state in self.transitions[s].keys():
                    # Links to the states itself
                    to_me = self.transitions[state].setdefault(state, [])
                    # We look for paths of the type x -> state -> y to be able
                    # to recreate it as it will be deleted
                    for l0 in self.transitions[s][state]:
                        for y in self.transitions[state]:
                            for l1 in self.transitions[state][y]:
                                if len(to_me) == 0 and y != state:
                                    # To link to itself, simply concatenate
                                    self.add_transition(s, y, l0 + "," + l1)
                                    res = True
                                elif y != state:
                                    # If there is a link to itself, we have a
                                    # a kleene star
                                    for l2 in to_me:
                                        self.add_transition(s, y, l0 +
                                                            ",(" + l2 + ")*" +
                                                            l1)
                                    res = True

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
        else:
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

    def exists_path(self, start, end, l):
        """exists_path
        Does the given path between two nodes exists?
        :param start: The starting node
        :param end: The ending node
        :param l: The path to consider
        :return: Whether the path l exists between start and end
        :rtype: Boolean
        """
        # Contains the nodes reached so far
        # It is a kind of BFS
        starts = [start]
        for rel in l:
            next_starts = []
            for s in starts:
                if s in self.transitions:
                    for y in self.transitions[s]:
                        if rel in self.transitions[s][y]:
                            next_starts.append(y)
            starts = next_starts
        return end in starts

    def apply_rule(self, l0, l1):
        """apply_rule
        Apply a Horn rule
        :param l0: left part of the horn rule
        :param l1: right part of the horn rule
        :return: Whether the FSM was modified
        :rtype: Boolean
        """
        # l0 => l1 Horn Rule
        was_modified = False
        # While there are modifications, we continue
        while self.apply_rule_sub(l0, l1):
            was_modified = True
            continue
        return was_modified

    def apply_rule_sub(self, l0, l1):
        """apply_rule_sub
        Make one pass of the Horn rule transformation
        :param l0: left part of the horn rule
        :param l1: right part of the horn rule
        :return: Whether the FSM was modified
        :rtype: Boolean
        """
        # l0 => l1
        # Keep track of all previous states encountered when a given node was
        # reached
        seen_before = dict()
        # Nothing was seen before
        for s in self.states:
            seen_before[s] = []
        # A stack of elements to process (DFS)
        # We use RoundLists which are list which keep track only of the last
        # elements inserted
        to_process = [(self.initial, RoundList(len(l0)), False)]
        # Counter to prevent the duplication of nodes
        # Should be useless for horn rules
        counter = max(self.states) + 1
        # Whether there was a modification done
        was_modified = False
        while len(to_process) > 0:
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
            if l0 == list(map(lambda x: x[1], current_l)) and\
                    not self.exists_path(current_l[0][0], current_node, l1) and\
                    should_be_processed:
                prev_first = current_l[0][0]
                # Should not be useful for Horn rule. It is here for testing
                # purposes
                for i in range(len(l1) - 1):
                    self.add_transition(prev_first, counter, l1[i])
                    prev_first = counter
                    seen_before[counter] = []
                    counter += 1
                self.add_transition(prev_first, current_node, l1[-1])
                was_modified = True
            # Continue exploration
            if current_node in self.transitions.keys():
                for y in self.transitions[current_node]:
                    for a in self.transitions[current_node][y]:
                        next_rl = current_rl.copy()
                        # The empty symbols should be ignored
                        if a != "$":
                            next_rl.push((current_node, a))
                            to_process.append((y, next_rl, True))
                        if a == "$":
                            to_process.append((y, next_rl, False))
        return was_modified
