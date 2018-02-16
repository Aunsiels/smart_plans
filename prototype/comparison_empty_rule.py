# In this script, we look at the effect of having the rule C[sigma] -> ...
# or the middle rules.

from function_generator import FunctionGenerator
from function_indexed_grammar import FunctionIndexedGrammar
import random
import time


# Number relations
n_relations = 4
size_max = 4
generator = FunctionGenerator(n_relations)

for i in range(0, 1000):
    # random number of function, size_max is 10
    functions = []
    n_functions = random.randint(10, 15)
    temp = generator.generate(n_functions, size_max)
    functions += temp
    query = generator.get_random_query(functions)

    # With middle rules
    current_time = time.time()
    grammar = FunctionIndexedGrammar(functions, [[query]], 7, False)
    res0 = grammar.is_empty()
    delta_t0 = time.time() - current_time
    n_rules0 = grammar.get_n_rules()
    n_rules0 = n_rules0[0] + n_rules0[1]

    # With C[sigma] -> ... and no middle rule
    current_time = time.time()
    grammar = FunctionIndexedGrammar(functions, [[query]], 7, True)
    res1 = grammar.is_empty()
    delta_t1 = time.time() - current_time
    n_rules1 = grammar.get_n_rules()
    n_rules1 = n_rules1[0] + n_rules1[1]

    # Save the results in a file
    with open("comparison_empty_rule.csv", "a") as f:
        f.write(",".join([str(n_functions), str(res0), str(delta_t0),
                          str(n_rules0),
                          str(res1), str(delta_t1), str(n_rules1)]) + "\n")
    # Good for testing
    assert(res0 == res1)
