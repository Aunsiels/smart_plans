import networkx as nx
from queue import Queue
import random


class RuleOrdering(object):

    def __init__(self, rules, conso_rules):
        self.rules = rules
        self.conso_rules = conso_rules

    def reverse(self):
        return self.rules[::1]

    def get_graph(self):
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
        return DG

    def order_by_core(self, reverse=False):
        # Graph construction
        DG = self.get_graph()
        # Get core number, careful the degree is in + out
        core_numbers = nx.core_number(DG)
        new_order = sorted(self.rules,
                           key=lambda x: core_numbers.setdefault(
                               x.getLeftTerm(), 0))
        if reverse:
            new_order.reverse()
        return new_order

    def order_by_arborescence(self, reverse=True):
        DG = self.get_graph()
        # arborescence = nx.minimum_spanning_arborescence(DG)
        arborescence = nx.minimum_spanning_tree(DG.to_undirected())
        to_process = Queue()
        processed = set()
        res = dict()
        res["S"] = 0
        for x in arborescence["S"]:
            if x not in processed:
                res[x] = 1
                processed.add(x)
                to_process.put(x)
        while not to_process.empty():
            p = to_process.get()
            for x in arborescence[p]:
                if x not in processed:
                    res[x] = res[p] + 1
                    processed.add(x)
                    to_process.put(x)
        new_order = sorted(self.rules,
                           key=lambda x: res.setdefault(
                               x.getLeftTerm(), 0))
        if reverse:
            new_order.reverse()
        return new_order

    def get_len_out(self, DG, x):
        if x.getLeftTerm() in DG:
            return len(DG[x.getLeftTerm()])
        else:
            return 0

    def order_by_edges(self, reverse=False):
        DG = self.get_graph()
        new_order = sorted(self.rules, key=lambda x:
                           self.get_len_out(DG, x))
        if reverse:
            new_order.reverse()
        return new_order

    def order_random(self):
        random.shuffle(self.rules)
        return self.rules
