class PDAState(object):

    def __init__(self, state):
        self.state = state
        self.representation = "PDAState(" + str(self.state) + ")"

    def __repr__(self):
        return self.representation

    def __eq__(self, other):
        return isinstance(other, PDAState) and self.state == other.state

    def __hash__(self):
        return hash(self.state)
