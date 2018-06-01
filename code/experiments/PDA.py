from queue import Queue
from variable import Variable
from terminal import Terminal
from CFG_rule import CFGRule
from itertools import product
from pda_transition_function import PDATransitionFunction
from pda_state import PDAState

class PDA(object):

    def __init__(self, states, input_symbols, stack_alphabet,
                 transition_function, start_state, start_symbol, final_states):
        self.states = states
        self.input_symbols = input_symbols
        self.stack_alphabet = stack_alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.start_symbol = start_symbol
        self.final_states = final_states

    def from_empty_stack_to_final_state(self):
        states = self.states[:]
        start_state = PDAState("p_start_e_to_f")
        final_states = [PDAState("p_final_e_to_f")]
        states.append(start_state)
        states.append(final_states[0])
        stack_alphabet = self.stack_alphabet[:]
        input_symbols = self.input_symbols[:]
        start_symbol = Terminal("X_start_end_e_to_f")
        stack_alphabet.append(start_symbol)
        transition_function = self.transition_function[:]
        transition_function.append(PDATransitionFunction(
            start_state, "epsilon", start_symbol,
            self.start_state, [self.start_symbol, start_symbol]))
        for q in self.states:
            transition_function.append(PDATransitionFunction(
                q, "epsilon", start_symbol,
                final_states[0], []))
        return PDA(states, input_symbols, stack_alphabet,
                 transition_function, start_state, start_symbol, final_states)

    def from_final_state_to_empty_stack(self):
        states = self.states[:]
        start_state = PDAState("p_start_f_to_e")
        final_states = [PDAState("p_final_f_to_e")]
        states.append(start_state)
        states.append(final_states[0])
        stack_alphabet = self.stack_alphabet[:]
        input_symbols = self.input_symbols[:]
        start_symbol = Terminal("X_start_end_f_to_e")
        stack_alphabet.append(start_symbol)
        transition_function = self.transition_function[:]
        transition_function.append(PDATransitionFunction(
            start_state, "epsilon", start_symbol,
            self.start_state, [self.start_symbol, start_symbol]))

        for q in stack_alphabet:
            transition_function.append(PDATransitionFunction(
                final_states[0], "epsilon", q,
                final_states[0], []))

        for final in self.final_states:
            for q in stack_alphabet:
                transition_function.append(PDATransitionFunction(
                    final, "epsilon", q,
                    final_states[0], []))
        return PDA(states, input_symbols, stack_alphabet,
                 transition_function, start_state, start_symbol, final_states)

    def accepts_by_final_state(self, word, limit=-1):
        return self.__accepts(word, True, limit)

    def accepts_by_empty_stack(self, word, limit=-1):
        return self.__accepts(word, False, limit)

    def __accepts(self, word, final, limit=-1):
        current_state = Queue()
        current_state.put((self.start_state, word, [self.start_symbol]))
        counter = 0
        while not current_state.empty():
            if counter == limit:
                break
            counter += 1
            current = current_state.get()
            if len(current[1]) == 0:
                if (final and current[0] in self.final_states) or\
                        (not final and len(current[2]) == 0):
                    return True
                else:
                    for trans in self.transition_function:
                        if trans.accepts(current[0], "epsilon", current[2]):
                            new_state, new_stack = trans.transform(current[0],
                                                                   "epsilon",
                                                                   current[2])
                            current_state.put((new_state,
                                               current[1][:],
                                               new_stack))
                    continue
            for trans in self.transition_function:
                if trans.accepts(current[0], current[1][0], current[2]):
                    new_state, new_stack = trans.transform(current[0],
                                                           current[1][0],
                                                           current[2])
                    current_state.put((new_state,
                                       current[1][1:],
                                       new_stack))
                if trans.accepts(current[0], "epsilon", current[2]):
                    new_state, new_stack = trans.transform(current[0],
                                                           "epsilon",
                                                           current[2])
                    current_state.put((new_state,
                                       current[1][:],
                                       new_stack))
        return False

    def to_CFG(self):
        from CFG import CFG
        start = Variable("S")
        variables = set()
        variables.add(start)
        terminals = list(map(Terminal, self.input_symbols[:]))
        productions = []
        for p in self.states:
            productions.append(CFGRule(start, [Variable(str(self.start_state) +
                                                        "," +
                                                        str(self.start_symbol) +
                                                        "," +
                                                        str(p))]))
        for trans in self.transition_function:
            size = len(trans.stack_to)
            s_to = trans.stack_to
            for states in product(self.states, repeat=size):
                if size == 0:
                    head = Variable(str(trans.state_from) + "," +
                                    str(trans.stack_from) + "," +
                                    str(trans.state_to))
                else:
                    head = Variable(str(trans.state_from) + "," +
                                    str(trans.stack_from) + "," +
                                    str(states[-1]))
                variables.add(head)
                body = []
                if trans.input_symbol != "epsilon":
                    body.append(Terminal(trans.input_symbol))
                else:
                    body.append(trans.input_symbol)
                previous = trans.state_to
                for i in range(size):
                    body.append(Variable(str(previous) + "," +
                                         str(s_to[i]) + "," +
                                         str(states[i])))
                    variables.add(body[-1])
                    previous = states[i]
                productions.append(CFGRule(head, body))
        variables = list(variables)
        return CFG(variables, terminals, productions, start)

    def intersect(self, fsm):
        states = set()
        input_symbols = self.input_symbols[:]
        stack_alphabet = self.stack_alphabet[:]
        start_state = PDAState(str(self.start_state) + "," +
                               str(fsm.initial))
        start_symbol = self.start_symbol
        final_states = []
        for final_self in self.final_states:
            for final_fsm in fsm.finals:
                final_states.append(PDAState(str(final_self) + "," +
                                             str(final_fsm)))

        transition_function = []
        transitions_temp = fsm.transitions
        for key_from in transitions_temp:
            for key_to in transitions_temp[key_from]:
                for a in transitions_temp[key_from][key_to]:
                    for trans in self.transition_function:
                        t = type(trans.input_symbol)
                        if trans.input_symbol == t(a) or\
                                (trans.input_symbol == "epsilon" and
                                 a == "$"):
                            states.add(PDAState(str(trans.state_from) + "," +
                                                str(key_from)))
                            states.add(PDAState(str(trans.state_to) + "," +
                                                str(key_to)))
                            transition_function.append(
                                PDATransitionFunction(
                                    PDAState(str(trans.state_from) + "," +
                                             str(key_from)),
                                    trans.input_symbol,
                                    trans.stack_from,
                                    PDAState(str(trans.state_to) + "," +
                                             str(key_to)),
                                    trans.stack_to[:]))
        for state in fsm.states:
            for trans in self.transition_function:
                if trans.input_symbol == "epsilon":
                    states.add(PDAState(str(trans.state_from) + "," +
                                        str(state)))
                    states.add(PDAState(str(trans.state_to) + "," +
                                        str(state)))
                    transition_function.append(
                        PDATransitionFunction(
                            PDAState(str(trans.state_from) + "," +
                                     str(state)),
                            trans.input_symbol,
                            trans.stack_from,
                            PDAState(str(trans.state_to) + "," +
                                     str(state)),
                            trans.stack_to[:]))
        states = list(states)
        return PDA(states, input_symbols, stack_alphabet,
                   transition_function, start_state, start_symbol, final_states)
