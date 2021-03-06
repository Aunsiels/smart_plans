"""
Testing of indexed grammar, with manual rules
"""

import unittest

from experiments.rules import Rules
from experiments.consommation_rule import ConsommationRule
from experiments.end_rule import EndRule
from experiments.production_rule import ProductionRule
from experiments.duplication_rule import DuplicationRule
from experiments.indexed_grammar import IndexedGrammar
from experiments.function import Function
from experiments.nft import NFT


class TestIndexedGrammar(unittest.TestCase):


    def test_simple_ig_0(self):

        # Write rules

        l_rules = []

        # Initialization rules

        l_rules.append(ProductionRule("S", "Cinit", "end"))
        l_rules.append(ProductionRule("Cinit", "C", "b"))
        l_rules.append(ConsommationRule("end", "C", "T"))
        l_rules.append(EndRule("T", "epsilon"))

        # C[cm sigma] -> cm C[sigma]

        l_rules.append(ConsommationRule("b", "C", "B0"))
        l_rules.append(DuplicationRule("B0", "A0", "C"))
        l_rules.append(EndRule("A0", "b"))

        rules = Rules(l_rules)
        i_grammar = IndexedGrammar(rules)
        self.assertFalse(i_grammar.is_empty())

        i_grammar_init = i_grammar

        # Create NFT
        nft = NFT()
        # Add functions
        nft.add_function(Function(["b"]))
        # Generate Grammar
        i_grammar = nft.intersect_indexed_grammar(i_grammar)
        self.assertFalse(i_grammar.is_empty())

        i_grammar = i_grammar_init

        nft = NFT()
        nft.add_function(Function(["c"]))
        i_grammar = nft.intersect_indexed_grammar(i_grammar)
        self.assertTrue(i_grammar.is_empty())

    def test_simple_ig_1(self):

        # Write rules

        l_rules = []

        # Initialization rules

        l_rules.append(ProductionRule("S", "Cinit", "end"))
        l_rules.append(ProductionRule("Cinit", "C", "b"))
        l_rules.append(ConsommationRule("end", "C", "T"))
        l_rules.append(EndRule("T", "epsilon"))

        # C[cm sigma] -> cm C[sigma]

        l_rules.append(ConsommationRule("cm", "C", "B0"))
        l_rules.append(DuplicationRule("B0", "A0", "C"))
        l_rules.append(EndRule("A0", "cm"))

        # C[b sigma] -> C[cm sigma] c b C[sigma]

        l_rules.append(ConsommationRule("b", "C", "B"))
        l_rules.append(DuplicationRule("B", "A1", "D"))
        l_rules.append(ConsommationRule("b", "A1", "A1"))
        l_rules.append(ConsommationRule("bm", "A1", "A1"))
        l_rules.append(ConsommationRule("c", "A1", "A1"))
        l_rules.append(ConsommationRule("cm", "A1", "A1"))
        l_rules.append(ConsommationRule("end", "A1", "Abackm2"))
        l_rules.append(ProductionRule("Abackm2", "Abackm1", "end"))
        l_rules.append(ProductionRule("Abackm1", "C", "cm"))
        l_rules.append(DuplicationRule("D", "E0", "C"))
        l_rules.append(DuplicationRule("E0", "F0", "E1"))
        l_rules.append(DuplicationRule("E1", "F1", "E2"))
        l_rules.append(EndRule("E2", "epsilon"))
        l_rules.append(EndRule("F0", "c"))
        l_rules.append(EndRule("F1", "b"))

        rules = Rules(l_rules)
        i_grammar = IndexedGrammar(rules)
        self.assertFalse(i_grammar.is_empty())

    def test_simple_ig_2(self):

        # Write rules

        l_rules = []

        # Initialization rules

        l_rules.append(ProductionRule("S", "Cinit", "end"))
        l_rules.append(ProductionRule("Cinit", "C", "b"))
        l_rules.append(ConsommationRule("end", "C", "T"))
        l_rules.append(EndRule("T", "epsilon"))

        # C[b sigma] -> C[cm sigma] c b C[sigma]

        l_rules.append(ConsommationRule("b", "C", "B"))
        l_rules.append(DuplicationRule("B", "A1", "D"))
        l_rules.append(ConsommationRule("b", "A1", "A1"))
        l_rules.append(ConsommationRule("bm", "A1", "A1"))
        l_rules.append(ConsommationRule("c", "A1", "A1"))
        l_rules.append(ConsommationRule("cm", "A1", "A1"))
        l_rules.append(ConsommationRule("end", "A1", "Abackm2"))
        l_rules.append(ProductionRule("Abackm2", "Abackm1", "end"))
        l_rules.append(ProductionRule("Abackm1", "C", "cm"))
        l_rules.append(DuplicationRule("D", "E0", "C"))
        l_rules.append(DuplicationRule("E0", "F0", "E1"))
        l_rules.append(DuplicationRule("E1", "F1", "E2"))
        l_rules.append(EndRule("E2", "epsilon"))
        l_rules.append(EndRule("F0", "c"))
        l_rules.append(EndRule("F1", "b"))

        rules = Rules(l_rules)
        i_grammar = IndexedGrammar(rules)
        self.assertTrue(i_grammar.is_empty())

    def test_simple_ig_3(self):

        # Write rules

        l_rules = []

        # Initialization rules

        l_rules.append(ProductionRule("S", "Cinit", "end"))
        l_rules.append(ProductionRule("Cinit", "C", "b"))
        l_rules.append(ConsommationRule("end", "C", "T"))
        l_rules.append(EndRule("T", "epsilon"))

        # C[cm sigma] -> cm C[sigma]

        l_rules.append(ConsommationRule("cm", "C", "B0"))
        l_rules.append(DuplicationRule("B0", "A0", "C"))
        l_rules.append(EndRule("A0", "cm"))

        rules = Rules(l_rules)
        i_grammar = IndexedGrammar(rules)
        self.assertTrue(i_grammar.is_empty())

    def test_simple_ig_4(self):

        # Write rules

        l_rules = []

        # Initialization rules

        l_rules.append(ProductionRule("S", "Cinit", "end"))
        l_rules.append(ConsommationRule("end", "C", "T"))
        l_rules.append(EndRule("T", "epsilon"))

        # C[cm sigma] -> cm C[sigma]

        l_rules.append(ConsommationRule("cm", "C", "B0"))
        l_rules.append(DuplicationRule("B0", "A0", "C"))
        l_rules.append(EndRule("A0", "cm"))

        # C[b sigma] -> C[cm sigma] c b C[sigma]

        l_rules.append(ConsommationRule("b", "C", "B"))
        l_rules.append(DuplicationRule("B", "A1", "D"))
        l_rules.append(ConsommationRule("b", "A1", "A1"))
        l_rules.append(ConsommationRule("bm", "A1", "A1"))
        l_rules.append(ConsommationRule("c", "A1", "A1"))
        l_rules.append(ConsommationRule("cm", "A1", "A1"))
        l_rules.append(ConsommationRule("end", "A1", "Abackm2"))
        l_rules.append(ProductionRule("Abackm2", "Abackm1", "end"))
        l_rules.append(ProductionRule("Abackm1", "C", "cm"))
        l_rules.append(DuplicationRule("D", "E0", "C"))
        l_rules.append(DuplicationRule("E0", "F0", "E1"))
        l_rules.append(DuplicationRule("E1", "F1", "E2"))
        l_rules.append(EndRule("E2", "epsilon"))
        l_rules.append(EndRule("F0", "c"))
        l_rules.append(EndRule("F1", "b"))

        rules = Rules(l_rules)
        i_grammar = IndexedGrammar(rules)
        self.assertTrue(i_grammar.is_empty())

    def test_simple_ig_5(self):

        # Write rules

        l_rules = []

        # Initialization rules

        l_rules.append(ProductionRule("S", "A", "f"))
        l_rules.append(ConsommationRule("f", "A", "B"))
        l_rules.append(ConsommationRule("f", "C", "F"))
        l_rules.append(ProductionRule("B", "C", "f"))
        l_rules.append(ProductionRule("D", "E", "f"))
        l_rules.append(EndRule("F", "epsilon"))
        l_rules.append(DuplicationRule("B0", "A0", "C"))

        rules = Rules(l_rules)
        i_grammar = IndexedGrammar(rules)
        self.assertFalse(i_grammar.is_empty())

    def test_simple_ig_regular_expression(self):

        # Test for regular expression functions

        l_rules = []
        l_rules.append(ProductionRule("S", "Ci", "end"))
        l_rules.append(ProductionRule("Ci", "C", "q"))
        l_rules.append(ConsommationRule("q", "C", "C0"))
        l_rules.append(ProductionRule("C0", "C0", "a-"))
        l_rules.append(DuplicationRule("C0", "T", "C"))
        l_rules.append(EndRule("T", "epsilon"))
        l_rules.append(ConsommationRule("end", "C", "Cend"))
        l_rules.append(EndRule("Cend", "epsilon"))
        l_rules.append(ConsommationRule("a-", "C", "C1"))
        l_rules.append(ConsommationRule("a-", "C1", "C2"))
        l_rules.append(ConsommationRule("a-", "C2", "C3"))
        l_rules.append(ConsommationRule("a-", "C3", "C4"))
        l_rules.append(ConsommationRule("a-", "C4", "C"))

        rules = Rules(l_rules)
        i_grammar = IndexedGrammar(rules)
        self.assertFalse(i_grammar.is_empty())
