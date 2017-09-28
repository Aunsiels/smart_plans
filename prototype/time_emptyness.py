import time
from function_generator import FunctionGenerator
from function_indexed_grammar import FunctionIndexedGrammar
import cProfile


def get_millis():
    return int(round(time.time() * 1000))


current_time = get_millis()

for _ in range(10):
    generator = FunctionGenerator(10)
    functions = generator.generate(5, 4)
    query = generator.get_random_query(functions)
    print(functions)
    print(query)
    grammar = FunctionIndexedGrammar(functions, query)
    cProfile.run("grammar.is_empty()")
    print(get_millis() - current_time)
    current_time = get_millis()
