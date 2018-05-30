from duplication_rule import DuplicationRule
from production_rule import ProductionRule
from end_rule import EndRule
from consommation_rule import ConsommationRule
from indexed_grammar import IndexedGrammar
from rules import Rules

class NFT(object):

    def __init__(self):
        self.Q = set()  # Set of states
        self.T = set()  # Set of input symbols
        self.Sigma = set()  # Set of output symnols
        self.delta = dict()  # Dict from Q x T U {epsilon} into Q X Sigma*
        self.q0 = 0  # Initial state
        self.Q.add(self.q0)
        self.final = 1  # Standard final node
        self.F = set()  # Final states
        self.F.add(self.final)
        self.max_node = 1
        self.delta[(self.final, "epsilon")] = (self.q0, "epsilon")  # Loop

    def get_next_node(self):
        self.max_node += 1
        return self.max_node

    def add_function(self, function):
        current_node = self.q0
        l_function = function.to_list("m")
        for i in range(len(l_function) - 1):
            rel = l_function[i]
            if (current_node, rel) in self.delta:
                current_node = self.delta[current_node][0]
            else:
                next_node = self.get_next_node()
                self.Q.add(next_node)
                self.Sigma.add(rel)
                self.T.add(rel)
                self.delta[(current_node, rel)] = (next_node, rel)
                current_node = next_node
        rel = l_function[-1]
        if (current_node, rel) in self.delta:
            current_node = self.delta[current_node][0]
            if (current_node, "epsilon") not in self.delta:
                self.delta[(current_node, "epsilon")] = (self.final, "")
        else:
            next_node = self.final
            self.Q.add(next_node)
            self.Sigma.add(rel)
            self.T.add(rel)
            self.delta[(current_node, rel)] = (next_node, rel)

    def intersect_indexed_grammar(self, indexed_grammar):
        rules = indexed_grammar.rules
        new_rules = []
        terminals = rules.getTerminals()
        new_rules.append(EndRule("T", "epsilon"))
        consommations = rules.getConsommationRules()
        for f in consommations:
            for consommation in consommations[f]:
                for r in self.Q:
                    for s in self.Q:
                        new_rules.append(ConsommationRule(
                            consommation.getF(),
                            str((r, consommation.getLeftTerm(), s)),
                            str((r, consommation.getRight(), s))))
        for rule in rules.getRules():
            if rule.isDuplication():
                for p in self.Q:
                    for q in self.Q:
                        for r in self.Q:
                            new_rules.append(DuplicationRule(
                                str((p, rule.getLeftTerm(), q)),
                                str((p, rule.getRightTerms()[0], r)),
                                str((r, rule.getRightTerms()[1], q))))
            elif rule.isProduction():
                for p in self.Q:
                    for q in self.Q:
                        new_rules.append(ProductionRule(
                            str((p, rule.getLeftTerm(), q)),
                            str((p, rule.getRightTerm(), q)),
                            str(rule.getProduction())))
            elif rule.isEndRule():
                for p in self.Q:
                    for q in self.Q:
                        new_rules.append(DuplicationRule(
                            str((p, rule.getLeftTerm(), q)),
                            str((p, rule.getRightTerm(), q)),
                            "T"))
        for a in terminals:
            for p in self.Q:
                for q in self.Q:
                    for r in self.Q:
                        new_rules.append(DuplicationRule(
                            str((p, a, q)),
                            str((p, "epsilon", r)),
                            str((r, a, q))))
                        new_rules.append(DuplicationRule(
                            str((p, a, q)),
                            str((p, a, r)),
                            str((r, "epsilon", q))))
        for p in self.Q:
            for q in self.Q:
                for r in self.Q:
                    new_rules.append(DuplicationRule(
                        str((p, "epsilon", q)),
                        str((p, "epsilon", r)),
                        str((r, "epsilon", q))))
        for key in self.delta:
            p = key[0]
            a = key[1]
            q = self.delta[key][0]
            x = self.delta[key][1]
            new_rules.append(EndRule(
                str((p, a, q)),
                x))
        for p in self.Q:
            new_rules.append(EndRule(
                str((p, "epsilon", p)),
                "epsilon"))
        for p in self.F:
            new_rules.append(DuplicationRule(
                "S",
                str((self.q0, "S", p)),
                "T"))
        rules = Rules(new_rules)
        return IndexedGrammar(rules)
