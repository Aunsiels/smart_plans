# In this script, we try to evaluate the influence of a loop. To do so, we
# generate automatically some function, then we take one of them, inverse it
# and add it to the grammar. We compare the influence when we use the rule
# C[sigma] -> ... or the middle rules.

from function_generator import FunctionGenerator
from function_indexed_grammar import FunctionIndexedGrammar
from function import Function
import time


# number relations
n_relations = 6
size_max = 6
generator = FunctionGenerator(n_relations)

functions = []

for i in range(0, 1000):
    # 10 functions, size_max is 10
    functions = []
    n_functions = 9
    temp = generator.generate(n_functions, size_max)
    functions += temp
    query = generator.get_random_query(functions)

    current_time = time.time()
    grammar = FunctionIndexedGrammar(functions, [[query]], 7, False)
    res0 = grammar.is_empty()
    delta_t0 = time.time() - current_time
    n_rules0 = grammar.get_n_rules()
    n_rules0 = n_rules0[0] + n_rules0[1]

    current_time = time.time()
    grammar = FunctionIndexedGrammar(functions, [[query]], 7, True)
    res1 = grammar.is_empty()
    delta_t1 = time.time() - current_time
    n_rules1 = grammar.get_n_rules()
    n_rules1 = n_rules1[0] + n_rules1[1]

    functions.append(Function(functions[-1].get_inverse_function(), "f"))

    current_time = time.time()
    grammar = FunctionIndexedGrammar(functions, [[query]], 7, False)
    res2 = grammar.is_empty()
    delta_t2 = time.time() - current_time
    n_rules2 = grammar.get_n_rules()
    n_rules2 = n_rules2[0] + n_rules2[1]

    current_time = time.time()
    grammar = FunctionIndexedGrammar(functions, [[query]], 7, True)
    res3 = grammar.is_empty()
    delta_t3 = time.time() - current_time
    n_rules3 = grammar.get_n_rules()
    n_rules3 = n_rules3[0] + n_rules3[1]

    functions.append(Function(functions[-4].get_inverse_function(), "f"))

    current_time = time.time()
    grammar = FunctionIndexedGrammar(functions, [[query]], 7, False)
    res4 = grammar.is_empty()
    delta_t4 = time.time() - current_time
    n_rules4 = grammar.get_n_rules()
    n_rules4 = n_rules4[0] + n_rules4[1]

    current_time = time.time()
    grammar = FunctionIndexedGrammar(functions, [[query]], 7, True)
    res5 = grammar.is_empty()
    delta_t5 = time.time() - current_time
    n_rules5 = grammar.get_n_rules()
    n_rules5 = n_rules5[0] + n_rules5[1]

    with open("influence_loop2.csv", "a") as f:
        f.write(",".join([str(n_functions),
                          str(res0), str(delta_t0), str(n_rules0),
                          str(res1), str(delta_t1), str(n_rules1),
                          str(res2), str(delta_t2), str(n_rules2),
                          str(res3), str(delta_t3), str(n_rules3),
                          str(res4), str(delta_t4), str(n_rules4),
                          str(res5), str(delta_t5), str(n_rules5)
                          ]) + "\n")
    assert res0 == res1, functions
    assert res2 == res3, functions
    assert res4 == res5, functions
