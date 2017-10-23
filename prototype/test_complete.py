from function_indexed_grammar import FunctionIndexedGrammar
from function import Function
import sys

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
functions.append(["hasIdCollab-"])  # 0
functions.append(["hasIdCollab-", "isMemberOf-"])  # 0
functions.append(["hasIdCollab-", "isMemberOf-", "hasIdArtist"])  # 0
# GetLyricsInfoByArtistTrackName
functions.append(["hasLyrics"])  # 0
functions.append(["hasLyrics", "describes-"])  # 0
# GetBookInfoByISBN
# functions.append(["hasISBN-"])  # 0
# functions.append(["hasISBN-", "wrote-"])  # 0
# functions.append(["hasISBN-", "published"])  # 0
# GetTracksByArtistId
functions.append(["hasIdArtist-"])  # 0
functions.append(["hasIdArtist-", "sang"])  # 0
# GetTrackInfoByName
functions.append(["hasIdTrack"])  # 0
functions.append(["isMemberOf"])  # 0
functions.append(["sang-"])  # 0
functions.append(["hasValue"])  # 0
functions.append(["hasDuration"])  # 0
# GetTracksByReleaseID
functions.append(["hasIdRelease-"])  # 0
functions.append(["hasIdRelease-", "inLanguage"])  # 0
functions.append(["hasIdRelease-", "isMemberOf-"])  # 0
functions.append(["hasIdRelease-", "isMemberOf-", "hasDuration"])  # 0
functions.append(["hasIdRelease-", "isMemberOf-", "hasIdTrack"])  # 0
# GetTrackInfoByID
functions.append(["hasIdTrack-"])  # 0
functions.append(["hasIdTrack-", "hasDuration"])  # 0
functions.append(["hasIdTrack-", "isMemberOf"])  # 0
functions.append(["hasIdTrack-", "sang-"])  # 0
functions.append(["hasIdTrack-", "hasValue"])  # 0
# GetRealeaseByArtistID
functions.append(["hasIdArtist-"])  # 0
functions.append(["hasIdArtist-", "released"])  # 0
functions.append(["hasIdArtist-", "released", "hasIdRelease"])  # 0
functions.append(["hasIdArtist-", "released", "inLanguage"])  # 0
# GetArtistsByRealeaseID
functions.append(["hasIdRelease-"])  # 0
functions.append(["hasIdRelease-", "inLanguage"])  # 0
functions.append(["hasIdRelease-", "sang-"])  # 0
functions.append(["hasIdRelease-", "produced-"])  # 0
functions.append(["hasIdRelease-", "lyricsBy"])  # 0
# GetArtistInfoByName
functions.append(["hasIdArtist"])  # 0
functions.append(["diedOnDate"])  # 0
functions.append(["bornOnDate"])  # 0
# GetCollaboratorsByID
functions.append(["hasIdArtist-"])  # 0
functions.append(["hasIdArtist-", "isMemberOf"])  # 0
functions.append(["hasIdArtist-", "isMemberOf", "hasIdCollab"])  # 0
# GetBookInfoByISBN
# functions.append(["hasISBN-"])  # 0
# functions.append(["hasISBN-", "isTitleOf"])  # 0
# functions.append(["hasISBN-", "hasId"])  # 0
# functions.append(["hasISBN-", "publishedOnDate"])  # 0
# functions.append(["hasISBN-", "wrote-"])  # 0
# functions.append(["hasISBN-", "wrote-", "hasWonPrize"])  # 0
# functions.append(["hasISBN-", "wrote-", "hasId"])  # 0
# GetRelativesByID
functions.append(["hasIdArtist-"])  # 0
functions.append(["hasIdArtist-", "hasSiblings"])  # 0
functions.append(["hasIdArtist-", "hasSiblings", "hasIdSibling"])  # 0
functions.append(["hasIdArtist-", "isMarriedTo"])  # 0
functions.append(["hasIdArtist-", "isMarriedTo", "hasIdSpouse"])  # 0
functions.append(["hasIdArtist-", "hasChild"])  # 0
functions.append(["hasIdArtist-", "hasChild", "hasIdChild"])  # 0
functions.append(["hasIdArtist-", "divorcedOn"])  # 0
functions.append(["hasIdArtist-", "marriedOn"])  # 0
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

i_grammar = FunctionIndexedGrammar(functions, [[""]])

terminals = i_grammar.get_terminals()
terminals.remove("epsilon")
terminals.remove("end")
terminals.remove("query")

for terminal in terminals:
    # i_grammar.update([[terminal]])
    print(terminal)
    i_grammar = FunctionIndexedGrammar(functions, [[terminal]])
    print(terminal, i_grammar.is_empty())
    sys.stdout.flush()
