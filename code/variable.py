class Variable(object):

    def __init__(self, variable):
        self.variable = variable

    def __repr__(self):
        return "Variable(" + str(self.variable) + ")"
