import unittest
from experiments.variable import Variable


class TestVariable(unittest.TestCase):

    def test_creation(self):
        v = Variable("T")
        self.assertIsInstance(v, Variable)

    def test_repr(self):
        v = Variable("T")
        self.assertEqual(str(v), "Variable(T)")

    def test_eq(self):
        v0 = Variable("T")
        self.assertEqual(v0, v0)
        v1 = Variable("T")
        self.assertEqual(v1, v0)
        self.assertEqual(v0, v1)
        v2 = Variable("M")
        self.assertNotEqual(v2, v0)
        self.assertNotEqual(v0, v2)

    def test_set(self):
        v0 = Variable("T")
        v1 = Variable("T")
        v2 = Variable("M")
        s = set()
        s.add(v0)
        self.assertIn(v0, s)
        self.assertIn(v1, s)
        self.assertNotIn(v2, s)
