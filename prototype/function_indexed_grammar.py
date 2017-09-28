from indexed_grammar import IndexedGrammar
from consommation_rule import ConsommationRule
from end_rule import EndRule
from rules import Rules
from production_rule import ProductionRule


class FunctionIndexedGrammar(IndexedGrammar):
    """FunctionIndexedGrammar
    Represents a grammar generated from functions as presented in our paper
    """

    def __init__(self, functions, query):
        """__init__
        Initializes the indexed grammar from a set of functions
        :param functions: a list of Functions
        :param query: the query (one terminal for now)
        :param all_relations: all terminals used (with - also)
        """
        # Initial rules
        initial_rules = []
        initial_rules.append(ProductionRule("S", "Cinit", "end"))
        # TODO query with multiple symboles
        initial_rules.append(ProductionRule("Cinit", "C", query))
        initial_rules.append(ConsommationRule("end", "C", "T"))
        initial_rules.append(EndRule("T", "epsilon"))
        # Rules from functions
        f_rules = []
        # Generate the rules
        counter = 0
        self.functions = functions
        for f in functions:
            temp_rule = f.generate_reduced_rules(counter)
            counter = temp_rule[1]
            f_rules += temp_rule[0]
        rules = Rules(f_rules + initial_rules)
        self.query = query
        super(FunctionIndexedGrammar, self).__init__(rules)

    def update(self, new_query):
        """update
        Updates the rules and the cache for a new query. This way, the emptyness
        function will be faster because it is using previous data.
        :param new_query: The new query to consider
        """
        # Only Cinit is affected
        self.rules.remove_production("Cinit", "C", self.query)
        self.rules.add_production("Cinit", "C", new_query)
        self.query = new_query
        # Reinitialize the marked symboles for S and Cinit
        self.marked["Cinit"] = []
        self.marked["Cinit"].append({"Cinit"})
        self.marked["S"] = []
        self.marked["S"].append({"S"})
