import random
import string
import math
from function import Function


class FunctionGenerator(object):
    """FunctionGenerator
    This class generates random functions from random relations
    """

    def __init__(self, n_relations):
        """__init__
        Initialises the class by creating random relations
        :param n_relations: The number of random relations to create
        """
        # m is used for minus
        # not exactly n_relations different relations
        self.relations = [''.join([random.choice(
            string.ascii_lowercase.replace("m", ""))
                             for _ in range(int(math.log(n_relations, 20) +
                                                1))])
                     for _ in range(n_relations)]
        while len(self.relations) != n_relations:
            self.relations.append(''.join([random.choice(
                string.ascii_lowercase.replace("m", ""))
                             for _ in range(int(math.log(n_relations, 20) +
                                                1))]))

    def generate(self, n_functions, max_size_functions):
        """generate
        Generates random functions
        :param n_functions: The number of functions to generate
        :param max_size_functions: The maximal size of a function
        """
        functions = []
        for i in range(n_functions):
            # Remove size 1 to prevent too easy examples
            size = random.randint(2, max_size_functions)
            function_name = "f" + str(i)
            # minus relations are random too
            f_rel = Function([random.choice(self.relations) +
                              ('-' * random.randint(0, 1))
                              for _ in range(size)], function_name)
            functions.append(f_rel)
        return functions

    def get_random_query(self):
        """get_random_query
        Returns a random query
        """
        return random.choice(self.relations) + "m" * random.randint(0, 1)
