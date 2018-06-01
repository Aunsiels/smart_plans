from queue import Queue
from pda_state import PDAState
from pda_transition_function import PDATransitionFunction

class CFG(object):

    def __init__(self, variables, terminals, productions, start):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start = start
        self.__empty = None

    def __repr__(self):
        res = "Variables: " + ", ".join(map(str, self.variables)) + "\n"
        res += "Terminals: " + ", ".join(map(str, self.terminals)) + "\n"
        res += "Productions:\n"
        res += "\n".join(map(str, self.productions)) + "\n"
        res += "Start: " + str(self.start)
        return res

    def is_empty(self):
        generating = self.get_reachable()
        return self.start not in generating

    def get_reachable(self):
        generating = set(self.terminals[:])
        modified = True
        while modified:
            modified = False
            for rule in self.productions:
                if all(map(lambda x: x in generating or x == "epsilon",
                           rule.body)):
                    if rule.head not in generating:
                        generating.add(rule.head)
                        modified = True
        return generating

    def __is_final(self, states):
        return all(map(lambda x: x == "epsilon" or x.is_final(), states))

    def __is_valid(self, states):
        return all(map(lambda x: x in self.__reachable or x == "epsilon",
                       states))

    def __iter__(self):
        self.__iter_states = Queue()
        self.__iter_states.put([self.start])
        self.__empty = self.is_empty()
        self.__reachable = self.get_reachable()
        return self

    def __next__(self):
        if self.__empty or self.__iter_states.empty():
            raise StopIteration
        else:
            while not self.__iter_states.empty():
                current = self.__iter_states.get()
                if not self.__is_valid(current):
                    continue
                if self.__is_final(current):
                    return list(filter(lambda x: x != "epsilon", current))
                split = 0
                for i in range(len(current)):
                    if current[i] == "epsilon":
                        continue
                    elif not current[i].is_final():
                        split = i
                        break
                for rule in self.productions:
                    if rule.head == current[i]:
                        self.__iter_states.put(current[:i] + rule.body +
                                             current[i+1:])
            raise StopIteration

    def to_PDA(self):
        from PDA import PDA
        states = [PDAState("q")]
        input_symbols = self.terminals[:]
        stack_symbols = self.terminals[:] + self.variables[:]
        start_state = states[0]
        start_symbol = self.start
        final_states = []
        transition = []
        for rule in self.productions:
            transition.append(PDATransitionFunction(
                states[0],
                "epsilon",
                rule.head,
                states[0],
                rule.body))
        for terminal in self.terminals:
            transition.append(PDATransitionFunction(
                states[0],
                terminal,
                terminal,
                states[0],
                []))
        return PDA(states, input_symbols, stack_symbols, transition,
                   start_state, start_symbol, final_states)

    def intersect(self, fsm):
        pda = self.to_PDA()
        pda = pda.from_empty_stack_to_final_state()
        pda = pda.intersect(fsm)
        pda = pda.from_final_state_to_empty_stack()
        return pda.to_CFG()
