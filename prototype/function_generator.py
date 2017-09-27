import random
import string
import math
from function import Function


class FunctionGenerator(object):

    def __init__(self, n_relations):
        # m is used for minus
        # not exactly n_relations different relations
        self.relations = [''.join([random.choice(
            string.ascii_lowercase.replace("m", ""))
                             for _ in range(int(math.log(n_relations, 20) +
                                                1))])
                     for _ in range(n_relations)]

    def generate(self, n_functions, max_size_functions):
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
