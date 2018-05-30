import sys
import random
from function_generator import FunctionGenerator


"""
Here we generate random functions and queries for testing purposes.
It takes 5 arguments:
    * the number of relations
    * the number of functions
    * the maximum size of the functions
    * the file where to write the functions
    * the file where to write the query
"""

if len(sys.argv) != 6:
    sys.exit("Correct usage : python3 function_generator_main.py n_relations " +
             "n_functions max_size_functions function_file query_file")

# Read arguments
n_relations = int(sys.argv[1])
n_functions = int(sys.argv[2])
max_size_functions = int(sys.argv[3])

generator = FunctionGenerator(n_relations)

lasts = []

f = open(sys.argv[4], "w")

# Generate the functions, in prolog format
for f_rel in generator.generate(n_functions, max_size_functions):
    f.write(f_rel.get_prolog())
    lasts.append(f_rel.get_last())

f.close()

# Generate the query
with open(sys.argv[5], "w") as f:
    f.write(random.choice(lasts) + "\n")
