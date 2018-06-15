"""
Difference Palindromes vs Susie
"""


from function_generator import FunctionGenerator
from function_indexed_grammar import FunctionIndexedGrammar
import time
from regex_tree import RegexTree
from node import Node
from utils import make_DFS, get_sub_functions, dangie_fsm
from multiple_input_function import MultipleInputFunction


# number relations
n_relations = 10
size_max = 3
n_functions = 30
generator = FunctionGenerator(n_relations)

functions = []

for j in range(5, 50, 5):
    n_functions = j
# for j in range(2, 20, 2):
#     n_relations = j
    generator = FunctionGenerator(n_relations)
    for i in range(0, 200):
        # 1 function, size_max is 10
        functions = []
        temp = generator.generate(n_functions, size_max)
        functions += temp
        functions_sub = list(set(filter(lambda x: x.n_relations() > 0,
                                        get_sub_functions(functions) +
                                 functions)))
        query = generator.get_random_query(functions)
        if query[-1] == "-":
            susie_query = query[:-1] + "m"
        else:
            susie_query = query

        functions_dangie = []
        for f in functions:
            functions_dangie.append(MultipleInputFunction(
                f.to_list("-"), f.name, 1))

        # ==== FSM ====

        current_time = time.time()
        new_function = "|".join(["(" +
                                 ",".join(function.to_list("m")) +
                                 ")" for function in functions])
        regex_function = RegexTree(Node(new_function))
        fsm = regex_function.to_fsm()
        fsm.close()

        # === FSM NOT WEAK ===

        pfsm = fsm.get_palindrome_fsm(susie_query, weak=False)
        fsm_not_weak_res = pfsm.is_empty()
        fsm_not_weak_time = time.time() - current_time

        # === FSM WEAK ===

        pfsm = fsm.get_palindrome_fsm(susie_query, weak=True)
        fsm_weak_res = pfsm.is_empty()
        fsm_weak_time = time.time() - current_time

        # ==== FSM Sub ====

        current_time = time.time()
        new_function = "|".join(["(" +
                                 ",".join(function.to_list("m")) +
                                 ")" for function in functions_sub])
        regex_function = RegexTree(Node(new_function))
        fsm = regex_function.to_fsm()
        fsm.close()

        # === FSM NOT WEAK Sub ===

        pfsm = fsm.get_palindrome_fsm(susie_query, weak=False)
        fsm_not_weak_sub_res = pfsm.is_empty()
        fsm_not_weak_sub_time = time.time() - current_time

        # === FSM WEAK Sub ===

        pfsm = fsm.get_palindrome_fsm(susie_query, weak=True)
        fsm_weak_sub_res = pfsm.is_empty()
        fsm_weak_sub_time = time.time() - current_time

        # === DFS Strong ===

        current_time = time.time()
        dfs_strong_res = not make_DFS(functions, query, weak=False)
        dfs_strong_time = time.time() - current_time

        # === DFS Weak ===

        current_time = time.time()
        dfs_weak_res = not make_DFS(functions, query, weak=True)
        dfs_weak_time = time.time() - current_time

        # === DFS Strong Sub ===

        current_time = time.time()
        dfs_strong_sub_res = not make_DFS(functions_sub, query, weak=False)
        dfs_strong_sub_time = time.time() - current_time

        # === DFS Weak Sub ===

        current_time = time.time()
        dfs_weak_sub_res = not make_DFS(functions_sub, query, weak=True)
        dfs_weak_sub_time = time.time() - current_time

        # ==== SUSIE ====

        current_time = time.time()
        i_grammar = FunctionIndexedGrammar(functions, [[susie_query]],
                                           palindrome=True,
                                           susie=True)
        susie_res = i_grammar.is_empty()
        susie_time = time.time() - current_time

        # ==== SUSIE sub ====

        current_time = time.time()
        i_grammar = FunctionIndexedGrammar(functions_sub, [[susie_query]],
                                           palindrome=True,
                                           susie=True)
        susie_sub_res = i_grammar.is_empty()
        susie_sub_time = time.time() - current_time


        # ==== Dangie - with FSM ====
        current_time = time.time()
        fsm = dangie_fsm(functions_dangie)

        if susie_query[-1] == "m":
            dangie_res = not fsm.accepts([susie_query[:-1] + "_OUT" + "m"])
        else:
            dangie_res = not fsm.accepts([susie_query + "_OUT"])
        dangie_time = time.time() - current_time



        if not susie_res and dfs_strong_res:
            print("susie pb")
            print(functions)
            print(query)
            exit()
        if not fsm_not_weak_res and dfs_strong_res:
            print("Fsm strong")
            pfsm = fsm.get_palindrome_fsm(susie_query, weak=False)
            print(pfsm.find_word())
            print(functions)
            print(query)
            exit()
        if not fsm_weak_res and dfs_weak_res:
            print("Fsm weak")
            pfsm = fsm.get_palindrome_fsm(susie_query, weak=True)
            print(pfsm.find_word())
            print(functions)
            print(query)
            exit()
        if not susie_res and fsm_not_weak_res:
            print("Fsm Susie strong")
            pfsm = fsm.get_palindrome_fsm(susie_query, weak=False)
            print(pfsm)
            print(functions)
            print(query)
            exit()
        if dangie_res and not dfs_weak_res:
            print("dangie pb")
            print(functions)
            print(query)
            exit()

        with open("results/pali_vs_susie_vs_dfs_vs_fsm.csv", "a") as f:
            f.write(str(fsm_not_weak_res) + "," +
                    str(fsm_weak_res) + "," +
                    str(fsm_not_weak_sub_res) + "," +
                    str(fsm_weak_sub_res) + "," +
                    str(dfs_weak_res) + "," +
                    str(dfs_strong_res) + "," +
                    str(dfs_weak_sub_res) + "," +
                    str(dfs_strong_sub_res) + "," +
                    str(susie_res) + "," +
                    str(susie_sub_res) + "," +
                    str(dangie_res) + "," +
                    str(fsm_not_weak_time) + "," +
                    str(fsm_weak_time) + "," +
                    str(fsm_not_weak_sub_time) + "," +
                    str(fsm_weak_sub_time) + "," +
                    str(dfs_weak_time) + "," +
                    str(dfs_strong_time) + "," +
                    str(dfs_weak_sub_time) + "," +
                    str(dfs_strong_sub_time) + "," +
                    str(susie_time) + "," +
                    str(susie_sub_time) + "," +
                    str(dangie_time) + "," +
                    str(n_relations) + "," +
                    str(size_max) + "," +
                    str(n_functions) + "\n")
