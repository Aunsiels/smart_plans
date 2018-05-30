import unittest
from experiments.terminal import Terminal


class TestTerminal(unittest.TestCase):

    def test_creation(self):
        t = Terminal("T")
        self.assertIsInstance(t, Terminal)

    def test_repr(self):
        t = Terminal("T")
        self.assertEqual(str(t), "Terminal(T)")
