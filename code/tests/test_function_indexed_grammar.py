"""
Testing of single input linear function, tree self.functions and equivalence rules
"""

import unittest

from experiments.function_indexed_grammar import FunctionIndexedGrammar
from experiments.function import Function
from experiments.horn_rule import HornRule
from experiments.tree_function import TreeFunction


class TestFunctionIndexedGrammar(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestFunctionIndexedGrammar, self).__init__(*args, **kwargs)

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


        self.tree_functions = []
        self.tree_functions.append(TreeFunction("(a;b)c"))  # 0
        self.tree_functions.append(TreeFunction("(a;b)c,d"))  # 1
        self.tree_functions.append(TreeFunction("(a;b)c-"))  # 2
        self.tree_functions.append(TreeFunction("c"))  # 3
        self.tree_functions.append(TreeFunction("d"))  # 4
        self.tree_functions.append(TreeFunction("d-, b-, e-"))  # 5
        self.tree_functions.append(TreeFunction("e, c-"))  # 6
        self.tree_functions.append(TreeFunction(Function(["c", "b", "a"]), []))  # 7
        self.tree_functions.append(TreeFunction("((f;g)h;e)b"))  # 8
        self.tree_functions.append(TreeFunction("(((f;g)h;c)a,d;e)b"))  # 9


        self.equivalence_rules = []

        # forbidden
        self.equivalence_rules.append(HornRule(["a", "b"], ["d-", "c-"], "r0"))  # 0
        self.equivalence_rules.append(HornRule(["c"], ["q"], "r1"))  # 1
        # forbidden
        self.equivalence_rules.append(HornRule(["b", "c"], ["c", "b"], "r2"))  # 2
        self.equivalence_rules.append(HornRule(["b", "a"], ["a"], "r3"))  # 3
        self.equivalence_rules.append(HornRule(["c", "c", "c"], ["d"], "r4"))  # 4

        counter = 0

        for i in range(len(self.functions)):
            self.functions[i] = Function(self.functions[i], "f" + str(i))

    def test_fig_0(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [8]], [["b"]])
        self.assertFalse(i_grammar.is_empty())

    def test_fig_1(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [9, 5]], [["b"]])
        self.assertFalse(i_grammar.is_empty())

    def test_fig_2(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [0, 1]], [["b"]])
        self.assertFalse(i_grammar.is_empty())

    def test_fig_3(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [0]], [["b"]])
        self.assertTrue(i_grammar.is_empty())

    def test_fig_4(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [1]], [["b"]])
        self.assertTrue(i_grammar.is_empty())

    def test_fig_5(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [2, 7]], [["b"]])
        self.assertFalse(i_grammar.is_empty())

    def test_fig_6(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [9, 10, 7]], [["b"]])
        self.assertFalse(i_grammar.is_empty())

    def test_fig_7(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [6, 11]], [["b"]])
        self.assertFalse(i_grammar.is_empty())

    def test_fig_8(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [2, 6, 5]], [["b"]])
        self.assertFalse(i_grammar.is_empty())

    def test_fig_9(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [2, 3, 4, 5]],
                                           [["b"]])
        self.assertFalse(i_grammar.is_empty())


        i_grammar.update([["b"]])
        self.assertFalse(i_grammar.is_empty())


        i_grammar.update([["c"]])
        self.assertFalse(i_grammar.is_empty())


        i_grammar.update([["e"]])
        self.assertTrue(i_grammar.is_empty())

    def test_fig_13(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [12, 13]],
                                           [["xm"]])
        # empty without subfunctions
        self.assertTrue(i_grammar.is_empty())

        # print("Test 13")
        #
        # i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [14, 15]],
        #                                    [["q"]],
        #                                    eq_rules=[self.equivalence_rules[x]
        #                                            for x in [0]])
        #
        # self.assertFalse(i_grammar.is_empty())

    def test_fig_14(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [14, 15]],
                                           [["q"]])

        self.assertTrue(i_grammar.is_empty())

    def test_fig_15(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [16, 17, 18, 19]],
                                           [["a"]])
        self.assertFalse(i_grammar.is_empty())

    def test_fig_16(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [0, 19]],
                                           [["b", "a"]])
        self.assertFalse(i_grammar.is_empty())

        i_grammar.update([["a", "b"]])
        self.assertTrue(i_grammar.is_empty())

    def test_fig_18(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [20]],
                                           [["c"], ["c", "c"]])
        self.assertFalse(i_grammar.is_empty())

    def test_fig_19(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [20]],
                                           [["c"], ["query", "c"]])
        self.assertFalse(i_grammar.is_empty())

    def test_fig_20(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [20]],
                                           [["c", "q"]],
                                           eq_rules=[self.equivalence_rules[x] for x in [1]])

        self.assertFalse(i_grammar.is_empty())

        # print("Test 21")
        #
        # i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [21, 22]],
        #                                    [["a", "c", "b", "d"]],
        #                                    eq_rules=[self.equivalence_rules[x]
        # for x in [2]])
        #
        # self.assertFalse(i_grammar.is_empty())

    def test_fig_21(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [21, 22]],
                                           [["a", "c", "b", "d"]],
                                           eq_rules=[])

        self.assertTrue(i_grammar.is_empty())

        # print("Test 23")
        #
        # i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [23, 24]],
        #                                    [["a", "b", "c", "d"]],
        #                                    eq_rules=[self.equivalence_rules[x]
        # for x in [2]])
        #
        # self.assertFalse(i_grammar.is_empty())

    def test_fig_22(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [0]] +
                                           [self.functions[x] for x in [25, 26]],
                                           [["c"]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_23(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [0]] +
                                           [self.functions[x] for x in [25]],
                                           [["c"]])

        self.assertTrue(i_grammar.is_empty())

    def test_fig_24(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [1]] +
                                           [self.functions[x] for x in [25, 26, 6]],
                                           [["c"]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_25(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [2]] +
                                           [self.functions[x] for x in [25, 26, 6, 27]],
                                           [["q"]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_26(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [0]] +
                                           [self.functions[x] for x in [25, 28]],
                                           [["c"]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_27(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [0]] +
                                           [self.functions[x] for x in [29, 16, 28]],
                                           [["c"]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_28(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [3]],
                                           [["c"]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_29(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [4, 5, 6, 7]],
                                           [["a"]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_30(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [1]] +
                                           [self.functions[x] for x in [30, 31]],
                                           [["d"]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_31(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [0]] +
                                           [self.functions[x] for x in [28]],
                                           [["a", "c"]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_32(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [6]],
                                           [["c-"]])

        self.assertTrue(i_grammar.is_empty())

    def test_fig_33(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [14]],
                                           [["a", "b"]],
                                           eq_rules=[self.equivalence_rules[x] for x in [3]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_34(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [14]],
                                           [["a", "a", "b"]],
                                           eq_rules=[self.equivalence_rules[x] for x in [3]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_35(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [14]],
                                           [["a", "a", "a", "b"]],
                                           eq_rules=[self.equivalence_rules[x] for x in [3]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_36(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [14]],
                                           [["a", "a", "a", "b"]],
                                           eq_rules=[self.equivalence_rules[x] for x in [3]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_37(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [32, 33]],
                                           [["a", "d", "c", "b"]],
                                           eq_rules=[self.equivalence_rules[x] for x in [4]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_38(self):

        i_grammar = FunctionIndexedGrammar([self.functions[x] for x in [32, 33]],
                                           [["a", "c", "d", "b"]],
                                           eq_rules=[self.equivalence_rules[x] for x in [4]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_39(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [8]] +
                                           [self.functions[x] for x in [34, 35, 36]],
                                           [["b"]])

        self.assertFalse(i_grammar.is_empty())

    def test_fig_40(self):

        i_grammar = FunctionIndexedGrammar([self.tree_functions[x] for x in [9]] +
                                           [self.functions[x] for x in [37, 38, 39, 40]],
                                           [["d", "b"]])

        self.assertFalse(i_grammar.is_empty())
