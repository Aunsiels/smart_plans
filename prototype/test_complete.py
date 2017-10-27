from function_indexed_grammar import FunctionIndexedGrammar
from function import Function
import sys

# Books
FUNLIBTH = False
FUNABE = False
FUNISBN1 = False
# Music
FUNLF1 = False
FUNMB1 = False
FUNMB1reduced = True
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
    # FUNMB1GetCollaboratorInfoById
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "isMemberOf-"])
    functions.append(["hasIdArtist-", "isMemberOf-", "hasIdArtist"])
    # FUNMB1GetRealeaseByArtistID
    functions.append(["hasIdArtist-"])
    functions.append(["hasIdArtist-", "released"])
    functions.append(["hasIdArtist-", "released", "hasIdRelease"])
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
if FUNMB1:
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
    functions.append(["sang-"])
    functions.append(["describes-"])
    # FUNF1GetArtistInfoByID
    functions.append(["hasIdArtist-"])
    functions.append(["describes-"])

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
    print(functions[i])

i_grammar = FunctionIndexedGrammar(functions, [[""]])

terminals = i_grammar.get_terminals()
terminals.remove("epsilon")
terminals.remove("end")
terminals.remove("query")

for terminal in terminals:
    # i_grammar.update([[terminal]])
    i_grammar = FunctionIndexedGrammar(functions, [[terminal]])
    if i_grammar.is_empty():
        print(terminal, "Cannot be reached")
    else:
        print(terminal, "Can be reached")
    sys.stdout.flush()
