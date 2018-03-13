from indexed_grammar import IndexedGrammar
from consommation_rule import ConsommationRule
from end_rule import EndRule
from rules import Rules
from regex_tree import RegexTree
from node import Node
from production_rule import ProductionRule


class FunctionIndexedGrammar(IndexedGrammar):
    """FunctionIndexedGrammar
    Represents a grammar generated from functions as presented in our paper
    """

    def __init__(self, functions, query, optim=7, empty=False, eq_rules=[]):
        """__init__
        Initializes the indexed grammar from a set of functions
        :param functions: a list of Functions
        :param query: the query (one terminal for now)
        :param all_relations: all terminals used (with - also)
        """
        # Initial rules
        initial_rules = []
        self.init_counter = -1
        initial_rules.append(ProductionRule("S",
                                            "Cinitquery",
                                            "end"))
        initial_rules.append(ProductionRule("Cinitquery",
                                            "C",
                                            "query"))
        for j in range(len(query)):
            self.init_counter += 1
            initial_rules.append(ConsommationRule(
                "query",
                "C",
                "Cinit" + str(self.init_counter)))
            for i in range(len(query[j]) - 1):
                initial_rules.append(ProductionRule(
                    "Cinit" + str(self.init_counter),
                    "Cinit" + str(self.init_counter + 1),
                    query[j][len(query[j]) - i - 1]))
                self.init_counter += 1
            initial_rules.append(ProductionRule(
                "Cinit" + str(self.init_counter),
                "C",
                query[j][0]))
        initial_rules.append(ConsommationRule("end", "C", "T"))
        initial_rules.append(EndRule("T", "epsilon"))
        # Rules from functions
        f_rules = []
        if len(eq_rules) != 0:
            new_function = "|".join(["(" +
                                     ",".join(function.to_list()) +
                                     ")" for function in functions])
            regex_function = RegexTree(Node(new_function))
            fsm = regex_function.to_fsm()
            fsm.close()
            was_modified = True
            while was_modified:
                was_modified = False
                for eq_rule in eq_rules:
                    was_modified |= fsm.apply_rule(eq_rule.l0,
                                                   eq_rule.l1)
            fsm.open()
            functions = [fsm.to_regex()]
        counter = 0
        self.functions = functions
        for f in functions:
            temp_rule = f.generate_reduced_rules(counter, empty)
            counter = temp_rule[1]
            f_rules += temp_rule[0]
        rules = Rules(f_rules + initial_rules, optim=optim)
        self.query = query
        super(FunctionIndexedGrammar, self).__init__(rules)

    def update(self, new_query):
        """update
        Updates the rules and the cache for a new query. This way, the emptyness
        function will be faster because it is using previous data.
        :param new_query: The new query to consider
        """
        # Only Cinits are affected
        temp_counter = -1
        for j in range(len(self.query)):
            temp_counter += 1
            self.rules.remove_consommation("query", "C",
                                           "Cinit" + str(temp_counter))
            for i in range(len(self.query[j]) - 1):
                self.rules.remove_production("Cinit" + str(temp_counter),
                                             "Cinit" + str(temp_counter + 1),
                                             self.query[j][
                                                 len(self.query[j]) - i - 1])
                temp_counter += 1
            self.rules.remove_production("Cinit" + str(temp_counter),
                                         "C",
                                         self.query[j][0])

        # Reinitialize the marked symboles for S and Cinit
        temp_counter = -1
        self.marked["Cinitquery"] = set()
        self.marked["Cinitquery"].add(frozenset({"Cinitquery"}))
        for i in range(self.init_counter + 1):
            self.marked["Cinit" + str(i)] = set()
            self.marked["Cinit" + str(i)].add(
                        frozenset({"Cinit" + str(i)}))
        self.marked["S"] = set()
        self.marked["S"].add(frozenset({"S"}))

        # Add new rules
        self.init_counter = -1
        for j in range(len(new_query)):
            self.init_counter += 1
            self.rules.add_consommation("query", "C",
                                        "Cinit" + str(self.init_counter))
            for i in range(len(new_query[j]) - 1):
                self.rules.add_production(
                    "Cinit" + str(self.init_counter),
                    "Cinit" + str(self.init_counter + 1),
                    new_query[j][len(new_query[j]) - 1 - i])
                self.init_counter += 1
            self.rules.add_production(
                "Cinit" + str(self.init_counter),
                "C",
                new_query[j][0])

        # Init rules
        for i in range(self.init_counter + 1):
            self.marked["Cinit" + str(i)] = set()
            self.marked["Cinit" + str(i)].add(
                        frozenset({"Cinit" + str(i)}))
        self.query = new_query

    def is_empty(self, debug=False):
        """is_empty Whether the grammar is empty or not"""
        # Here we have an optimization: if the query is not among the terminals,
        # it is not possible the reach it
        if any([any([y not in self.rules.getTerminals() for y in x])
                for x in self.query]) and ["end"] not in self.query:
            return True
        else:
            return super(FunctionIndexedGrammar, self).is_empty(debug)

    def get_prolog_rules(self, max_depth):
        """get_prolog_rules
        Gives the prolog rules. Be Careful, it does not work for everything
        :param max_depth: The maximum depth in the search.
        """
        # CAREFUL DO NOT WORK WITH MULTIPLE INPUT FUNCTION
        # AND WITH QUERY WITH MORE THAN ONE RELATION
        # Stop rules
        res = "p([], _, []).\n"
        res += "p(_, Counter, _) :- Counter =< 0, !, fail.\n"
        for f in self.functions:
            res += "\n".join(f.generate_middle_rules()) + "\n"
        # Initialization rules
        res += "q(X) :- p([" + self.query[0][0] + "], X, L), print(L).\n"
        res += "q(X) :- X < " + str(max_depth) + ", q(X + 1).\n"
        res += "q(_).\n"
        # To start automatically the program in prolog
        res += ":- initialization main.\n"
        res += "main :- q(1), halt(0).\n"
        return res

    def get_n_rules(self):
        """get_n_rules Get the number of rules"""
        return self.rules.get_length()
