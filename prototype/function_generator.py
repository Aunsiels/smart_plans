import random
import string
import math
import sys

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
    sys.exit("Correct usage : python3 function_generator.py n_relations " +
             "n_functions max_size_functions function_file query_file")

n_relations = int(sys.argv[1])
n_functions = int(sys.argv[2])
max_size_functions = int(sys.argv[3])

# m is used for minus
# not exactly n_relations different relations
relations = [''.join([random.choice(string.ascii_lowercase.replace("m", ""))
                     for _ in range(int(math.log(n_relations, 20) + 1))])
             for _ in range(n_relations)]


lasts = []
f = open(sys.argv[4], "w")

for i in range(n_functions):
    # Remove size 1 to prevent too easy examples
    size = random.randint(2, max_size_functions)
    function_name = "f" + str(i)
    # minus relations are random too
    f_rel = [random.choice(relations) + ('-' * random.randint(0, 1))
             for _ in range(size)]
    f.write(function_name + " :- " + ", ".join(f_rel) + ".\n")
    lasts.append(f_rel[-1])

f.close()

with open(sys.argv[5], "w") as f:
    f.write(random.choice(lasts) + "\n")
