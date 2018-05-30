import unittest
from experiments.variable import Variable


class TestVariable(unittest.TestCase):

    def test_creation(self):
        v = Variable("T")
        self.assertIsInstance(v, Variable)

    def test_repr(self):
        v = Variable("T")
        self.assertEqual(str(v), "Variable(T)")
