class Terminal(object):

    def __init__(self, terminal):
        self.terminal = terminal

    def __repr__(self):
        return "Terminal(" + str(self.terminal) + ")"

    def __eq__(self, other):
        return isinstance(other, Terminal) and other.terminal == self.terminal

    def __hash__(self):
        return hash(self.terminal)

    def is_final(self):
        return True
