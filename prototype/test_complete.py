from function_indexed_grammar import FunctionIndexedGrammar
from function import Function

functions = []

# GetAuthorInfoByName
# functions.append(["hasWonPrize"])  # 0
# functions.append(["hasId"])  # 0
# functions.append(["isCitizenOf"])  # 0
# functions.append(["bornOnDate"])  # 0
# functions.append(["graduatedFrom"])  # 0
# functions.append(["hasGender"])  # 0
# functions.append(["livesIn"])  # 0
# GetCollaboratorInfoById
functions.append(["hasId-"])  # 0
functions.append(["hasId-", "isMemberOf-"])  # 0
functions.append(["hasId-", "isMemberOf-", "hasId"])  # 0
# GetLyricsInfoByArtistTrackName
functions.append(["hasLyrics"])  # 0
functions.append(["hasLyrics", "describes-"])  # 0
# GetBookInfoByISBN
# functions.append(["hasISBN-"])  # 0
# functions.append(["hasISBN-", "wrote-"])  # 0
# functions.append(["hasISBN-", "published"])  # 0
# GetTracksByArtistId
functions.append(["hasId-"])  # 0
functions.append(["hasId-", "sang"])  # 0
# GetTrackInfoByName
functions.append(["hasId"])  # 0
functions.append(["isMemberOf"])  # 0
functions.append(["sang-"])  # 0
functions.append(["hasValue"])  # 0
functions.append(["hasDuration"])  # 0
# GetTracksByReleaseID
functions.append(["hasId-"])  # 0
functions.append(["hasId-", "inLanguage"])  # 0
functions.append(["hasID-", "isMemberOf-"])  # 0
functions.append(["hasID-", "isMemberOf-", "hasDuration"])  # 0
functions.append(["hasID-", "isMemberOf-", "hasId"])  # 0
# GetTrackInfoByID
functions.append(["hasId-"])  # 0
functions.append(["hasId-", "hasDuration"])  # 0
functions.append(["hasId-", "isMemberOf"])  # 0
functions.append(["hasId-", "sang-"])  # 0
functions.append(["hasId-", "hasValue"])  # 0
# GetRealeaseByArtistID
functions.append(["hasId-"])  # 0
functions.append(["hasId-", "released"])  # 0
functions.append(["hasId-", "released", "hasId"])  # 0
functions.append(["hasId-", "released", "inLanguage"])  # 0
# GetArtistsByRealeaseID
functions.append(["hasId-"])  # 0
functions.append(["hasId-", "inLanguage"])  # 0
functions.append(["hasId-", "sang-"])  # 0
functions.append(["hasId-", "produced-"])  # 0
functions.append(["hasId-", "lyricsBy"])  # 0
# GetArtistInfoByName
functions.append(["hasId"])  # 0
functions.append(["diedOnDate"])  # 0
functions.append(["bornOnDate"])  # 0
# GetCollaboratorsByID
functions.append(["hasId-"])  # 0
functions.append(["hasId-", "isMemberOf"])  # 0
functions.append(["hasId-", "isMemberOf", "hasId"])  # 0
# GetBookInfoByISBN
# functions.append(["hasISBN-"])  # 0
# functions.append(["hasISBN-", "isTitleOf"])  # 0
# functions.append(["hasISBN-", "hasId"])  # 0
# functions.append(["hasISBN-", "publishedOnDate"])  # 0
# functions.append(["hasISBN-", "wrote-"])  # 0
# functions.append(["hasISBN-", "wrote-", "hasWonPrize"])  # 0
# functions.append(["hasISBN-", "wrote-", "hasId"])  # 0
# GetRelativesByID
functions.append(["hasId-"])  # 0
functions.append(["hasId-", "hasSiblings"])  # 0
functions.append(["hasId-", "hasSiblings", "hasId"])  # 0
functions.append(["hasId-", "isMarriedTo"])  # 0
functions.append(["hasId-", "isMarriedTo", "hasId"])  # 0
functions.append(["hasId-", "hasChild"])  # 0
functions.append(["hasId-", "hasChild", "hasId"])  # 0
functions.append(["hasId-", "divorcedOn"])  # 0
functions.append(["hasId-", "marriedOn"])  # 0
# GetReleaseInfoByName
functions.append(["released-"])  # 0
functions.append(["describes-"])  # 0
functions.append(["happenedOnDate"])  # 0

# Make each function unique
print("Number functions:", len(functions))
f_temp = []
for f in functions:
    if f not in f_temp:
        f_temp.append(f)
functions = f_temp
print("Number functions:", len(functions))

for i in range(len(functions)):
    functions[i] = Function(functions[i], "f" + str(i))


i_grammar = FunctionIndexedGrammar(functions, [["b"]])

terminals = i_grammar.get_terminals()

for terminal in terminals:
    # i_grammar.update([[terminal]])
    i_grammar = FunctionIndexedGrammar(functions, [[terminal]])
    print(terminal, i_grammar.is_empty())
