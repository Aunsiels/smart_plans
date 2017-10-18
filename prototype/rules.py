from production_rule import ProductionRule
from consommation_rule import ConsommationRule


class Rules(object):
    """Rules
    Use to store a set of rules
    """

    def getRules(self):
        """getRules Gets the non consumption rules"""
        return self.rules

    def getConsommationRules(self):
        """getConsommationRules Gets the consumption rules"""
        return self.consommationRules

    def getTerminals(self):
        """getTerminals Gets all the terminals used by all the rules"""
        terminals = set()
        for temp_rule in self.consommationRules.values():
            for rule in temp_rule:
                terminals = terminals.union(rule.getTerminals())
        for rule in self.rules:
            terminals = terminals.union(rule.getTerminals())
        return list(terminals)

    def getNonTerminals(self):
        """getNonTerminals Gets all the non-terminals used by all the rules"""
        terminals = set()
        for temp_rule in self.consommationRules.values():
            for rule in temp_rule:
                terminals = terminals.union(rule.getNonTerminals())
        for rule in self.rules:
            terminals = terminals.union(rule.getNonTerminals())
        return list(terminals)

    def remove_production(self, left, right, prod):
        """remove_production
        Remove the production rule:
            left[sigma] -> right[prod sigma]
        :param left: The left non-terminal in the rule
        :param right: The right non-terminal in the rule
        :param prod: The production used in the rule
        """
        self.rules = list(filter(lambda x: not(x.isProduction() and
                                 x.getLeftTerm() == left and
                                 x.getRightTerm() == right and
                                 x.getProduction() == prod), self.rules))

    def add_production(self, left, right, prod):
        """add_production
        Add the production rule:
            left[sigma] -> right[prod sigma]
        :param left: The left non-terminal in the rule
        :param right: The right non-terminal in the rule
        :param prod: The production used in the rule
        """
        self.rules.append(ProductionRule(left, right, prod))

    def remove_consommation(self, prod, left, right):
        """remove_consommation
        Remove the consommation rule:
            left[prod sigma] -> right[sigma]
        :param prod: The production used in the rule
        :param left: The left non-terminal in the rule
        :param right: The right non-terminal in the rule
        """
        self.rules = list(filter(lambda x: not(x.isConsommation() and
                                 x.getLeft == left and
                                 x.getRight == right and
                                 x.getF == prod), self.rules))

    def add_consommation(self, prod, left, right):
        """add_consommation
        Add the consommation rule:
            left[prod sigma] -> right[sigma]
        :param prod: The production used in the rule
        :param left: The left non-terminal in the rule
        :param right: The right non-terminal in the rule
        """
        self.rules.append(ConsommationRule(prod, left, right))

    def __init__(self, rules, optim=True):
        """__init__
        Initializes the rules.
        :param rules: A list of all the rules
        """
        self.rules = []
        self.consommationRules = dict()
        for rule in rules:
            # We separate consumption rule from other
            if rule.isConsommation():
                temp = self.consommationRules.setdefault(rule.getF(), [])
                temp.append(rule)
                self.consommationRules[rule.getF()] = temp
            else:
                self.rules.append(rule)
        if optim:
            self.rules.reverse()  # Nice optimization
