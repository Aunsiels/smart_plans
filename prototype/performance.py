from function_generator import FunctionGenerator
from function_indexed_grammar import FunctionIndexedGrammar
import time


generator = FunctionGenerator(10)

functions = []

for i in range(1, 101):
    current_time = time.time()
    temp = generator.generate(1, 10)
    functions += temp
    query = generator.get_random_query(functions)
    optim = True
    grammar = FunctionIndexedGrammar(functions, [[query]], optim=True)
    grammar.is_empty()
    delta_t = time.time() - current_time
    print(str(True) + "," + str(i) + "," + str(delta_t))
    current_time = time.time()
    optim = False
    grammar = FunctionIndexedGrammar(functions, [[query]], optim=False)
    grammar.is_empty()
    delta_t = time.time() - current_time
    print(str(False) + "," + str(i) + "," + str(delta_t))
