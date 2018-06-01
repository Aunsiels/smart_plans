class Variable(object):

    def __init__(self, variable):
        self.variable = variable

    def __repr__(self):
        return "Variable(" + str(self.variable) + ")"

    def __eq__(self, other):
        return isinstance(other, Variable) and other.variable == self.variable

    def __hash__(self):
        return hash(self.variable)

    def is_final(self):
        return False
