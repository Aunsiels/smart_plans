import unittest
from CFG import CFG
from terminal import Terminal
from variable import Variable
from CFG_rule import CFGRule
from PDA import PDA
from pda_state import PDAState
from pda_transition_function import PDATransitionFunction
from regex_tree import RegexTree
from node import Node

class TestCFG(unittest.TestCase):

    def test_creation(self):
        cfg = CFG([], [], [], Variable(""))
        self.assertIsInstance(cfg, CFG)

    def test_repr(self):
        cfg = CFG([Variable("I"), Variable("J")],
                  [Terminal("a"), Terminal("b")],
                  [CFGRule(Variable("I"), [Terminal("a"), Variable("I")])],
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

    def test_emptiness(self):
        cfg = CFG([Variable("S"), Variable("A"), Variable("B")],
                  [Terminal("a"), Terminal("b")],
                  [CFGRule(Variable("S"), [Variable("A"), Variable("B")]),
                   CFGRule(Variable("S"), [Terminal("a")]),
                   CFGRule(Variable("A"), [Terminal("b")])],
                  Variable("S"))
        self.assertEqual(set([Variable("S"), Variable("A"), Terminal("a"),
                              Terminal("b")]), cfg.get_reachable())
        self.assertFalse(cfg.is_empty())
        cfg = CFG([Variable("S"), Variable("A"), Variable("B")],
                  [Terminal("a"), Terminal("b")],
                  [CFGRule(Variable("S"), [Variable("A"), Variable("B")]),
                   CFGRule(Variable("S"), [Terminal("a")]),
                   CFGRule(Variable("A"), [Terminal("b")])],
                  Variable("B"))
        self.assertEqual(set([Variable("S"), Variable("A"), Terminal("a"),
                              Terminal("b")]), cfg.get_reachable())
        self.assertTrue(cfg.is_empty())

    def test_iter(self):
        cfg = CFG([Variable("S"), Variable("A"), Variable("B"), Variable("C")],
                  [Terminal("a"), Terminal("b")],
                  [CFGRule(Variable("S"), [Variable("A"), Variable("B")]),
                   CFGRule(Variable("S"), [Terminal("a")]),
                   CFGRule(Variable("A"), [Terminal("b")]),
                   CFGRule(Variable("A"), [Variable("C")])],
                  Variable("S"))
        words = [x for x in cfg]
        self.assertEqual(words, [[Terminal("a")]])
        cfg = CFG([Variable("S"), Variable("A"), Variable("C")],
                  [Terminal("a"), Terminal("b")],
                  [CFGRule(Variable("S"), [Variable("A")]),
                   CFGRule(Variable("S"), [Terminal("a")]),
                   CFGRule(Variable("A"), [Terminal("b")]),
                   CFGRule(Variable("A"), [Variable("C")])],
                  Variable("S"))
        words = [x for x in cfg]
        self.assertIn([Terminal("a")], words)
        self.assertIn([Terminal("b")], words)
        self.assertEqual(len(words), 2)
        cfg = CFG([Variable("S"), Variable("A"), Variable("B")],
                  [Terminal("a"), Terminal("b")],
                  [CFGRule(Variable("S"), [Variable("S"), Variable("S")]),
                   CFGRule(Variable("S"), [Terminal("a")]),
                   CFGRule(Variable("A"), [Terminal("b")])],
                  Variable("S"))
        it = iter(cfg)
        word = next(it)
        self.assertEqual(set(word), set([Terminal("a")]))
        word = next(it)
        self.assertEqual(set(word), set([Terminal("a")]))
        word = next(it)
        self.assertEqual(set(word), set([Terminal("a")]))
        word = next(it)
        self.assertEqual(set(word), set([Terminal("a")]))
        word = next(it)
        self.assertEqual(set(word), set([Terminal("a")]))
        cfg = CFG([Variable("S"), Variable("A"), Variable("B")],
                  [Terminal("a"), Terminal("b")],
                  [CFGRule(Variable("S"), [Variable("A"), Variable("S")]),
                   CFGRule(Variable("S"), [Terminal("a")]),
                   CFGRule(Variable("A"), [Terminal("b")])],
                  Variable("S"))
        it = iter(cfg)
        temp = [next(it) for _ in range(100)]
        self.assertIn([Terminal("b"), Terminal("b"), Terminal("b"),
                       Terminal("a")], temp)

    def test_to_pda(self):
        cfg = CFG([Variable("E"), Variable("I")],
                  [Terminal("a"), Terminal("b"), Terminal("0"),
                   Terminal("1"), Terminal("+"), Terminal("*"),
                   Terminal("("), Terminal(")")],
                  [CFGRule(Variable("I"), [Terminal("a")]),
                   CFGRule(Variable("I"), [Terminal("b")]),
                   CFGRule(Variable("I"), [Variable("I"), Terminal("a")]),
                   CFGRule(Variable("I"), [Variable("I"), Terminal("b")]),
                   CFGRule(Variable("I"), [Variable("I"), Terminal("0")]),
                   CFGRule(Variable("I"), [Variable("I"), Terminal("1")]),
                   CFGRule(Variable("E"), [Variable("I")]),
                   CFGRule(Variable("E"), [Variable("E"), Terminal("*"),
                                           Variable("E")]),
                   CFGRule(Variable("E"), [Variable("E"), Terminal("+"),
                                           Variable("E")]),
                   CFGRule(Variable("E"), [Terminal("("), Variable("E"),
                                           Terminal(")")])],
                  Variable("E"))
        pda = cfg.to_PDA()
        self.assertIsInstance(pda, PDA)
        self.assertIn(PDATransitionFunction(PDAState("q"),
                                            "epsilon",
                                            Variable("I"),
                                            PDAState("q"),
                                            [Terminal("a")]),
                      pda.transition_function)
        self.assertIn(PDATransitionFunction(PDAState("q"),
                                            "epsilon",
                                            Variable("I"),
                                            PDAState("q"),
                                            [Variable("I"), Terminal("0")]),
                      pda.transition_function)
        self.assertIn(PDATransitionFunction(PDAState("q"),
                                            "epsilon",
                                            Variable("E"),
                                            PDAState("q"),
                                            [Variable("I")]),
                      pda.transition_function)
        self.assertEqual(18, len(pda.transition_function))
        self.assertTrue(pda.accepts_by_empty_stack([Terminal("a")], 100))
        self.assertTrue(pda.accepts_by_empty_stack([Terminal("b")], 100))
        self.assertFalse(pda.accepts_by_empty_stack(
            [Terminal(x) for x in "b0"], 100))
        self.assertTrue(pda.accepts_by_empty_stack(
            [Terminal(x) for x in "b0"], 1000))
        self.assertTrue(pda.accepts_by_empty_stack(
            [Terminal(x) for x in "b00"], 10000))

    def test_intersect(self):
        cfg = CFG([Variable("S"), Variable("A")],
                  [Terminal("a"), Terminal("b")],
                  [CFGRule(Variable("S"), [Variable("A"), Variable("A")]),
                   CFGRule(Variable("S"), [Terminal("a")]),
                   CFGRule(Variable("A"), [Terminal("b")])],
                  Variable("S"))
        regex = RegexTree(Node("a"))
        fsm = regex.to_fsm()
        fsm.close()
        cfg_temp = cfg.intersect(fsm)
        self.assertFalse(cfg_temp.is_empty())
        regex = RegexTree(Node("b"))
        fsm = regex.to_fsm()
        fsm.close()
        cfg_temp = cfg.intersect(fsm)
        self.assertFalse(cfg_temp.is_empty())
        regex = RegexTree(Node("b,b"))
        fsm = regex.to_fsm()
        fsm.close()
        cfg_temp = cfg.intersect(fsm)
        self.assertFalse(cfg_temp.is_empty())
        regex = RegexTree(Node("b,a"))
        fsm = regex.to_fsm()
        fsm.close()
        cfg_temp = cfg.intersect(fsm)
        self.assertTrue(cfg_temp.is_empty())

    def test_paper(self):
        cfg = CFG([Variable("S"), Variable("C")],
                  [Terminal("a"), Terminal("b"), Terminal("c"), Terminal("q"),
                   Terminal("am"), Terminal("bm"), Terminal("cm"),
                   Terminal("qm")],
                  [CFGRule(Variable("S"), [Variable("C"), Terminal("q"),
                                           Variable("C")]),
                   CFGRule(Variable("C"), [Terminal("a"), Variable("C"),
                                           Terminal("am")]),
                   CFGRule(Variable("C"), [Terminal("b"), Variable("C"),
                                           Terminal("bm")]),
                   CFGRule(Variable("C"), [Terminal("c"), Variable("C"),
                                           Terminal("cm")]),
                   CFGRule(Variable("C"), [Terminal("q"), Variable("C"),
                                           Terminal("qm")]),
                   CFGRule(Variable("C"), [Variable("C"), Variable("C")]),
                   CFGRule(Variable("C"), [])],
                  Variable("S"))
        regex = RegexTree(Node("(a,b)|(bm,c)|(cm,am,q)"))
        fsm = regex.to_fsm()
        fsm.close()
        cfg_temp = cfg.intersect(fsm)
        self.assertFalse(cfg_temp.is_empty())
        regex = RegexTree(Node("(a,b)|(b,c)|(cm,am,q)"))
        fsm = regex.to_fsm()
        fsm.close()
        cfg_temp = cfg.intersect(fsm)
        self.assertTrue(cfg_temp.is_empty())


if __name__ == '__main__':
    unittest.main()
