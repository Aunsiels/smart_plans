from round_list import RoundList


class FSM(object):

    def __init__(self, alphabet, states, initial, finals, transitions):
        self.alphabet = alphabet
        self.states = states
        self.initial = initial
        self.finals = finals
        self.transitions = transitions

    def add_transition(self, x, y, a):
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
        if x not in self.finals:
            self.finals.append(x)
        if x not in self.states:
            self.states.append(x)
        self.update_finals()

    def __repr__(self):
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

    def update_finals(self):
        temp = -1
        while temp < len(self.finals):
            temp = len(self.finals)
            temp_finals = self.finals[:]
            for final in temp_finals:
                if final in self.transitions.keys():
                    for y in self.transitions[final].keys():
                        if "$" in self.transitions[final][y] and\
                                y not in self.finals:
                            self.finals.append(y)

    def create_or(self):
        for x in self.transitions.keys():
            for y in self.transitions[x].keys():
                if len(self.transitions[x][y]) > 1:
                    self.transitions[x][y] = ["(" +
                                              ")|(".join(
                                                  self.transitions[x][y]) +
                                              ")"]

    def remove_state_cleanup(self, state, is_final):
        if not is_final:
            for s in self.states:
                if s in self.transitions.keys() and \
                        state in self.transitions[s].keys():
                    del self.transitions[s][state]
            self.states.remove(state)

    def clean_transition(self, state, is_final):
        to_remove = []
        for y in self.transitions[state]:
            if y != state:
                to_remove.append(y)
        for y in to_remove:
            del self.transitions[state][y]
        if not is_final:
            del self.transitions[state]

    def remove_state(self, state, is_final):
        res = False
        if state in self.transitions.keys():
            for s in self.states:
                if s != state and s in self.transitions.keys() and \
                        state in self.transitions[s].keys():
                    to_me = self.transitions[state].setdefault(state, [])
                    for l0 in self.transitions[s][state]:
                        for y in self.transitions[state]:
                            for l1 in self.transitions[state][y]:
                                if len(to_me) == 0 and y != state:
                                    self.add_transition(s, y, l0 + "," + l1)
                                    res = True
                                elif y != state:
                                    for l2 in to_me:
                                        self.add_transition(s, y, l0 +
                                                            ",(" + l2 + ")*" +
                                                            l1)
                                    res = True

            self.clean_transition(state, is_final)

        self.remove_state_cleanup(state, is_final)
        return res

    def get_final_strings(self):
        temp_finals = []
        for final in self.finals:
            if final in self.transitions[self.initial]:
                if self.initial == final:
                    temp_finals.append("(" + "".join(
                        self.transitions[self.initial][final]) + ")*")
                else:
                    temp_finals.append("".join(
                        self.transitions[self.initial][final]))
                    if final in self.transitions.keys() and\
                            final in self.transitions[final].keys():
                        temp_finals[-1] += "(" + \
                            "".join(self.transitions[final][final]) +\
                            ")*"
        return temp_finals

    def to_regex(self):
        temp_states = self.states[:]
        for state in temp_states:
            self.create_or()
            if state != self.initial and state not in self.finals:
                self.remove_state(state, False)
                self.update_finals()
        self.create_or()
        # Converges ?
        cont = True
        while cont:
            cont = False
            for final in self.finals:
                if final != self.initial:
                    cont |= self.remove_state(final, True)
                    self.create_or()
        res = ""
        if self.initial not in self.transitions:
            return ""
        if self.initial in self.transitions[self.initial]:
            res += "(" + \
                "".join(self.transitions[self.initial][self.initial]) + ")*"
        temp_finals = self.get_final_strings()
        from regex_tree import RegexTree
        if len(temp_finals) > 1:
            return RegexTree(res + "(" + ")|(".join(temp_finals) + ")")
        else:
            return RegexTree(res + ")|(".join(temp_finals))

    def close(self):
        for final in self.finals:
            self.add_transition(final, self.initial, "$")

    def open(self):
        for final in self.finals:
            if final in self.transitions.keys():
                if self.initial in self.transitions[final].keys():
                    self.transitions[final][self.initial].remove("$")

    def exists_path(self, start, end, l):
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
        # l0 => l1 Horn Rule
        was_modified = False
        while self.apply_rule_sub(l0, l1):
            was_modified = True
            continue
        return was_modified

    def apply_rule_sub(self, l0, l1):
        # l0 => l1
        seen_before = dict()
        for s in self.states:
            seen_before[s] = []
        to_process = [(self.initial, RoundList(len(l0)))]
        counter = max(self.states) + 1
        was_modified = False
        while len(to_process) > 0:
            current = to_process.pop()
            current_node = current[0]
            current_rl = current[1]
            if current_rl in seen_before[current_node]:
                continue
            seen_before[current_node].append(current_rl)
            current_l = current_rl.get()
            if l0 == list(map(lambda x: x[1], current_l)) and\
                    not self.exists_path(current_l[0][0], current_node, l1):
                prev_first = current_l[0][0]
                for i in range(len(l1) - 1):
                    self.add_transition(prev_first, counter, l1[i])
                    prev_first = counter
                    seen_before[counter] = []
                    counter += 1
                self.add_transition(prev_first, current_node, l1[-1])
                was_modified = True
            if current_node in self.transitions.keys():
                for y in self.transitions[current_node]:
                    for a in self.transitions[current_node][y]:
                        next_rl = current_rl.copy()
                        if a != "$":
                            next_rl.push((current_node, a))
                        to_process.append((y, next_rl))
        return was_modified
