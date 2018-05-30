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
