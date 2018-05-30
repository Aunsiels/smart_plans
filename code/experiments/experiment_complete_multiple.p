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

functions["FUNLIBTH"] = []
# FUNLIBTHGetAuthorInfoByName
functions["FUNLIBTH"].append(["hasWonPrize"])
functions["FUNLIBTH"].append(["hasIdAuthor"])
functions["FUNLIBTH"].append(["isCitizenOf"])
functions["FUNLIBTH"].append(["bornOnDate"])
functions["FUNLIBTH"].append(["graduatedFroM"])
functions["FUNLIBTH"].append(["hasGender"])
functions["FUNLIBTH"].append(["livesIn"])
# FUNLIBTHGetBookInfoByISBN
# functions["FUNLIBTH"].append(["hasISBN-"])
functions["FUNLIBTH"].append(["hasISBN-", "isTitledOf"])
functions["FUNLIBTH"].append(["hasISBN-", "hasIdBook"])
functions["FUNLIBTH"].append(["hasISBN-", "publishedOnDate"])
# functions["FUNLIBTH"].append(["hasISBN-", "wrote-"])
functions["FUNLIBTH"].append(["hasISBN-", "wrote-", "hasWonPrize"])
functions["FUNLIBTH"].append(["hasISBN-", "wrote-", "hasIdAuthor"])
# FUNLIBTHGetBookInfoByName
functions["FUNLIBTH"].append(["hasIdBook"])
functions["FUNLIBTH"].append(["isTitledOf"])
functions["FUNLIBTH"].append(["publishedOnDate"])
# functions["FUNLIBTH"].append(["wrote-"])
functions["FUNLIBTH"].append(["wrote-", "hasIdAuthor"])
functions["FUNLIBTH"].append(["wrote-", "hasWonPrize"])
# FUNLIBTHGetAuthorInfoByName
functions["FUNLIBTH"].append(["hasIdAuthor"])
functions["FUNLIBTH"].append(["livesIn"])
functions["FUNLIBTH"].append(["bornOnDate"])
functions["FUNLIBTH"].append(["graduatedFroM"])
functions["FUNLIBTH"].append(["hasGender"])
functions["FUNLIBTH"].append(["isCitizenOf"])
functions["FUNLIBTH"].append(["hasWonPrize"])
# FUNLIBTHGetBookInfoByID
# functions["FUNLIBTH"].append(["hasIdBook-"])
# functions["FUNLIBTH"].append(["hasIdBook-", "wrote-"])
functions["FUNLIBTH"].append(["hasIdBook-", "wrote-", "hasWonPrize"])
functions["FUNLIBTH"].append(["hasIdBook-", "wrote-", "hasIdAuthor"])
functions["FUNLIBTH"].append(["hasIdBook-", "publishedOnDate"])
functions["FUNLIBTH"].append(["hasIdBook-", "isTitledOf"])

functions["FUNABE"] = []
# FUNABEGetBookInfoByISBN
# functions["FUNABE"].append(["hasISBN-"])
functions["FUNABE"].append(["hasISBN-", "wrote-"])
functions["FUNABE"].append(["hasISBN-", "published"])
# FUNABEGetBookInfoByTitle
functions["FUNABE"].append(["hasISBN"])
functions["FUNABE"].append(["isTitled"])
functions["FUNABE"].append(["published-"])
functions["FUNABE"].append(["wrote-"])
# FUNABEGetBooksByAuthorName
# functions["FUNABE"].append(["wrote"])
functions["FUNABE"].append(["wrote", "isTitled"])
functions["FUNABE"].append(["wrote", "published-"])
# functions["FUNABE"].append(["wrote", "wrote-"])

functions["FUNISBN1"] = []
# FUNISBN1GetBooksByAuthorID
# functions["FUNISBN1"].append(["hasId-"])
# functions["FUNISBN1"].append(["hasId-", "wrote"])
functions["FUNISBN1"].append(["hasId-", "wrote", "hasIdBook"])
functions["FUNISBN1"].append(["hasId-", "wrote", "isTitled"])
functions["FUNISBN1"].append(["hasId-", "wrote", "hasISBN"])
# FUNISBN1GetBooksByName
# functions["FUNISBN1"].append(["isTitled-"])
functions["FUNISBN1"].append(["isTitled-", "hasIdBook"])
functions["FUNISBN1"].append(["isTitled-", "hasISBN"])
# functions["FUNISBN1"].append(["isTitled-", "wrote-"])
functions["FUNISBN1"].append(["isTitled-", "wrote-", "hasIdAuthor"])

functions["FUNMB1"] = []
# FUNMB1GetArtistInfoByID
# functions["FUNMB1"].append(["hasIdArtist-"])
functions["FUNMB1"].append(["hasIdArtist-", "describes-"])
functions["FUNMB1"].append(["hasIdArtist-", "rated"])
functions["FUNMB1"].append(["hasIdArtist-", "diedOnDate"])
functions["FUNMB1"].append(["hasIdArtist-", "bornOnDate"])
# FUNMB1etArtistInfoByName
functions["FUNMB1"].append(["hasIdArtist"])
functions["FUNMB1"].append(["diedOnDate"])
functions["FUNMB1"].append(["bornOnDate"])
# FUNMB1setArtistsByRealeaseID
# functions["FUNMB1"].append(["hasIdRelease-"])
functions["FUNMB1"].append(["hasIdRelease-", "inLanguage"])
functions["FUNMB1"].append(["hasIdRelease-", "sang-"])
functions["FUNMB1"].append(["hasIdRelease-", "produced-"])
functions["FUNMB1"].append(["hasIdRelease-", "lyricsBy"])
# FUNMB1setCollaboratorInfoById
# functions["FUNMB1"].append(["hasIdArtist-"])
# functions["FUNMB1"].append(["hasIdArtist-", "isMemberOf-"])
functions["FUNMB1"].append(["hasIdArtist-", "isMemberOf-", "hasIdArtist"])
# FUNMB1setCollaboratorsByID
# functions["FUNMB1"].append(["hasIdArtist-"])
# functions["FUNMB1"].append(["hasIdArtist-", "isMemberOf"])
functions["FUNMB1"].append(["hasIdArtist-", "isMemberOf", "hasIdCollab"])
# FUNMB1setRelativesByID
# functions["FUNMB1"].append(["hasIdArtist-"])
# functions["FUNMB1"].append(["hasIdArtist-", "hasSiblings"])
functions["FUNMB1"].append(["hasIdArtist-", "hasSiblings", "hasIdSibling"])
# functions["FUNMB1"].append(["hasIdArtist-", "isMarriedTo"])
functions["FUNMB1"].append(["hasIdArtist-", "isMarriedTo", "hasIdSpouse"])
# functions["FUNMB1"].append(["hasIdArtist-", "hasChild"])
functions["FUNMB1"].append(["hasIdArtist-", "hasChild", "hasIdChild"])
functions["FUNMB1"].append(["hasIdArtist-", "divorcedOn"])
functions["FUNMB1"].append(["hasIdArtist-", "marriedOn"])
# FUNMB1setReleaseInfoByID
# functions["FUNMB1"].append(["hasIdRelease-"])
functions["FUNMB1"].append(["hasIdRelease-", "inLanguage"])
functions["FUNMB1"].append(["hasIdRelease-", "happenedIn"])
functions["FUNMB1"].append(["hasIdRelease-", "hasTrackNumber"])
functions["FUNMB1"].append(["hasIdRelease-", "happenedOnDate"])
functions["FUNMB1"].append(["hasIdRelease-", "hasDiscNumber"])
functions["FUNMB1"].append(["hasIdRelease-", "describes-"])
# functions["FUNMB1"].append(["hasIdRelease-", "released-"])
functions["FUNMB1"].append(["hasIdRelease-", "released-", "hasIdArtist"])
# FUNMB1setReleaseInfoByTitle
functions["FUNMB1"].append(["hasIdRelease"])
functions["FUNMB1"].append(["inLanguage"])
functions["FUNMB1"].append(["released-"])
# FUNMB1setRealeaseByArtistID
# functions["FUNMB1"].append(["hasIdArtist-"])
# functions["FUNMB1"].append(["hasIdArtist-", "released"])
functions["FUNMB1"].append(["hasIdArtist-", "released", "hasIdRelease"])
functions["FUNMB1"].append(["hasIdArtist-", "released", "inLanguage"])
# FUNMB1setTrackInfoByID
# functions["FUNMB1"].append(["hasIdTrack-"])
functions["FUNMB1"].append(["hasIdTrack-", "hasDuration"])
functions["FUNMB1"].append(["hasIdTrack-", "sang-"])
functions["FUNMB1"].append(["hasIdTrack-", "hasValue"])
functions["FUNMB1"].append(["hasIdTrack-", "isMemberOf"])
# FUNMB1setTrackInfoByName
functions["FUNMB1"].append(["hasIdTrack"])
functions["FUNMB1"].append(["isMemberOf"])
functions["FUNMB1"].append(["sang-"])
functions["FUNMB1"].append(["hasValue"])
functions["FUNMB1"].append(["hasDuration"])
# FUNMB1setTracksByReleaseID
# functions["FUNMB1"].append(["hasIdRelease-"])
functions["FUNMB1"].append(["hasIdRelease-", "inLanguage"])
# functions["FUNMB1"].append(["hasIdRelease-", "isMemberOf-"])
functions["FUNMB1"].append(["hasIdRelease-", "isMemberOf-", "hasDuration"])
functions["FUNMB1"].append(["hasIdRelease-", "isMemberOf-", "hasIdTrack"])
# FUNMB1setTracksByArtistId
# functions["FUNMB1"].append(["hasIdArtist-"])
functions["FUNMB1"].append(["hasIdArtist-", "sang"])

functions["FUNLYRIC1"] = []
# FUNMB1GetRealeaseByArtistID
# functions["FUNLYRIC1"].append(["hasIdArtist-"])
functions["FUNLYRIC1"].append(["hasIdArtist-", "released", "hasIdRelease"])
functions["FUNLYRIC1"].append(["hasIdArtist-", "released", "inLanguage"])
# FUNLYRIC1GetLyricsInfoByArtistTrackName
# functions["FUNLYRIC1"].append(["hasLyrics"])
functions["FUNLYRIC1"].append(["hasLyrics", "describes-"])
# FUNMB1GetArtistInfoByName
functions["FUNLYRIC1"].append(["hasIdArtist"])

functions["FUNLF1"] = []
# FUNLF1GetReleaseInfoByName
functions["FUNLF1"].append(["released-"])
functions["FUNLF1"].append(["describes-"])
functions["FUNLF1"].append(["happenedOnDate"])
# FUNLF1GetTrackInfoById
# functions["FUNLF1"].append(["hasIdTrack-"])
# functions["FUNLF1"].append(["hasIdTrack-", "isMemberOf"])
functions["FUNLF1"].append(["hasIdTrack-", "isMemberOf", "hasIdRelease"])
functions["FUNLF1"].append(["hasIdTrack-", "describes-"])
functions["FUNLF1"].append(["hasIdTrack-", "hasDuration"])
# functions["FUNLF1"].append(["hasIdTrack-", "sang-"])
functions["FUNLF1"].append(["hasIdTrack-", "sang-", "hasIdArtist"])
# FUNLF1GetArtistInfoByName
functions["FUNLF1"].append(["hasIdArtist"])
functions["FUNLF1"].append(["describes-"])
# FUNLF1GetReleaseInfoByID
# functions["FUNLF1"].append(["hasIdRelease-"])
functions["FUNLF1"].append(["hasIdRelease-", "released-"])
functions["FUNLF1"].append(["hasIdRelease-", "describes-"])
functions["FUNLF1"].append(["hasIdRelease-", "happenedOnDate"])
# FUNLF1GetTrackInfoByName
functions["FUNLF1"].append(["sang-"])
functions["FUNLF1"].append(["describes-"])
# FUNF1GetArtistInfoByID
functions["FUNLF1"].append(["hasIdArtist-"])
functions["FUNLF1"].append(["describes-"])

functions["Test"] = []
functions["Test"].append(["b-", "a-", "q"])
functions["Test"].append(["b", "c"])
functions["Test"].append(["a"])
functions["Test"].append(["c-"])

functions["Test2"] = []
functions["Test2"].append(["a", "b"])
functions["Test2"].append(["b-"])

functions["Test3"] = []
functions["Test3"].append(["a"])
functions["Test3"].append(["b-", "a-", "q"])

### NICOLETA

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


#########################
#author info by author id
functions["IE"].append(["personWonPrize"])
functions["IE"].append(["isCitizenOf"])
functions["IE"].append(["bornOnDate"])
functions["IE"].append(["graduatedFroM"])
functions["IE"].append(["hasGender"])
functions["IE"].append(["livesIn"])

functions["IE"].append(["personWonPrize", "prizeYear"])

#author id by author name
functions["IE"].append(["hasName-"])

#book info by ISBN
functions["IE"].append(["title"])
functions["IE"].append(["wrote-","hasName"])
functions["IE"].append(["wrote-"])
functions["IE"].append(["publishedOnDate"])
functions["IE"].append(["publishedInCountry"])
functions["IE"].append(["publisher"])
functions["IE"].append(["bookWonPrize"])

#get ISBN by title
functions["IE"].append(["title-"])

#########################
#books by author id (no existential variables, I generate all subqueries)
functions["IE"].append(["wrote", "title"])
functions["IE"].append(["wrote"])


#books by author name
functions["IE"].append(["hasName-", "wrote", "title"])
functions["IE"].append(["hasName-", "wrote"])
functions["IE"].append(["hasName-"])


#book info by ISBN
functions["IE"].append(["title"])
functions["IE"].append(["wrote-","hasName"])
functions["IE"].append(["wrote-"])
functions["IE"].append(["publisher"])


#get book ISBN by title
functions["IE"].append(["title-"])

###################################
#artist id by artist name
functions["IE"].append(["hasName-"])

#artist info by artist id
functions["IE"].append(["genre"])
functions["IE"].append(["diedOnDate"])
functions["IE"].append(["bornOnDate"])
functions["IE"].append(["hasName"])


#get albums by artist id
functions["IE"].append(["release"]) #the albums

#album id by  album title
functions["IE"].append(["title-"])

#album info by album id
functions["IE"].append(["language"])
functions["IE"].append(["sang-", "hasName"])
functions["IE"].append(["sang-"])
functions["IE"].append(["producer"])
functions["IE"].append(["releaseYear"])
functions["IE"].append(["releaseCountry"])

#song ids by album id
functions["IE"].append(["track"])

#song id by song  title
functions["IE"].append(["title-"])

#song info by song id
functions["IE"].append(["language"])
functions["IE"].append(["sang-", "hasName"])
functions["IE"].append(["sang-"])
functions["IE"].append(["composer"])
functions["IE"].append(["lyricsBy"])
functions["IE"].append(["songYear"])
functions["IE"].append(["songCountry"])


#get collaborator
functions["IE"].append(["isMemberOf", "isMemberOf-",])

#get relatives by artist id
functions["IE"].append(["sibling"])
functions["IE"].append(["sibling"])
functions["IE"].append(["marriedTo"])
functions["IE"].append(["hasChild"])

# Make each function unique
# print("Number functions:", len(functions))
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

# Multiple Input functions
functions["FUNABE"].append(MultipleInputFunction(["wrote", "hasISBN"], "f", 2))
functions["FUNABE"].append(MultipleInputFunction(["wrote", "published"], "f",
                                                 2))
functions["FUNLF1"].append(MultipleInputFunction(["released", "hasIdRelease"],
                                                  "f", 2))
functions["FUNLF1"].append(MultipleInputFunction(["released", "describes-"],
                                                 "f", 2))
functions["FUNLF1"].append(MultipleInputFunction(["released", "happenedOnDate"],
                                                 "f", 2))
functions["FUNLF1"].append(MultipleInputFunction(["sang", "hasIdTrack"],
                                                 "f", 2))
functions["FUNLF1"].append(MultipleInputFunction(["sang", "hasDuration"],
                                                 "f", 2))
functions["FUNLF1"].append(MultipleInputFunction(["sang", "isMemberOf"],
                                                 "f", 2))
functions["FUNLF1"].append(MultipleInputFunction(["sang", "isMemberOf",
                                                  "hasIdAlbuM"],
                                                 "f", 2))
functions["FUNLF1"].append(MultipleInputFunction(["sang", "describes-"],
                                                 "f", 2))
functions["FUNLF1"].append(MultipleInputFunction(["sang-", "hasIdArtist"],
                                                 "f", 2))
functions["Test3"].append(MultipleInputFunction(["a-"],
                                                 "f", 2))
functions["Test3"].append(MultipleInputFunction(["a", "b"],
                                                 "f", 2))



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

    for weak in [True, False]:
        for sub_functions in [True, False]:
            # With FSM
            if weak:
                qualitatif = "Weak"
            else:
                qualitatif = "Strong"

            if sub_functions:
                print("### Pali - with subfunctions " + qualitatif + " ###")
                titles.append("Pali - with subfunctions " +
                              qualitatif)
            else:
                print("### Pali - no subfunctions " + qualitatif + " ###")
                titles.append("Pali - no subfunctions " +
                              qualitatif)
            current_time = time.time()
            regex_function = RegexTree(Node(new_function))
            fsm = regex_function.to_fsm()
            fsm.close()
            n_reachable = 0
            for terminal in terminals[key]:
                pfsm = fsm.get_palindrome_fsm(terminal,
                                              sub_functions=sub_functions,
                                              weak=weak)
                if not pfsm.is_empty():
                    n_reachable += 1
                else:
                    print(terminal)

            print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
                        "% terminals reachable")
            results_temp.append(n_reachable * 100.0 /
                                float(len(terminals[key])))
            delta_t = (time.time() - current_time)
            print("Elapsed time", delta_t * 1000.0, 'ms')
            if sub_functions:
                titles.append("Pali - with subfunctions " +
                              qualitatif + " time")
            else:
                titles.append("Pali - no subfunctions " +
                              qualitatif + " time")
            results_temp.append(delta_t)

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
        else:
            print(terminal)

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

    print("### DFS Weak Subfunctions ###")
    current_time = time.time()
    n_reachable = 0

    for terminal in terminals[key]:
        if terminal[-1] == "m":
            terminal = terminal[:-1] + "-"
        else:
            terminal = terminal
        if make_DFS(functions_sub, terminal, weak=True):
            n_reachable += 1
        else:
            print(terminal)

    print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
          "% terminals reachable")
    delta_t = time.time() - current_time
    print("Elapsed time", delta_t)
    titles.append("DFS Weak Subfunctions")
    results_temp.append(n_reachable * 100.0 / float(len(terminals[key])))
    titles.append("DFS Weak Subfunctions time")
    results_temp.append(delta_t)

    print("### DFS Strong Subfunctions ###")
    current_time = time.time()
    n_reachable = 0

    for terminal in terminals[key]:
        if terminal[-1] == "m":
            terminal = terminal[:-1] + "-"
        else:
            terminal = terminal
        if make_DFS(functions_sub, terminal, weak=False):
            n_reachable += 1
        # else:
        #    print(terminal)

    print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
          "% terminals reachable")
    delta_t = time.time() - current_time
    print("Elapsed time", delta_t)
    titles.append("DFS Strong Subfunctions")
    results_temp.append(n_reachable * 100.0 / float(len(terminals[key])))
    titles.append("DFS Strong Subfunctions time")
    results_temp.append(delta_t)


    # print("### Dangie - with FSM ###")
    # current_time = time.time()
    # fsm = dangie_fsm(functions[key])
    # n_reachable = 0

    # for terminal in terminals[key]:
    #     if terminal[-1] == "m":
    #         terminal = terminal[:-1] + "_OUT" + "m"
    #     else:
    #         terminal = terminal + "_OUT"
    #     if fsm.accepts([terminal]):
    #         n_reachable += 1
    #         reachable.add(terminal)
    #     else:
    #         pass
    #         # print(terminal)

    # print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
    #       "% terminals reachable")
    # delta_t = time.time() - current_time
    # print("Elapsed time", delta_t)

    print(terminals[key])

    for palindrome in [True]:
        if palindrome:
            print("### Smootie ###")
            titles.append("Smootie")
        else:
            print("### Forward-backward ###")
            titles.append("Forward-backward")
        # print("###", key, "with palindrome =", palindrome, "###")
        n_reachable = 0

        current_time = time.time()

        for terminal in terminals[key]:
            i_grammar = FunctionIndexedGrammar(functions_single, [[terminal]],
                                               palindrome=palindrome,
                                               susie=True)
            # print(i_grammar.rules.get_length(), "rules")
            if i_grammar.is_empty():
                if not palindrome and terminal in reachable:
                    pass
                    # print(terminal, "was reachable")
                print(terminal)
            else:
                # print(terminal, "Can be reached")
                n_reachable += 1
                if not palindrome and terminal not in reachable:
                    pass
                    # print(terminal, "was not reachable")
                reachable.add(terminal)
                #with open('prolog_web_services/' + terminal + '.pl', "w") as f:
                #    f.write(i_grammar.get_prolog_rules(3))
            sys.stdout.flush()

        print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
                "% terminals reachable")
        results_temp.append(n_reachable * 100.0 / float(len(terminals[key])))

        delta_t = time.time() - current_time
        print("Elapsed time", delta_t)
        if palindrome:
            titles.append("Smootie time")
        else:
            titles.append("Forward-backward time")
        results_temp.append(delta_t)

    results.append(results_temp)

df = pd.DataFrame(results, columns=titles)
df.to_csv("experiments20-05-2018.csv", index=False)
