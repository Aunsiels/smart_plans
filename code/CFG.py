class CFG(object):

    def __init__(self, variables, terminals, productions, start):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start = start

    def __repr__(self):
        res = "Variables: " + ", ".join(map(str, self.variables)) + "\n"
        res += "Terminals: " + ", ".join(map(str, self.terminals)) + "\n"
        res += "Productions:\n"
        res += "\n".join(map(str, self.productions)) + "\n"
        res += "Start: " + str(self.start)
