"""
Tests the performance of several orderings of the rules
"""


from function_generator import FunctionGenerator
from function_indexed_grammar import FunctionIndexedGrammar
import time


# number relations
n_relations = 10
size_max = 10
generator = FunctionGenerator(n_relations)

functions = []

optims = [2, 3, 6, 7, 8]

deltas = dict()
for optim in optims:
    deltas[optim] = []

for i in range(0, 1000):
    # 1 function, size_max is 10
    functions = []
    temp = generator.generate(25, size_max)
    functions += temp
    query = generator.get_random_query(functions)
    for optim in optims:
        current_time = time.time()
        grammar = FunctionIndexedGrammar(functions, [[query]], optim=optim)
        grammar.is_empty()
        delta_t = time.time() - current_time
        with open("rule_ordering2.csv", "a") as f:
            f.write(str(optim) + "," + str(i) + "," + str(delta_t) + "," +
                    str(n_relations) + "," + str(size_max) + "\n")
        deltas[optim].append(delta_t)
