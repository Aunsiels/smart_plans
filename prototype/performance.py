from function_generator import FunctionGenerator
from function_indexed_grammar import FunctionIndexedGrammar
import time


# number relations
n_relations = 5
size_max = 10
generator = FunctionGenerator(n_relations)

functions = []

for i in range(1, 36):
    # 1 function, size_max is 10
    temp = generator.generate(1, size_max)
    functions += temp
    query = generator.get_random_query(functions)
    for optim in [0, 1, 2, 3]:
        current_time = time.time()
        grammar = FunctionIndexedGrammar(functions, [[query]], optim=optim)
        grammar.is_empty()
        delta_t = time.time() - current_time
        print(str(optim) + "," + str(i) + "," + str(delta_t) + "," +
              str(n_relations) + "," + str(size_max))
