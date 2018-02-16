import time
from function_generator import FunctionGenerator
from function_indexed_grammar import FunctionIndexedGrammar
import cProfile


def get_millis():
    return int(round(time.time() * 1000))


current_time = get_millis()
total = 0
n_loop = 10

for _ in range(n_loop):
    generator = FunctionGenerator(5)
    functions = generator.generate(25, 10)
    query = generator.get_random_query(functions)
    # print(functions)
    # print(query)
    grammar = FunctionIndexedGrammar(functions, query)
    # cProfile.run("grammar.is_empty()")
    print(get_millis() - current_time)
    total += get_millis() - current_time
    current_time = get_millis()

print("Mean :" + str(total / n_loop))
