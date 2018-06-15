class Variable(object):

    def __init__(self, variable):
        self.variable = variable
        self.__hash = None

    def __repr__(self):
        return "Variable(" + str(self.variable) + ")"

    def __eq__(self, other):
        return isinstance(other, Variable) and other.variable == self.variable

    def __hash__(self):
        if self.__hash is None:
            self.__hash = hash(self.variable)
        return self.__hash

    def is_final(self):
        return False
