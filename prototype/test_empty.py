from rules import Rules
from consommation_rule import ConsommationRule
from end_rule import EndRule
from production_rule import ProductionRule
from duplication_rule import DuplicationRule
from indexed_grammar import IndexedGrammar

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
assert(not i_grammar.is_empty())

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
assert(not i_grammar.is_empty())

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
assert(i_grammar.is_empty())

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
assert(i_grammar.is_empty())

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
assert(i_grammar.is_empty())
