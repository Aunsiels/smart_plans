import networkx as nx


class RuleOrdering(object):

    def __init__(self, rules, conso_rules):
        self.rules = rules
        self.conso_rules = conso_rules

    def reverse(self):
        return self.rules[::1]

    def order_by_core(self, reverse=False):
        # Graph construction
        DG = nx.DiGraph()
        for rule in self.rules:
            if rule.isDuplication():
                if rule.getRightTerms()[0] != rule.getLeftTerm():
                    DG.add_edge(rule.getRightTerms()[0], rule.getLeftTerm())
                if rule.getRightTerms()[1] != rule.getLeftTerm():
                    DG.add_edge(rule.getRightTerms()[1], rule.getLeftTerm())
            if rule.isProduction():
                f_rules = self.conso_rules.setdefault(
                    rule.getProduction(), [])
                for f_rule in f_rules:
                    if f_rule.getRight() != rule.getLeftTerm():
                        DG.add_edge(f_rule.getRight(), rule.getLeftTerm())
        # Get core number, careful the degree is in + out
        core_numbers = nx.core_number(DG)
        new_order = sorted(self.rules,
                           key=lambda x: core_numbers.setdefault(
                               x.getLeftTerm(), 0))
        if reverse:
            new_order.reverse()
        return new_order
