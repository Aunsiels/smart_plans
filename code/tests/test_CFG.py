import unittest
from experiments.CFG import CFG
from experiments.terminal import Terminal
from experiments.variable import Variable
from experiments.CFG_rule import CFGRule

class TestCFG(unittest.TestCase):

    def test_creation(self):
        cfg = CFG([], [], [], Variable(""))
        self.assertIsInstance(cfg, CFG)

    def test_repr(self):
        cfg = CFG([Variable("I"), Variable("J")],
                  [Terminal("a"), Terminal("b")],
                  [CFGRule(Terminal("I"), [Terminal("a"), Variable("I")])],
                  Variable("I"))
        r = str(cfg)
        self.assertIn(str(Variable("I")), r)
        self.assertIn(str(Variable("J")), r)
        self.assertIn(str(Terminal("a")), r)
        self.assertIn(str(Terminal("b")), r)
        self.assertIn("Variables", r)
        self.assertIn("Terminals", r)
        self.assertIn("Productions", r)
        self.assertIn("Start", r)
        self.assertEqual(r.count("->"), 1)
        self.assertEqual(r.count("\n"), 4)


if __name__ == "__main__":
    unittest.main()
