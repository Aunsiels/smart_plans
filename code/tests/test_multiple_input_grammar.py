"""
Testing of linear function, Multiple input self.functions, and equivalence rules
"""

import unittest

from experiments.function_indexed_grammar import FunctionIndexedGrammar
from experiments.multiple_input_function import MultipleInputFunction

class TestMultipleInputGrammar(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMultipleInputGrammar, self).__init__(*args, **kwargs)

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

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [8]], [["b"]])
        self.assertFalse(i_grammar.is_empty())

    def test_mif_2(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [9, 5]], [["b"]])
        self.assertFalse(i_grammar.is_empty())

    def test_mif_3(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [0, 1]], [["b"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_4(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [0]], [["b"]])
        self.assertTrue(i_grammar.is_empty())


    def test_mif_5(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [1]], [["b"]])
        self.assertTrue(i_grammar.is_empty())


    def test_mif_6(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [2, 7]], [["b"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_7(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [9, 10, 7]], [["b"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_8(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [6, 11]], [["b"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_9(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [2, 6, 5]], [["b"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_10(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [2, 3, 4, 5]],
                                           [["b"]])
        self.assertFalse(i_grammar.is_empty())


        i_grammar.update([["b"]])
        self.assertFalse(i_grammar.is_empty())


        i_grammar.update([["c"]])
        self.assertFalse(i_grammar.is_empty())


        i_grammar.update([["e"]])
        self.assertTrue(i_grammar.is_empty())


    def test_mif_14(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [12, 13]],
                                           [["xm"]])
        # Empty without subfunctions
        self.assertTrue(i_grammar.is_empty())


    def test_mif_15(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [14, 15]],
                                           [["q"]])

        self.assertTrue(i_grammar.is_empty())


    def test_mif_16(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [16, 17, 18, 19]],
                                           [["a"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_17(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [0, 19]],
                                           [["b", "a"]])
        self.assertFalse(i_grammar.is_empty())


        i_grammar.update([["a", "b"]])
        self.assertTrue(i_grammar.is_empty())


    def test_mif_19(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [20]],
                                           [["c"], ["c", "c"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_20(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [20]],
                                           [["c"], ["query", "c"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_21(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [21, 22]] +
                                           [self.mifunctions[x] for x in [0]],
                                           [["q"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_22(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [21, 23]] +
                                           [self.mifunctions[x] for x in [1]],
                                           [["q"]])
        self.assertTrue(i_grammar.is_empty())


    def test_mif_23(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [24]] +
                                           [self.mifunctions[x] for x in [2]],
                                           [["c"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_24(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [25]] +
                                           [self.mifunctions[x] for x in [2]],
                                           [["b", "c"]])
        self.assertTrue(i_grammar.is_empty())


    def test_mif_25(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [26]] +
                                           [self.mifunctions[x] for x in [3]],
                                           [["d"]])
        self.assertFalse(i_grammar.is_empty())


    def test_mif_26(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [24]] +
                                           [self.mifunctions[x] for x in [3]],
                                           [["c", "d"]])
        self.assertTrue(i_grammar.is_empty())


    # def test_mif_27(self):

        #
        # i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [9, 27]] +
        #                                    [self.mifunctions[x] for x in [4, 5]],
        #                                    [["q"]])
        # self.assertFalse(i_grammar.is_empty())
