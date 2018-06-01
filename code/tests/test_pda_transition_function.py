import unittest
from experiments.pda_transition_function import PDATransitionFunction
from experiments.pda_state import PDAState

class TestPDATransitionFunction(unittest.TestCase):

    def test_creation(self):
        trans = PDATransitionFunction(PDAState("S"), "a", "S",
                                      PDAState("I"), ["B"])
        self.assertIsInstance(trans, PDATransitionFunction)

    def test_repr(self):
        trans = PDATransitionFunction(PDAState("S"), "a", "S",
                                      PDAState("I"), ["B"])
        self.assertEqual(str(trans), "(PDAState(S), a, S) -> "
                         "(PDAState(I), ['B'])")

    def test_accepts(self):
        trans = PDATransitionFunction(PDAState("S"), "a", "S",
                                      PDAState("I"), ["B"])
        self.assertTrue(trans.accepts(PDAState("S"), "a", "S"))
        self.assertFalse(trans.accepts(PDAState("S"), "a", "Q"))
        self.assertFalse(trans.accepts(PDAState("S"), "b", "S"))
        self.assertFalse(trans.accepts(PDAState("Q"), "a", "S"))

    def test_transform(self):
        trans = PDATransitionFunction(PDAState("S"), "a", "S",
                                      PDAState("I"), ["B"])
        self.assertEqual(trans.transform(PDAState("S"), "a", ["S"]),
                         (PDAState("I"), ["B"]))
        self.assertEqual(trans.transform(PDAState("S"), "a", ["S", "Q"]),
                         (PDAState("I"), ["B", "Q"]))
        self.assertRaises(ValueError,
                          trans.transform, PDAState("S"), "b", ["S"])
        self.assertRaises(ValueError,
                          trans.transform, PDAState("Q"), "a", ["S"])

    def test_eq(self):
        trans0 = PDATransitionFunction(PDAState("S"), "a", ["S"],
                                      PDAState("I"), ["B"])
        self.assertEqual(trans0, trans0)
        trans1 = PDATransitionFunction(PDAState("S"), "a", ["S"],
                                      PDAState("I"), ["B"])
        self.assertEqual(trans1, trans0)
        self.assertEqual(trans0, trans1)
        trans2 = PDATransitionFunction(PDAState("S"), "b", ["S"],
                                      PDAState("I"), ["B"])
        self.assertNotEqual(trans0, trans2)
        temp = [trans0]
        self.assertIn(trans1, temp)
