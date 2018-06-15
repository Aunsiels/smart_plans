"""
Testing of single input linear function, tree self.functions and equivalence rules
"""

import unittest

from experiments.function import Function
from experiments.utils import make_dangie
from experiments.horn_rule import HornRule


class TestDangieFSMSingle(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestDangieFSMSingle, self).__init__(*args, **kwargs)

        self.functions = []

        self.functions.append(["c-"])  # 0
        self.functions.append(["c", "c", "b"])  # 1
        self.functions.append(["a", "d"])  # 2
        self.functions.append(["d-", "c-"])  # 3
        self.functions.append(["c"])  # 4
        self.functions.append(["a-", "b"])  # 5
        self.functions.append(["d-"])  # 6
        self.functions.append(["d-", "a-", "b"])  # 7
        self.functions.append(["b"])  # 8
        self.functions.append(["a"])  # 9
        self.functions.append(["d"])  # 10
        self.functions.append(["d", "b"])  # 11
        self.functions.append(["x-", "x-"])  # 12
        self.functions.append(["j", "x"])  # 13
        self.functions.append(["a", "b"])  # 14
        self.functions.append(["c", "d", "q"])  # 15
        self.functions.append(["d"])  # 16
        self.functions.append(["d-", "b-", "e-"])  # 17
        self.functions.append(["e", "c-"])  # 18
        self.functions.append(["c", "b", "a"])  # 19
        self.functions.append(["c", "c"])  # 20
        self.functions.append(["a", "b"])  # 21
        self.functions.append(["c", "d"])  # 22
        self.functions.append(["a", "c"])  # 23
        self.functions.append(["b", "d"])  # 24
        self.functions.append(["a-"])  # 25
        self.functions.append(["b-"])  # 26
        self.functions.append(["d", "c", "q"])  # 27
        self.functions.append(["a", "b-"])  # 28
        self.functions.append(["a-", "d-"])  # 29
        self.functions.append(["c-", "a-"])  # 30
        self.functions.append(["c-", "b-"])  # 31
        self.functions.append(["a", "c", "c"])  # 32
        self.functions.append(["c", "c", "b"])  # 33
        self.functions.append(["h-", "f-"])  # 34
        self.functions.append(["h-", "g-"])  # 35
        self.functions.append(["e-"])  # 36
        self.functions.append(["a-", "c-"])  # 37
        self.functions.append(["d", "e-"])  # 38
        self.functions.append(["a-", "h-", "f-"])  # 39
        self.functions.append(["a-", "h-", "g-"])  # 40

        self.equivalence_rules = []

        # forbidden
        self.equivalence_rules.append(HornRule(["a_OUT", "b_OUT"], ["d_OUTm",
                                                                    "c_OUTm"], "r0"))  # 0
        self.equivalence_rules.append(HornRule(["c_OUT"], ["q_OUT"], "r1"))  # 1
        # forbidden
        self.equivalence_rules.append(HornRule(["b_OUT", "c_OUT"], ["c_OUT",
                                                                    "b_OUT"],
                                               "r2"))  # 2
        self.equivalence_rules.append(HornRule(["b_OUT", "a_OUT"], ["a_OUT"],
                                               "r3"))  # 3
        self.equivalence_rules.append(HornRule(["c_OUT", "c_OUT", "c_OUT"],
                                               ["d_OUT"], "r4"))  # 4

        counter = 0

        for i in range(len(self.functions)):
            self.functions[i] = Function(self.functions[i], "f" + str(i))

    def test_fig_0(self):

        self.assertFalse(make_dangie([self.functions[x] for x in [8]], ["b"]))

    def test_fig_1(self):

        res = make_dangie([self.functions[x] for x in [9, 5]], ["b"])
        self.assertFalse(res)

    def test_fig_2(self):

        res = make_dangie([self.functions[x] for x in [0, 1]], ["b"])
        self.assertFalse(res)

    def test_fig_3(self):

        res = make_dangie([self.functions[x] for x in [0]], ["b"])
        self.assertTrue(res)

    def test_fig_4(self):

        res = make_dangie([self.functions[x] for x in [1]], ["b"])
        self.assertTrue(res)

    def test_fig_5(self):

        res = make_dangie([self.functions[x] for x in [2, 7]], ["b"])
        self.assertFalse(res)

    def test_fig_6(self):

        res = make_dangie([self.functions[x] for x in [9, 10, 7]], ["b"])
        self.assertFalse(res)

    def test_fig_7(self):

        res = make_dangie([self.functions[x] for x in [6, 11]], ["b"])
        self.assertFalse(res)

    def test_fig_8(self):

        res = make_dangie([self.functions[x] for x in [2, 6, 5]], ["b"])
        self.assertFalse(res)

    def test_fig_9(self):

        res = make_dangie([self.functions[x] for x in [2, 3, 4, 5]],
                                           ["b"])
        self.assertFalse(res)

    def test_fig_13(self):

        res = make_dangie([self.functions[x] for x in [12, 13]],
                                           ["xm"])
        # empty without subfunctions
        self.assertTrue(res)

    def test_fig_14(self):

        res = make_dangie([self.functions[x] for x in [14, 15]],
                                           ["q"])

        self.assertTrue(res)

    def test_fig_15(self):

        res = make_dangie([self.functions[x] for x in [16, 17, 18, 19]],
                                           ["a"])
        self.assertFalse(res)

    def test_fig_16(self):

        res = make_dangie([self.functions[x] for x in [0, 19]],
                                           ["b", "a"])
        self.assertFalse(res)

    def test_fig_20(self):

        res = make_dangie([self.functions[x] for x in [20]],
                                           ["c", "q"],
                                           eq_rules=[self.equivalence_rules[x] for x in [1]])

        self.assertFalse(res)

    def test_fig_21(self):

        res = make_dangie([self.functions[x] for x in [21, 22]],
                                           ["a", "c", "b", "d"],
                                           eq_rules=[])

        self.assertTrue(res)

    def test_fig_33(self):

        res = make_dangie([self.functions[x] for x in [14]],
                                           ["a", "b"],
                                           eq_rules=[self.equivalence_rules[x] for x in [3]])

        self.assertFalse(res)

    def test_fig_34(self):

        res = make_dangie([self.functions[x] for x in [14]],
                                           ["a", "a", "b"],
                                           eq_rules=[self.equivalence_rules[x] for x in [3]])

        self.assertFalse(res)

    def test_fig_35(self):

        res = make_dangie([self.functions[x] for x in [14]],
                                           ["a", "a", "a", "b"],
                                           eq_rules=[self.equivalence_rules[x] for x in [3]])

        self.assertFalse(res)

    def test_fig_36(self):

        res = make_dangie([self.functions[x] for x in [14]],
                                           ["a", "a", "a", "b"],
                                           eq_rules=[self.equivalence_rules[x] for x in [3]])

        self.assertFalse(res)

    def test_fig_37(self):

        res = make_dangie([self.functions[x] for x in [32, 33]],
                                           ["a", "d", "c", "b"],
                                           eq_rules=[self.equivalence_rules[x] for x in [4]])

        self.assertFalse(res)

    def test_fig_38(self):

        res = make_dangie([self.functions[x] for x in [32, 33]],
                                           ["a", "c", "d", "b"],
                                           eq_rules=[self.equivalence_rules[x] for x in [4]])

        self.assertFalse(res)

