"""
Difference Palindromes vs Susie
"""


from function_generator import FunctionGenerator
from function_indexed_grammar import FunctionIndexedGrammar
import time
from regex_tree import RegexTree
from node import Node


# number relations
n_relations = 10
size_max = 3
n_functions = 30
generator = FunctionGenerator(n_relations)

functions = []

for j in range(5, 70, 5):
    n_functions = j
# for j in range(2, 20, 2):
#     n_relations = j
    generator = FunctionGenerator(n_relations)
    for i in range(0, 200):
        # 1 function, size_max is 10
        functions = []
        temp = generator.generate(n_functions, size_max)
        functions += temp
        query = generator.get_random_query(functions)

        # ==== FSM ====

        current_time = time.time()
        new_function = "|".join(["(" +
                                 ",".join(function.to_list("m")) +
                                 ")" for function in functions])
        regex_function = RegexTree(Node(new_function))
        fsm = regex_function.to_fsm()
        fsm.close()

        # === NOT WEAK ===

        pfsm = fsm.get_palindrome_fsm(query, weak=False)
        fsm_not_weak_res = pfsm.is_empty()
        fsm_not_weak_time = time.time() - current_time

        # === WEAK ===

        pfsm = fsm.get_palindrome_fsm(query, weak=True)
        fsm_weak_res = pfsm.is_empty()
        fsm_weak_time = time.time() - current_time

        # ==== SUSIE ====

        current_time = time.time()
        i_grammar = FunctionIndexedGrammar(functions, [[query]],
                                           palindrome=True,
                                           susie=True)
        susie_res = i_grammar.is_empty()
        susie_time = time.time() - current_time

        with open("pali_vs_susie_weak.csv", "a") as f:
            f.write(str(fsm_not_weak_res) + "," +
                    str(fsm_weak_res) + "," +
                    str(susie_res) + "," +
                    str(fsm_not_weak_time) + "," +
                    str(fsm_weak_time) + "," +
                    str(susie_time) + "," +
                    str(n_relations) + "," +
                    str(size_max) + "," +
                    str(n_functions) + "\n")
