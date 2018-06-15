from CFG import CFG
from terminal import Terminal
from variable import Variable
from CFG_rule import CFGRule
from utils import inverse
from regex_tree import RegexTree
from node import Node

class ForwardBackwardCFG(CFG):

    def __init__(self, terminals, query):
        self.variables = [Variable("S"), Variable("C")]
        self.terminals = terminals[:]
        self.productions = [
            CFGRule(Variable("S"), [Variable("C"), Terminal(query),
                                    Variable("C")]),
            CFGRule(Variable("C"), [Variable("C"), Variable("C")]),
            CFGRule(Variable("C"), [])]
        for terminal in self.terminals:
            self.productions.append(
                CFGRule(Variable("C"), [Terminal(terminal), Variable("C"),
                                        Terminal(inverse(terminal))]))
        self.start = Variable("S")
        self.__empty = None

    def is_empty_regex(self, regex):
        if not isinstance(regex, RegexTree):
            regex = RegexTree(Node(regex))
        fsm = regex.to_fsm()
        fsm.close()
        cfg = self.intersect(fsm)
        return cfg.is_empty()
