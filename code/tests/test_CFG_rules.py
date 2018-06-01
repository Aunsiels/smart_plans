import unittest
from experiments.CFG_rule import CFGRule
from experiments.variable import Variable
from experiments.terminal import Terminal


class TestCFGRule(unittest.TestCase):

    def test_creation(self):
        rule = CFGRule(Variable("S"), [Terminal("a"), Variable("I")])
        self.assertIsInstance(rule, CFGRule)

    def test_repr(self):
        rule = CFGRule(Variable("S"), [Terminal("a"), Variable("I")])
        self.assertEqual(str(rule), "Variable(S) -> Terminal(a), Variable(I)")

    def test_eq(self):
        rule0 = CFGRule(Variable("S"), [Terminal("a"), Variable("I")])
        self.assertEqual(rule0, rule0)
        rule1 = CFGRule(Variable("S"), [Terminal("a"), Variable("I")])
        self.assertEqual(rule1, rule0)
        self.assertEqual(rule0, rule1)
        rule2 = CFGRule(Variable("S"), [Terminal("b"), Variable("I")])
        self.assertNotEqual(rule0, rule2)
