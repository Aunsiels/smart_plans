"""
Testing on real world data, with multiple inputs.
"""


from function_indexed_grammar import FunctionIndexedGrammar
from multiple_input_function import MultipleInputFunction
from regex_tree import RegexTree
from node import Node
import sys
import time

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
# functions["FUNABE"].append(MultipleInputFunction(["wrote", "hasISBN"], "f", 2))
# functions["FUNABE"].append(MultipleInputFunction(["wrote", "published"], "f",
#                                                  2))
# functions.append(MultipleInputFunction(["released", "hasIdRelease"],
#                                        "f", 2))
# functions["FUNLF1"].append(MultipleInputFunction(["released", "describes-"],
#                                                  "f", 2))
# functions["FUNLF1"].append(MultipleInputFunction(["released", "happenedOnDate"],
#                                                  "f", 2))
# functions["FUNLF1"].append(MultipleInputFunction(["sang", "hasIdTrack"],
#                                                  "f", 2))
# functions["FUNLF1"].append(MultipleInputFunction(["sang", "hasDuration"],
#                                                  "f", 2))
# functions["FUNLF1"].append(MultipleInputFunction(["sang", "isMemberOf"],
#                                                  "f", 2))
# functions["FUNLF1"].append(MultipleInputFunction(["sang", "isMemberOf",
#                                                   "hasIdAlbum"],
#                                                  "f", 2))
# functions["FUNLF1"].append(MultipleInputFunction(["sang", "describes-"],
#                                                  "f", 2))
# functions["FUNLF1"].append(MultipleInputFunction(["sang-", "hasIdArtist"],
#                                            "f", 2))



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

for key in functions:
    reachable = set()

    # With FSM
    current_time = time.time()
    functions_single = list(set(filter(lambda x: x.n_inputs == 1,
                                      functions[key])))
    new_function = "|".join(["(" +
                             ",".join(function.to_list("m")) +
                             ")" for function in functions_single])
    regex_function = RegexTree(Node(new_function))
    fsm = regex_function.to_fsm()
    fsm.close()
    n_reachable = 0
    for terminal in terminals[key]:
        pfsm = fsm.get_palindrome_fsm(terminal)
        if not pfsm.is_empty():
            n_reachable += 1

    print("With FSM")
    print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
                "% terminals reachable")
    delta_t = time.time() - current_time
    print("Elapsed time", delta_t)

    for palindrome in [True, False]:
        print(key, "with palindrome =", palindrome)
        n_reachable = 0

        current_time = time.time()

        for terminal in terminals[key]:
            i_grammar = FunctionIndexedGrammar(functions[key], [[terminal]],
                                               palindrome=palindrome,
                                               susie=True)
            if i_grammar.is_empty():
                if not palindrome and terminal in reachable:
                    print(terminal, "was reachable")
                pass
            else:
                # print(terminal, "Can be reached")
                n_reachable += 1
                if not palindrome and terminal not in reachable:
                    print(terminal, "was not reachable")
                reachable.add(terminal)
                #with open('prolog_web_services/' + terminal + '.pl', "w") as f:
                #    f.write(i_grammar.get_prolog_rules(3))
            sys.stdout.flush()

        print(str(n_reachable * 100.0 / float(len(terminals[key]))) +
                "% terminals reachable")

        delta_t = time.time() - current_time
        print("Elapsed time", delta_t)
