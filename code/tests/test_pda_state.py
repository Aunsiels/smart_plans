import unittest
from experiments.pda_state import PDAState

class TestPDAState(unittest.TestCase):

    def test_creation(self):
        state = PDAState("0")
        self.assertIsInstance(state, PDAState)

    def test_repr(self):
        state = PDAState("0")
        self.assertEqual(str(state), "PDAState(0)")
        state = PDAState(0)
        self.assertEqual(str(state), "PDAState(0)")

    def test_eq(self):
        state0 = PDAState("0")
        self.assertEqual(state0, state0)
        state1 = PDAState("0")
        self.assertEqual(state1, state0)
        self.assertEqual(state0, state1)
        state2 = PDAState(0)
        self.assertNotEqual(state0, state2)
        self.assertNotEqual(state2, state0)

    def test_hash(self):
        s = PDAState("0")
        self.assertEqual(hash(s), hash("0"))
        self.assertNotEqual(hash(s), hash(0))
