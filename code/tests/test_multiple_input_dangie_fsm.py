"""
Testing of linear function, Multiple input self.functions, and equivalence rules
"""

import unittest

from experiments.utils import make_dangie
from experiments.multiple_input_function import MultipleInputFunction

class TestMultipleInputDangieFSM(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMultipleInputDangieFSM, self).__init__(*args, **kwargs)

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
        self.functions.append(["b", "a", "q"])  # 21
        self.functions.append(["a-", "c", "d"])  # 22
        self.functions.append(["d-", "c-", "b-"])  # 23
        self.functions.append(["b-", "a-"])  # 24
        self.functions.append(["a-"])  # 25
        self.functions.append(["c-", "b-", "a-"])  # 26
        self.functions.append(["b-", "a-", "q"])  # 27

        self.mifunctions = []

        self.mifunctions.append(["d-", "c-", "b-"])  # 0
        self.mifunctions.append(["a-", "c", "d"])  # 1

        counter = 0

        for i in range(len(self.functions)):
            self.functions[i] = MultipleInputFunction(self.functions[i], "f" + str(i), 1)

        self.functions.append(MultipleInputFunction(["a-", "c", "d"], "f28", 1,
                                                    outputs=[1,2])) # 28
        self.functions.append(MultipleInputFunction(["c-", "b-", "a-"], "f29",
                                                    1, outputs=[0,2])) # 29

        for i in range(len(self.mifunctions)):
            self.mifunctions[i] = MultipleInputFunction(self.mifunctions[i],
                                                   "f" + str(i + len(self.functions)), 2)

        self.mifunctions.append(MultipleInputFunction(["a", "b", "c"], "f",
                                                 [1]))  # 2
        self.mifunctions.append(MultipleInputFunction(["a", "b", "c", "d"], "f",
                                                 [1, 2]))  # 3
        self.mifunctions.append(MultipleInputFunction(["a-"], "f",
                                                 2))  # 4
        self.mifunctions.append(MultipleInputFunction(["a", "b"], "f",
                                                 2))  # 5


    def test_mif_1(self):

        res = make_dangie([self.functions[x] for x in [8]], ["b"])
        self.assertFalse(res)

    def test_mif_2(self):

        res = make_dangie([self.functions[x] for x in [9, 5]], ["b"])
        self.assertFalse(res)

    def test_mif_3(self):

        res = make_dangie([self.functions[x] for x in [0, 1]], ["b"])
        self.assertFalse(res)


    def test_mif_4(self):

        res = make_dangie([self.functions[x] for x in [0]], ["b"])
        self.assertTrue(res)


    def test_mif_5(self):

        res = make_dangie([self.functions[x] for x in [1]], ["b"])
        self.assertTrue(res)


    def test_mif_6(self):

        res = make_dangie([self.functions[x] for x in [2, 7]], ["b"])
        self.assertFalse(res)


    def test_mif_7(self):

        res = make_dangie([self.functions[x] for x in [9, 10, 7]], ["b"])
        self.assertFalse(res)


    def test_mif_8(self):

        res = make_dangie([self.functions[x] for x in [6, 11]], ["b"])
        self.assertFalse(res)


    def test_mif_9(self):

        res = make_dangie([self.functions[x] for x in [2, 6, 5]], ["b"])
        self.assertFalse(res)


    def test_mif_10(self):

        res = make_dangie([self.functions[x] for x in [2, 3, 4, 5]],
                                           ["b"])
        self.assertFalse(res)

    def test_mif_14(self):

        res = make_dangie([self.functions[x] for x in [12, 13]],
                                           ["xm"])
        # Empty without subfunctions
        self.assertTrue(res)


    def test_mif_15(self):

        res = make_dangie([self.functions[x] for x in [14, 15]],
                                           ["q"])

        self.assertTrue(res)


    def test_mif_16(self):

        res = make_dangie([self.functions[x] for x in [16, 17, 18, 19]],
                                           ["a"])
        self.assertFalse(res)


    def test_mif_17(self):

        res = make_dangie([self.functions[x] for x in [0, 19]],
                                           ["b", "a"])
        self.assertFalse(res)

    def test_mif_20(self):

        res = make_dangie([self.functions[x] for x in [21, 22]] +
                                           [self.mifunctions[x] for x in [0]],
                                           ["q"])
        self.assertTrue(res)

    def test_mif_21(self):

        res = make_dangie([self.functions[x] for x in [21, 28]] +
                                           [self.mifunctions[x] for x in [0]],
                                           ["q"])
        self.assertFalse(res)


    def test_mif_22(self):

        res = make_dangie([self.functions[x] for x in [21, 23]] +
                                           [self.mifunctions[x] for x in [1]],
                                           ["q"])
        self.assertTrue(res)


    def test_mif_23(self):

        res = make_dangie([self.functions[x] for x in [24]] +
                                           [self.mifunctions[x] for x in [2]],
                                           ["c"])
        self.assertFalse(res)


    def test_mif_24(self):

        res = make_dangie([self.functions[x] for x in [25]] +
                                           [self.mifunctions[x] for x in [2]],
                                           ["b", "c"])
        self.assertTrue(res)


    def test_mif_25(self):

        res = make_dangie([self.functions[x] for x in [26]] +
                                           [self.mifunctions[x] for x in [3]],
                                           ["d"])
        self.assertTrue(res)

    def test_mif_18(self):

        res = make_dangie([self.functions[x] for x in [29]] +
                                           [self.mifunctions[x] for x in [3]],
                                           ["d"])
        self.assertFalse(res)



    def test_mif_26(self):

        res = make_dangie([self.functions[x] for x in [24]] +
                                           [self.mifunctions[x] for x in [3]],
                                           ["c", "d"])
        self.assertTrue(res)


    def test_mif_27(self):
      res = make_dangie([self.functions[x] for x in [9, 27]] +
                                         [self.mifunctions[x] for x in [4, 5]],
                                         ["q"])
      self.assertFalse(res)


if __name__ == "__main__":
        unittest.main()
