from function_generator import FunctionGenerator
from function_indexed_grammar import FunctionIndexedGrammar
import time


# number relations
n_relations = 15
size_max = 10
generator = FunctionGenerator(n_relations)

functions = []

for i in range(1, 101):
    current_time = time.time()
    # 1 function, size_max is 10
    temp = generator.generate(1, size_max)
    functions += temp
    query = generator.get_random_query(functions)
    optim = True
    grammar = FunctionIndexedGrammar(functions, [[query]], optim=True)
    grammar.is_empty()
    delta_t = time.time() - current_time
    print(str(True) + "," + str(i) + "," + str(delta_t) + "," +
          str(n_relations) + "," + str(size_max))
    # current_time = time.time()
    # optim = False
    # grammar = FunctionIndexedGrammar(functions, [[query]], optim=False)
    # grammar.is_empty()
    # delta_t = time.time() - current_time
    # print(str(False) + "," + str(i) + "," + str(delta_t) + "," +
    #       str(n_relations) + "," + str(size_max))
