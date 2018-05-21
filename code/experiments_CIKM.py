"""
Testing on real world data, with multiple inputs.
"""


from function_indexed_grammar import FunctionIndexedGrammar
from multiple_input_function import MultipleInputFunction
from regex_tree import RegexTree
from node import Node
from utils import dangie_fsm, make_DFS, get_sub_functions
import sys
import time
import pandas as pd

functions = dict()

webservices = ["FUNLIBTH", "FUNABE", "FUNMB1"]

#Functions wrapping information extraction techniques from the Web:
#have existential variables in the middle
#persons
functions["IE"] = []
functions["IE"].append(["personWonPrize-", "hasName"])
functions["IE"].append(["bornOnDate-", "hasName"])
functions["IE"].append(["graduatedFroM-", "hasName"])
functions["IE"].append(["isCitizenOf-", "hasName"])
functions["IE"].append(["livesIn-", "hasName"])


#books
functions["IE"].append(["bookWonPrize-", "title"])
functions["IE"].append(["publishedOnDate-", "title"])
functions["IE"].append(["publishedInCountry-", "title"])
functions["IE"].append(["publisher-", "title"])

#albums
functions["IE"].append(["releaseYear-", "title"])
functions["IE"].append(["releaseCountry-", "title"])
functions["IE"].append(["language-", "title"])
functions["IE"].append(["producer-", "title"])

#songs
functions["IE"].append(["songYear-", "title"])
functions["IE"].append(["songCountry-", "title"])
functions["IE"].append(["composer-", "title"])
functions["IE"].append(["lyricsBy-", "title"])

functions["IE"].append(["producer-", "title"])


#########################
functions["FUNLIBTH"] = []
#author info by author id
functions["FUNLIBTH"].append(["personWonPrize"])
functions["FUNLIBTH"].append(["isCitizenOf"])
functions["FUNLIBTH"].append(["bornOnDate"])
functions["FUNLIBTH"].append(["graduatedFroM"])
functions["FUNLIBTH"].append(["hasGender"])
functions["FUNLIBTH"].append(["livesIn"])

#author id by author name
functions["FUNLIBTH"].append(["hasName-"])

#book info by ISBN
functions["FUNLIBTH"].append(["title"])
functions["FUNLIBTH"].append(["wrote-","hasName"])
functions["FUNLIBTH"].append(["wrote-"])
functions["FUNLIBTH"].append(["publishedOnDate"])
functions["FUNLIBTH"].append(["publishedInCountry"])
functions["FUNLIBTH"].append(["publisher"])
functions["FUNLIBTH"].append(["bookWonPrize"])

#get ISBN by title
functions["FUNLIBTH"].append(["title-"])

functions["FUNLIBTH"].append(["personWonPrize", "prizeYear"])
functions["FUNLIBTH"].append(["personWonPrize", "genre"])
functions["FUNLIBTH"].append(["personWonPrize", "country"])
functions["FUNLIBTH"].append(["publisher", "country"])


#########################
functions["FUNABE"] = []
#books by author id (no existential variables, I generate all subqueries)
functions["FUNABE"].append(["wrote", "title"])
functions["FUNABE"].append(["wrote"])


#books by author name
functions["FUNABE"].append(["hasName-", "wrote", "title"])
functions["FUNABE"].append(["hasName-", "wrote"])
functions["FUNABE"].append(["hasName-"])


#book info by ISBN
functions["FUNABE"].append(["title"])
functions["FUNABE"].append(["wrote-","hasName"])
functions["FUNABE"].append(["wrote-"])
functions["FUNABE"].append(["publisher"])


#get book ISBN by title
functions["FUNLIBTH"].append(["title-"])

###################################
functions["FUNMB1"] = []
#artist id by artist name
functions["FUNMB1"].append(["hasName-"])

#artist info by artist id
functions["FUNMB1"].append(["genre"])
functions["FUNMB1"].append(["diedOnDate"])
functions["FUNMB1"].append(["bornOnDate"])
functions["FUNMB1"].append(["hasName"])


#get albums by artist id
functions["FUNMB1"].append(["release"]) #the albums

#album id by  album title
functions["FUNMB1"].append(["title-"])

#album info by album id
functions["FUNMB1"].append(["language"])
functions["FUNMB1"].append(["sang-", "hasName"])
functions["FUNMB1"].append(["sang-"])
functions["FUNMB1"].append(["producer"])
functions["FUNMB1"].append(["releaseYear"])
functions["FUNMB1"].append(["releaseCountry"])

#song ids by album id
functions["FUNMB1"].append(["track"])

#song id by song  title
functions["FUNMB1"].append(["title-"])

#song info by song id
functions["FUNMB1"].append(["language"])
functions["FUNMB1"].append(["sang-", "hasName"])
functions["FUNMB1"].append(["sang-"])
functions["FUNMB1"].append(["composer"])
functions["FUNMB1"].append(["lyricsBy"])
functions["FUNMB1"].append(["songYear"])
functions["FUNMB1"].append(["songCountry"])


#get collaborator
functions["FUNMB1"].append(["isMemberOf", "isMemberOf-",])

#get relatives by artist id
functions["FUNMB1"].append(["sibling"])
functions["FUNMB1"].append(["sibling"])
functions["FUNMB1"].append(["marriedTo"])
functions["FUNMB1"].append(["hasChild"])

functions["FUNMB1"].append(["producer", "country"])

for key in functions:
    f_temp = []
    for f in functions[key]:
        if f not in f_temp:
            f_temp.append(f)
    functions[key] = f_temp

for key in functions:
    for i in range(len(functions[key])):
        functions[key][i] = MultipleInputFunction(functions[key][i],
                                                  "f" + str(i), 1)

for x in webservices:
    functions[x] = list(set(filter(lambda x: x.n_relations() > 0,
                                    get_sub_functions(functions[x]) +
                             functions[x])))

# x + IE
for x in webservices:
    functions[x + " + IE"] = functions[x][:] + functions["IE"][:]

functions["ALL"] = functions["IE"][:]
for x in webservices:
    functions["ALL"] += functions[x][:]

def remove_minus(rel):
    if rel.endswith("m"):
        return rel[:-1]
    else:
        return rel


terminals = dict()
for key in functions:
    i_grammar = FunctionIndexedGrammar(functions[key], [[""]], palindrome=False)

    terminals[key] = i_grammar.get_terminals()
    terminals[key].remove("epsilon")
    terminals[key].remove("end")
    terminals[key].remove("query")
    terminals[key] = list(filter(lambda x: "_IN" not in x, terminals[key]))


    terminals[key] = list(set(map(lambda x: remove_minus(x), terminals[key])))
    terminals[key] = terminals[key] + \
        list(map(lambda x: x + "m", terminals[key]))

results = []

for key in functions:
    titles = []
    results_temp = []

    titles.append("Dataset")
    results_temp.append(key)

    reachable = set()

    print("====", key, "====")
    print("Number of functions:", len(functions[key]))

    functions_single = list(set(filter(lambda x: x.n_inputs == 1,
                                      functions[key])))
    functions_sub = list(set(filter(lambda x: x.n_relations() > 0,
                                    get_sub_functions(functions_single) +
                             functions_single)))
    new_function = "|".join(["(" +
                             ",".join(function.to_list("m")) +
                             ")" for function in functions_single])
    print(len(functions_single), "functions")
    titles.append("Number Functions")
    results_temp.append(len(functions_single))

    print(len(terminals[key]), "relations")
    titles.append("Number Relations")
    results_temp.append(len(terminals[key]))

    n_reachable = 0
    for terminal in terminals[key]:
        for f in functions_single:
            if f.to_list("m")[0] == terminal:
                n_reachable += 1
                break

    print("### Naturally reachable with subfunctions ###")
    titles.append("Naturally reachable with subfunctions")
    results_temp.append(n_reachable * 100.0 / float(len(terminals[key])))
    print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
                "% terminals reachable")

    n_reachable = 0
    for terminal in terminals[key]:
        for f in functions_single:
            if f.n_relations() == 1 and f.to_list("m")[0] == terminal:
                n_reachable += 1
                break
    print("### Naturally reachable without subfunctions ###")
    titles.append("Naturally reachable without subfunctions")
    results_temp.append(n_reachable * 100.0 / float(len(terminals[key])))
    print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
                "% terminals reachable")

    print("### DFS Weak ###")
    current_time = time.time()
    n_reachable = 0

    for terminal in terminals[key]:
        if terminal[-1] == "m":
            terminal = terminal[:-1] + "-"
        else:
            terminal = terminal
        if make_DFS(functions_single, terminal, weak=True):
            n_reachable += 1
        # else:
        #     print(terminal)

    print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
          "% terminals reachable")
    delta_t = time.time() - current_time
    print("Elapsed time", delta_t)
    titles.append("DFS Weak")
    results_temp.append(n_reachable * 100.0 / float(len(terminals[key])))
    titles.append("DFS Weak time")
    results_temp.append(delta_t)

    print("### DFS Strong ###")
    current_time = time.time()
    n_reachable = 0

    for terminal in terminals[key]:
        if terminal[-1] == "m":
            terminal = terminal[:-1] + "-"
        else:
            terminal = terminal
        if make_DFS(functions_single, terminal, weak=False):
            n_reachable += 1
        else:
           print(terminal)

    print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
          "% terminals reachable")
    delta_t = time.time() - current_time
    print("Elapsed time", delta_t)
    titles.append("DFS Strong")
    results_temp.append(n_reachable * 100.0 / float(len(terminals[key])))
    titles.append("DFS Strong time")
    results_temp.append(delta_t)


    print("### Smootie ###")
    titles.append("Smootie")
    n_reachable = 0

    current_time = time.time()

    for terminal in terminals[key]:
        i_grammar = FunctionIndexedGrammar(functions_single, [[terminal]],
                                           palindrome=True,
                                           susie=True)
        if i_grammar.is_empty():
            print(terminal)
        else:
            n_reachable += 1

    print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
            "% terminals reachable")
    results_temp.append(n_reachable * 100.0 / float(len(terminals[key])))

    delta_t = time.time() - current_time
    print("Elapsed time", delta_t)
    titles.append("Smootie time")
    results_temp.append(delta_t)


    results.append(results_temp)

df = pd.DataFrame(results, columns=titles)
df.to_csv("experiments21-05-2018.csv", index=False)
