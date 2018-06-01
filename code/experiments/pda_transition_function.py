class PDATransitionFunction(object):

    def __init__(self, state_from, input_symbol, stack_from, state_to,
                 stack_to):
        self.state_from = state_from
        self.input_symbol = input_symbol
        self.stack_from = stack_from
        self.state_to = state_to
        self.stack_to = stack_to

    def __repr__(self):
        return "(" + str(self.state_from) + ", " + \
            str(self.input_symbol) + ", " + \
            str(self.stack_from) + ") -> (" + \
            str(self.state_to) + ", " + \
            str(self.stack_to) + ")"

    def __eq__(self, other):
        return isinstance(other, PDATransitionFunction) and\
            self.state_from == other.state_from and\
            self.input_symbol == other.input_symbol and\
            self.stack_from == other.stack_from and\
            self.state_to == other.state_to and\
            self.stack_to == other.stack_to

    def __hash__(self):
        return hash(self.state_from) +\
            hash(self.stack_from) +\
            hash(self.input_symbol) +\
            hash(self.state_to) +\
            hash(tuple(self.stack_to))

    def accepts(self, state, input_symbol, stack):
        if len(stack) == 0:
            if self.stack_from == "epsilon":
                return True
            else:
                return False
        return self.state_from == state and \
            self.input_symbol == input_symbol and \
            stack[0] == self.stack_from

    def transform(self, state, input_symbol, stack):
        if not self.accepts(state, input_symbol, stack):
            raise ValueError
        if len(stack) == 0:
            return (self.state_to, self.stack_to[:])
        return (self.state_to, self.stack_to[:] + stack[1:])
