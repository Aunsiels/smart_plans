"""
Testing of linear function, Multiple input functions, and equivalence rules
"""


from function_indexed_grammar import FunctionIndexedGrammar
from multiple_input_function import MultipleInputFunction

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
functions.append(["x-", "x-"])  # 12
functions.append(["j", "x"])  # 13
functions.append(["a", "b"])  # 14
functions.append(["c", "d", "q"])  # 15
functions.append(["d"])  # 16
functions.append(["d-", "b-", "e-"])  # 17
functions.append(["e", "c-"])  # 18
functions.append(["c", "b", "a"])  # 19
functions.append(["c", "c"])  # 20
functions.append(["b", "a", "q"])  # 21
functions.append(["a-", "c", "d"])  # 22
functions.append(["d-", "c-", "b-"])  # 23
functions.append(["b-", "a-"])  # 24
functions.append(["a-"])  # 25
functions.append(["c-", "b-", "a-"])  # 26
functions.append(["b-", "a-", "q"])  # 27

mifunctions = []

mifunctions.append(["d-", "c-", "b-"])  # 0
mifunctions.append(["a-", "c", "d"])  # 1

counter = 0

for i in range(len(functions)):
    functions[i] = MultipleInputFunction(functions[i], "f" + str(i), 1)

for i in range(len(mifunctions)):
    mifunctions[i] = MultipleInputFunction(mifunctions[i],
                                           "f" + str(i + len(functions)), 2)

mifunctions.append(MultipleInputFunction(["a", "b", "c"], "f",
                                         [1]))  # 2
mifunctions.append(MultipleInputFunction(["a", "b", "c", "d"], "f",
                                         [1, 2]))  # 3
mifunctions.append(MultipleInputFunction(["a-"], "f",
                                         2))  # 4
mifunctions.append(MultipleInputFunction(["a", "b"], "f",
                                         2))  # 5



print("Test -1")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [8]], [["b"]])
assert not i_grammar.is_empty(), "Error-1"

print("Test 0")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [9, 5]], [["b"]])
assert not i_grammar.is_empty(), "Error0"

print("Test 1")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [0, 1]], [["b"]])
assert not i_grammar.is_empty(), "Error1"

print("Test 2")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [0]], [["b"]])
assert i_grammar.is_empty(), "Error2"

print("Test 3")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [1]], [["b"]])
assert i_grammar.is_empty(), "Error3"

print("Test 4")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [2, 7]], [["b"]])
assert not i_grammar.is_empty(), "Error4"

print("Test 5")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [9, 10, 7]], [["b"]])
assert not i_grammar.is_empty(), "Error5"

print("Test 6")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [6, 11]], [["b"]])
assert not i_grammar.is_empty(), "Error6"

print("Test 7")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [2, 6, 5]], [["b"]])
assert not i_grammar.is_empty(), "Error7"

print("Test 8")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [2, 3, 4, 5]],
                                   [["b"]])
assert not i_grammar.is_empty(), "Error8"

print("Test 9")

i_grammar.update([["b"]])
assert not i_grammar.is_empty(), "Error9"

print("Test 10")

i_grammar.update([["c"]])
assert not i_grammar.is_empty(), "Error10"

print("Test 11")

i_grammar.update([["e"]])
assert i_grammar.is_empty(), "Error11"

print("Test 12")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [12, 13]],
                                   [["xm"]])
# Empty without subfunctions
assert i_grammar.is_empty(), "Error12"

print("Test 14")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [14, 15]],
                                   [["q"]])

assert i_grammar.is_empty(), "Error14"

print("Test 15")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [16, 17, 18, 19]],
                                   [["a"]])
assert not i_grammar.is_empty(), "Error15"

print("Test 16")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [0, 19]],
                                   [["b", "a"]])
assert not i_grammar.is_empty(), "Error16"

print("Test 17")

i_grammar.update([["a", "b"]])
assert i_grammar.is_empty(), "Error17"

print("Test 18")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [20]],
                                   [["c"], ["c", "c"]])
assert not i_grammar.is_empty(), "Error18"

print("Test 19")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [20]],
                                   [["c"], ["query", "c"]])
assert not i_grammar.is_empty(), "Error19"

print("Test 20")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [21, 22]] +
                                   [mifunctions[x] for x in [0]],
                                   [["q"]])
assert not i_grammar.is_empty(), "Error20"

print("Test 21")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [21, 23]] +
                                   [mifunctions[x] for x in [1]],
                                   [["q"]])
assert i_grammar.is_empty(), "Error21"

print("Test 22")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [24]] +
                                   [mifunctions[x] for x in [2]],
                                   [["c"]])
assert not i_grammar.is_empty(), "Error22"

print("Test 23")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [25]] +
                                   [mifunctions[x] for x in [2]],
                                   [["b", "c"]])
assert i_grammar.is_empty(), "Error23"

print("Test 24")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [26]] +
                                   [mifunctions[x] for x in [3]],
                                   [["d"]])
assert not i_grammar.is_empty(), "Error24"

print("Test 25")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [24]] +
                                   [mifunctions[x] for x in [3]],
                                   [["c", "d"]])
assert i_grammar.is_empty(), "Error25"

print("Test 26")

i_grammar = FunctionIndexedGrammar([functions[x] for x in [9, 27]] +
                                   [mifunctions[x] for x in [4, 5]],
                                   [["q"]])
assert not i_grammar.is_empty(), "Error26"
