from function_indexed_grammar import FunctionIndexedGrammar
from function import Function

functions = []

functions.append(["c-"])  # 0
functions.append(["c", "c", "b"])  # 1
functions.append(["a", "d"])  # 2
functions.append(["d-", "c-"])  # 3
functions.append(["c"])  # 4
functions.append(["a-", "b"])  # 5
functions.append(["d-"])  # 6
functions.append(["d-", "a-", "b"])  # 7
functions.append(["b"])  # 8
functions.append(["a"])  # 9
functions.append(["d"])  # 10
functions.append(["d", "b"])  # 11

all_relations = ["c", "b", "cm", "bm", "a", "am", "d", "dm", "e", "em"]

counter = 0

for i in range(len(functions)):
    functions[i] = Function(functions[i], "f" + str(i))

print("Test -1")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [8]], "b")
assert not i_grammar.is_empty(), "Error-1"

print("Test 0")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [9, 5]], "b")
assert not i_grammar.is_empty(), "Error0"

print("Test 1")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [0, 1]], "b")
assert not i_grammar.is_empty(), "Error1"

print("Test 2")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [0]], "b")
assert i_grammar.is_empty(), "Error2"

print("Test 3")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [1]], "b")
assert i_grammar.is_empty(), "Error3"

print("Test 4")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [2, 7]], "b")
assert not i_grammar.is_empty(), "Error4"

print("Test 5")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [9, 10, 7]], "b")
assert not i_grammar.is_empty(), "Error5"

print("Test 6")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [6, 11]], "b")
assert not i_grammar.is_empty(), "Error6"

print("Test 7")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [2, 6, 5]], "b")
assert not i_grammar.is_empty(), "Error7"

print("Test 8")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [2, 3, 4, 5]],
                                   "b")
assert not i_grammar.is_empty(), "Error8"

print("Test 9")

i_grammar.update("b")
assert not i_grammar.is_empty(), "Error9"

print("Test 10")

i_grammar.update("c")
assert not i_grammar.is_empty(), "Error10"

print("Test 11")

i_grammar.update("e")
assert i_grammar.is_empty(), "Error11"
