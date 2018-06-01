import unittest
from experiments.terminal import Terminal


class TestTerminal(unittest.TestCase):

    def test_creation(self):
        t = Terminal("T")
        self.assertIsInstance(t, Terminal)

    def test_repr(self):
        t = Terminal("T")
        self.assertEqual(str(t), "Terminal(T)")

    def test_eq(self):
        t0 = Terminal("T")
        self.assertEqual(t0, t0)
        t1 = Terminal("T")
        self.assertEqual(t1, t0)
        self.assertEqual(t0, t1)
        t2 = Terminal("M")
        self.assertNotEqual(t2, t0)
        self.assertNotEqual(t0, t2)

    def test_set(self):
        t0 = Terminal("T")
        t1 = Terminal("T")
        t2 = Terminal("M")
        s = set()
        s.add(t0)
        self.assertIn(t0, s)
        self.assertIn(t1, s)
        self.assertNotIn(t2, s)
