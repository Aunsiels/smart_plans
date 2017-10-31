from function_indexed_grammar import FunctionIndexedGrammar
from multiple_input_function import MultipleInputFunction
import sys

# Books
FUNLIBTH = True
FUNABE = False
FUNISBN1 = False
# Music
FUNLF1 = False
FUNMB1 = False
FUNMB1reduced = False
FUNLYRIC1 = False

functions = []

if FUNLIBTH:
    # FUNLIBTHGetAuthorInfoByName
    functions.append(["hasWonPrize"])
    functions.append(["hasIdAuthor"])
    functions.append(["isCitizenOf"])
    functions.append(["bornOnDate"])
    functions.append(["graduatedFrom"])
    functions.append(["hasGender"])
    functions.append(["livesIn"])
    # FUNLIBTHGetBookInfoByISBN
    functions.append(["hasISBN-"])
    functions.append(["hasISBN-", "isTitledOf"])
    functions.append(["hasISBN-", "hasIdBook"])
    functions.append(["hasISBN-", "publishedOnDate"])
    functions.append(["hasISBN-", "wrote-"])
    functions.append(["hasISBN-", "wrote-", "hasWonPrize"])
    functions.append(["hasISBN-", "wrote-", "hasIdAuthor"])
    # FUNLIBTHGetBookInfoByName
    functions.append(["hasIdBook"])
    functions.append(["isTitledOf"])
    functions.append(["publishedOnDate"])
    functions.append(["wrote-"])
    functions.append(["wrote-", "hasIdAuthor"])
    functions.append(["wrote-", "hasWonPrize"])
    # FUNLIBTHGetAuthorInfoByName
    functions.append(["hasIdAuthor"])
    functions.append(["livesIn"])
    functions.append(["bornOnDate"])
    functions.append(["graduatedFrom"])
    functions.append(["hasGender"])
    functions.append(["isCitizenOf"])
    functions.append(["hasWonPrize"])
    # FUNLIBTHGetBookInfoByID
    functions.append(["hasIdBook-"])
    functions.append(["hasIdBook-", "wrote-"])
    functions.append(["hasIdBook-", "wrote-", "hasWonPrize"])
    functions.append(["hasIdBook-", "wrote-", "hasIdAuthor"])
    functions.append(["hasIdBook-", "publishedOnDate"])
    functions.append(["hasIdBook-", "isTitledOf"])
if FUNABE:
    # FUNABEGetBookInfoByISBN
    functions.append(["hasISBN-"])
    functions.append(["hasISBN-", "wrote-"])
    functions.append(["hasISBN-", "published"])
    # FUNABEGetBookInfoByTitle
    functions.append(["hasISBN"])
    functions.append(["isTitled"])
    functions.append(["published-"])
    functions.append(["wrote-"])
    # FUNABEGetBooksByAuthorName
    functions.append(["wrote"])
    functions.append(["wrote", "isTitled"])
    functions.append(["wrote", "published-"])
    functions.append(["wrote", "wrote-"])
if FUNISBN1:
    # FUNISBN1GetBooksByAuthorID
    functions.append(["hasId-"])
    functions.append(["hasId-", "wrote"])
    functions.append(["hasId-", "wrote", "hasIdBook"])
    functions.append(["hasId-", "wrote", "isTitled"])
    functions.append(["hasId-", "wrote", "hasISBN"])
    # FUNISBN1GetBooksByName
    functions.append(["isTitled-"])
    functions.append(["isTitled-", "hasIdBook"])
    functions.append(["isTitled-", "hasISBN"])
    functions.append(["isTitled-", "wrote-"])
    functions.append(["isTitled-", "wrote-", "hasIdAuthor"])

if FUNMB1reduced:
    # FUNMB1GetArtistInfoByID
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "describes-"])
    functions.append(["hasIdArtist-", "rated"])
    functions.append(["hasIdArtist-", "diedOnDate"])
    functions.append(["hasIdArtist-", "bornOnDate"])
    # FUNMB1GetArtistInfoByName
    # functions.append(["hasIdArtist"])
    functions.append(["diedOnDate"])
    functions.append(["bornOnDate"])
    # FUNMB1GetArtistsByRealeaseID
    functions.append(["hasIdRelease-"])
    functions.append(["hasIdRelease-", "inLanguage"])
    functions.append(["hasIdRelease-", "sang-"])
    functions.append(["hasIdRelease-", "produced-"])
    functions.append(["hasIdRelease-", "lyricsBy"])
    # FUNMB1GetCollaboratorInfoById
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "isMemberOf-"])
    functions.append(["hasIdArtist-", "isMemberOf-", "hasIdArtist"])
    # FUNMB1GetCollaboratorsByID
    # functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "isMemberOf"])
    functions.append(["hasIdArtist-", "isMemberOf", "hasIdCollab"])
    # FUNMB1GetRelativesByID
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "hasSiblings"])
    functions.append(["hasIdArtist-", "hasSiblings", "hasIdSibling"])
    functions.append(["hasIdArtist-", "isMarriedTo"])
    functions.append(["hasIdArtist-", "isMarriedTo", "hasIdSpouse"])
    functions.append(["hasIdArtist-", "hasChild"])
    functions.append(["hasIdArtist-", "hasChild", "hasIdChild"])
    functions.append(["hasIdArtist-", "divorcedOn"])
    functions.append(["hasIdArtist-", "marriedOn"])
    # FUNMB1GetReleaseInfoByID
    functions.append(["hasIdRelease-"])
    functions.append(["hasIdRelease-", "inLanguage"])
    functions.append(["hasIdRelease-", "happenedIn"])
    functions.append(["hasIdRelease-", "hasTrackNumber"])
    functions.append(["hasIdRelease-", "happenedOnDate"])
    functions.append(["hasIdRelease-", "hasDiscNumber"])
    functions.append(["hasIdRelease-", "describes-"])
    functions.append(["hasIdRelease-", "released-"])
    functions.append(["hasIdRelease-", "released-", "hasIdArtist"])
    # FUNMB1GetReleaseInfoByTitle
    # functions.append(["hasIdRelease"])
    functions.append(["inLanguage"])
    functions.append(["released-"])
    # FUNMB1GetRealeaseByArtistID
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "released"])
    functions.append(["hasIdArtist-", "released", "hasIdRelease"])
    functions.append(["hasIdArtist-", "released", "inLanguage"])
    # FUNMB1GetTrackInfoByID
    functions.append(["hasIdTrack-"])
    functions.append(["hasIdTrack-", "hasDuration"])
    functions.append(["hasIdTrack-", "sang-"])
    functions.append(["hasIdTrack-", "hasValue"])
    functions.append(["hasIdTrack-", "isMemberOf"])
    # FUNMB1GetTrackInfoByName
    # functions.append(["hasIdTrack"])
    functions.append(["isMemberOf"])
    functions.append(["sang-"])
    functions.append(["hasValue"])
    functions.append(["hasDuration"])
    # FUNMB1GetTracksByReleaseID
    functions.append(["hasIdRelease-"])
    functions.append(["hasIdRelease-", "inLanguage"])
    functions.append(["hasIdRelease-", "isMemberOf-"])
    functions.append(["hasIdRelease-", "isMemberOf-", "hasDuration"])
    functions.append(["hasIdRelease-", "isMemberOf-", "hasIdTrack"])
    # FUNMB1GetTracksByArtistId
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "sang"])
if FUNMB1:
    # FUNMB1GetArtistInfoByID
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "describes-"])
    functions.append(["hasIdArtist-", "rated"])
    functions.append(["hasIdArtist-", "diedOnDate"])
    functions.append(["hasIdArtist-", "bornOnDate"])
    # FUNMB1GetCollaboratorInfoById
    functions.append(["hasIdCollab-"])
    functions.append(["hasIdCollab-", "isMemberOf-"])
    functions.append(["hasIdCollab-", "isMemberOf-", "hasIdArtist"])
    # FUNMB1GetCollaboratorsByID
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "isMemberOf"])
    functions.append(["hasIdArtist-", "isMemberOf", "hasIdCollab"])
    # FUNMB1GetTracksByArtistId
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "sang"])
    # FUNMB1GetTrackInfoByName
    functions.append(["hasIdTrack"])
    functions.append(["isMemberOf"])
    functions.append(["sang-"])
    functions.append(["hasValue"])
    functions.append(["hasDuration"])
    # FUNMB1GetTracksByReleaseID
    functions.append(["hasIdRelease-"])
    functions.append(["hasIdRelease-", "inLanguage"])
    functions.append(["hasIdRelease-", "isMemberOf-"])
    functions.append(["hasIdRelease-", "isMemberOf-", "hasDuration"])
    functions.append(["hasIdRelease-", "isMemberOf-", "hasIdTrack"])
    # FUNMB1GetTrackInfoByID
    functions.append(["hasIdTrack-"])
    functions.append(["hasIdTrack-", "hasDuration"])
    functions.append(["hasIdTrack-", "isMemberOf"])
    functions.append(["hasIdTrack-", "sang-"])
    functions.append(["hasIdTrack-", "hasValue"])
    # FUNMB1GetRealeaseByArtistID
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "released"])
    functions.append(["hasIdArtist-", "released", "hasIdRelease"])
    functions.append(["hasIdArtist-", "released", "inLanguage"])
    # FUNMB1GetArtistsByRealeaseID
    functions.append(["hasIdRelease-"])
    functions.append(["hasIdRelease-", "inLanguage"])
    functions.append(["hasIdRelease-", "sang-"])
    functions.append(["hasIdRelease-", "produced-"])
    functions.append(["hasIdRelease-", "lyricsBy"])
    # FUNMB1GetArtistInfoByName
    functions.append(["hasIdArtist"])
    functions.append(["diedOnDate"])
    functions.append(["bornOnDate"])
    # FUNMB1GetRelativesByID
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "hasSiblings"])
    functions.append(["hasIdArtist-", "hasSiblings", "hasIdSibling"])
    functions.append(["hasIdArtist-", "isMarriedTo"])
    functions.append(["hasIdArtist-", "isMarriedTo", "hasIdSpouse"])
    functions.append(["hasIdArtist-", "hasChild"])
    functions.append(["hasIdArtist-", "hasChild", "hasIdChild"])
    functions.append(["hasIdArtist-", "divorcedOn"])
    functions.append(["hasIdArtist-", "marriedOn"])
if FUNLYRIC1:
    # FUNMB1GetRealeaseByArtistID
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "released", "hasIdRelease"])
    functions.append(["hasIdArtist-", "released", "inLanguage"])
    # FUNLYRIC1GetLyricsInfoByArtistTrackName
    functions.append(["hasLyrics"])
    functions.append(["hasLyrics", "describes-"])
    # FUNMB1GetArtistInfoByName
    functions.append(["hasIdArtist"])
if FUNLF1:
    # FUNLF1GetReleaseInfoByName
    functions.append(["released-"])
    functions.append(["describes-"])
    functions.append(["happenedOnDate"])
    # FUNLF1GetTrackInfoById
    functions.append(["hasIdTrack-"])
    functions.append(["hasIdTrack-", "isMemberOf"])
    functions.append(["hasIdTrack-", "isMemberOf", "hasIdRelease"])
    functions.append(["hasIdTrack-", "describes-"])
    functions.append(["hasIdTrack-", "hasDuration"])
    functions.append(["hasIdTrack-", "sang-"])
    functions.append(["hasIdTrack-", "sang-", "hasIdArtist"])
    # FUNLF1GetArtistInfoByName
    functions.append(["hasIdArtist"])
    functions.append(["describes-"])
    # FUNLF1GetReleaseInfoByID
    functions.append(["hasIdRelease-"])
    functions.append(["hasIdRelease-", "released-"])
    functions.append(["hasIdRelease-", "describes-"])
    functions.append(["hasIdRelease-", "happenedOnDate"])
    # FUNLF1GetTrackInfoByName
    # functions.append(["sang-"])
    functions.append(["describes-"])
    # FUNF1GetArtistInfoByID
    functions.append(["hasIdArtist-"])
    functions.append(["describes-"])

# Make each function unique
# print("Number functions:", len(functions))
f_temp = []
for f in functions:
    if f not in f_temp:
        f_temp.append(f)
functions = f_temp

for i in range(len(functions)):
    functions[i] = MultipleInputFunction(functions[i], "f" + str(i), 1)

# Multiple Input functions
if FUNABE:
    functions.append(MultipleInputFunction(["wrote", "hasISBN"], "f", 2))
    functions.append(MultipleInputFunction(["wrote", "published"], "f", 2))
if FUNLF1:
    # functions.append(MultipleInputFunction(["released", "hasIdRelease"],
    #                                        "f", 2))
    functions.append(MultipleInputFunction(["released", "describes-"],
                                           "f", 2))
    functions.append(MultipleInputFunction(["released", "happenedOnDate"],
                                           "f", 2))
    functions.append(MultipleInputFunction(["sang", "hasIdTrack"],
                                           "f", 2))
    functions.append(MultipleInputFunction(["sang", "hasDuration"],
                                           "f", 2))
    functions.append(MultipleInputFunction(["sang", "isMemberOf"],
                                           "f", 2))
    functions.append(MultipleInputFunction(["sang", "isMemberOf", "hasIdAlbum"],
                                           "f", 2))
    functions.append(MultipleInputFunction(["sang", "describes-"],
                                           "f", 2))
    functions.append(MultipleInputFunction(["sang-", "hasIdArtist"],
                                           "f", 2))

print("Number functions:", len(functions))

for f in functions:
    print(f)

i_grammar = FunctionIndexedGrammar(functions, [[""]])

terminals = i_grammar.get_terminals()
terminals.remove("epsilon")
terminals.remove("end")
terminals.remove("query")
terminals = list(filter(lambda x: "_IN" not in x, terminals))

n_reachable = 0

for terminal in terminals:
    # i_grammar.update([[terminal]])
    i_grammar = FunctionIndexedGrammar(functions, [[terminal]])
    if i_grammar.is_empty():
        print(terminal, "Cannot be reached")
    else:
        print(terminal, "Can be reached")
        n_reachable += 1
    sys.stdout.flush()

if n_reachable == 0:
    print("No terminal was reachable")
else:
    print(str(n_reachable * 100.0 / float(len(terminals))) +
          "% terminals reachable")
