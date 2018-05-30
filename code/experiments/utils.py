"""
Some functions which are often useful
"""


from consommation_rule import ConsommationRule
from production_rule import ProductionRule
from duplication_rule import DuplicationRule
from end_rule import EndRule
from rules import Rules
from indexed_grammar import IndexedGrammar
from nft import NFT
from collections import Counter


def unstack(u_relations, all_relations, counter, start, end):
    """unstack
    Unstack the given relation from the stack by using reduced forms
    :param u_relations: The relations to unstack
    :param all_relations: All the relations used
    :param counter: Counter to avoid collision
    :param start: the starting non-terminal
    :param end: the ending non-terminal
    """
    rules = []
    if len(u_relations) != 0:
        rules.append(DuplicationRule(start,
                                     "T",
                                     "C" + str(counter)))
    else:
        rules.append(DuplicationRule(start,
                                     "T",
                                     end))
    temp_counter = counter
    if len(u_relations) > 1:
        rules.append(ConsommationRule(u_relations[0],
                                      "C" + str(counter),
                                      "C" + str(counter + 1)))
        counter += 1
    elif len(u_relations) == 1:
        rules.append(ConsommationRule(u_relations[0],
                                      "C" + str(counter),
                                      end))
    for x in range(1, len(u_relations) - 1):
        rules.append(ConsommationRule(u_relations[x],
                                      "C" + str(counter),
                                      "C" + str(counter + 1)))
        counter += 1
    if len(u_relations) > 1:
        rules.append(ConsommationRule(u_relations[-1],
                                      "C" + str(counter),
                                      end))
    for x in range(len(all_relations)):
        temp_counter += 1
    counter = max(temp_counter, counter)
    counter += 1
    return (rules, counter)


def stack(s_relations, counter, start, end):
    """stack
    Stack the given relations on the stack using reduced rules.
    :param s_relations: The relations to stack
    :param counter: The counter to avoid collisions
    :param start: The starting non-terminal
    :param end: The ending non-terminal
    """
    rules = []
    if len(s_relations) == 0:
        rules.append(DuplicationRule(start,
                                     "T",
                                     end))
    elif len(s_relations) == 1:
        rules.append(ProductionRule(start,
                                    end,
                                    s_relations[0]))
    else:
        rules.append(ProductionRule(start,
                                    "A" + str(counter),
                                    s_relations[0]))
    for x in range(1, len(s_relations) - 1):
        rules.append(ProductionRule("A" + str(counter),
                                    "A" + str(counter + 1),
                                    s_relations[x]))
        counter += 1
    if len(s_relations) > 1:
        rules.append(ProductionRule("A" + str(counter),
                                    end,
                                    s_relations[-1]))
    counter += 1
    return (rules, counter)


def dangie_fsm(functions):
    from fsm import FSM
    fsm = FSM()
    for function in functions:
        fsm = function.add_to_fsm(fsm)
    fsm = fsm.make_dangie_ready()
    return fsm

def inverse(relation, op="m"):
    if relation[-1] == op:
        return relation[:-1]
    else:
        return relation + op

def inverse_path(path):
    if type(path) == str:
        path = path.split(" ")
    return " ".join(map(lambda x: inverse(x, "-"), path))

def get_ISWC_grammar(relations, query):
    rules = []
    rules.append(EndRule("T", "epsilon"))
    rules.append(ProductionRule("S", "Finit", "end"))
    rules.append(ProductionRule("Finit", "F", query))
    for relation in relations:
        rules.append(DuplicationRule("F", relation, "F" + relation))
        rules.append(EndRule(relation, relation))
        rules.append(ProductionRule("F" + relation, "F", relation))
        rules.append(ConsommationRule(relation, "B", "Btemp" + relation))
        rules.append(DuplicationRule("Btemp" + relation,
                                     "Lleft" + relation,
                                     "B"))
        rules.append(DuplicationRule("Lleft", "L" + relation, relation))
        rules.append(ProductionRule("L" + relation, "L", relation))
        rules.append(ConsommationRule(relation, "L", "Ltemp" + relation))
        rules.append(DuplicationRule("Ltemp" + relation,
                                     "Lleft" + relation,
                                     "Lright" + relation))
        rules.append(DuplicationRule("Lleft" + relation,
                                     inverse(relation),
                                     "L"))
        rules.append(DuplicationRule("Lright" + relation,
                                     relation,
                                     "L" + relation))
    rules.append(EndRule("L", "epsilon"))
    rules.append(ConsommationRule("end", "B", "T"))
    rules.append(DuplicationRule("F", "B", "T"))
    rules = Rules(rules)
    return IndexedGrammar(rules)


def intersect(i_grammar, functions):
    nft = NFT()
    for function in functions:
        nft.add_function(function)
    i_grammar = nft.intersect_indexed_grammar(i_grammar)
    print(i_grammar.rules.get_length(), "rules")
    return i_grammar


def clean_rules(i_grammar):
    rules = i_grammar.rules
    print(rules.get_length(), "rules before")
    non_terminals = rules.getNonTerminalsList()
    prev_size = -1
    while len(non_terminals) != prev_size:
        prev_size = len(non_terminals)
        counter = Counter(non_terminals)
        to_remove = set()
        for key in counter:
            if counter[key] == 1 and key != "S":
                to_remove.add(key)
        new_rules = []
        for rule in rules.getRules():
            nts = rule.getNonTerminals()
            if any([nt in to_remove for nt in nts]):
                continue
            new_rules.append(rule)
        for rules_temp in rules.getConsommationRules().values():
            for rule in rules_temp:
                nts = rule.getNonTerminals()
                if any([nt in to_remove for nt in nts]):
                    continue
                new_rules.append(rule)
        rules = Rules(new_rules)
        non_terminals = rules.getNonTerminalsList()
    print(rules.get_length(), "rules after")
    return IndexedGrammar(rules)


def filter_clusters(i_grammar):
    rules = i_grammar.rules
    print(rules.get_length(), "rules before")
    clusters = []
    for temp_rule in rules.consommationRules.values():
        for rule in temp_rule:
            nts = rule.getNonTerminals()
            new_clusters = []
            pos_cluster = nts
            for cluster in clusters:
                if any([nt in cluster for nt in nts]):
                    pos_cluster += cluster
                else:
                    new_clusters.append(cluster)
            new_clusters.append(list(set(pos_cluster)))
            clusters = new_clusters
    for rule in rules.getRules():
        nts = rule.getNonTerminals()
        new_clusters = []
        pos_cluster = nts
        for cluster in clusters:
            if any([nt in cluster for nt in nts]):
                pos_cluster += cluster
            else:
                new_clusters.append(cluster)
        new_clusters.append(list(set(pos_cluster)))
        clusters = new_clusters
    good_cluster = []
    for cluster in clusters:
        if "S" in cluster:
            good_cluster = cluster
            break
    new_rules = []
    for temp_rule in rules.consommationRules.values():
        for rule in temp_rule:
            if rule.getNonTerminals()[0] in good_cluster:
                new_rules.append(rule)
    for rule in rules.getRules():
        if rule.getNonTerminals()[0] in good_cluster:
            new_rules.append(rule)
    rules = Rules(new_rules)
    print(rules.get_length(), "rules before")
    return IndexedGrammar(rules)


def get_translated_rule(rule, translator):
    if rule.isDuplication():
        return DuplicationRule(translator[rule.getLeftTerm()],
                               translator[rule.getRightTerms()[0]],
                               translator[rule.getRightTerms()[1]])
    if rule.isEndRule():
        return EndRule(translator[rule.getLeftTerm()],
                       rule.getRightTerm())
    if rule.isProduction():
        return ProductionRule(translator[rule.getLeftTerm()],
                              translator[rule.getRightTerm()],
                              rule.getProduction())
    if rule.isConsommation():
        return ConsommationRule(rule.getF(),
                                translator[rule.getLeftTerm()],
                                translator[rule.getRight()])


def rename_non_terminals(i_grammar):
    rules = i_grammar.rules
    non_terminals = rules.getNonTerminals()
    pos = 0
    translator = dict()
    for nt in non_terminals:
        if nt == "S":
            translator[nt] = nt
        else:
            translator[nt] = str(pos)
            pos += 1
    new_rules = []
    for rule in rules.getRules():
        new_rules.append(get_translated_rule(rule, translator))
    for temp_rule in rules.consommationRules.values():
        for rule in temp_rule:
            new_rules.append(get_translated_rule(rule, translator))
    return IndexedGrammar(Rules(new_rules))


def make_DFS(functions, relation, weak=True):
    from state import State
    from backward_state import BackwardState
    from forward_state import ForwardState
    from backward_path import BackwardPath
    # Compute the maximum size
    maxi = -1
    for f in functions:
        maxi = max(maxi, f.n_relations())
    # Create initial states
    states = []
    visited = set()
    for f in functions:
        f_l = f.to_list()
        # Weak
        if weak:
            if f_l[0] == relation:
                states.append((State(ForwardState(f_l[1:]),
                                     BackwardState([])), []))
                visited.add(states[-1][0])
                # Initial Kinks starts
                for i in range(2, len(f_l)):
                    f_left = f_l[:i]
                    f_right = f_l[i:]
                    f_left_str = " ".join(f_left[1:])
                    f_right_str = " ".join(map(lambda x: inverse(x, "-"),
                                               f_right[::-1]))
                    if starts_with(f_left_str, f_right_str):
                        states.append((State(ForwardState(f_left_str),
                                             BackwardState([
                                             BackwardPath(f_right_str, "b")
                                             ])), []))
                        visited.add(states[-1][0])

        if f_l[-1] == relation:
            states.append((State(ForwardState(""), BackwardState(
                [BackwardPath(f_l[-2::-1], "b")])), []))
            visited.add(states[-1][0])
            # Initial Kinks starts
            for i in range(1, len(f_l) - 1):
                f_left = f_l[:i]
                f_right = f_l[i:]
                f_left_str = " ".join(f_left)
                f_right_str = " ".join(map(lambda x: inverse(x, "-"),
                                           f_right[:-1][::-1]))
                if starts_with(f_left_str, f_right_str):
                    states.append((State(ForwardState(f_left_str),
                                         BackwardState([
                                         BackwardPath(f_right_str, "b")
                                         ])), []))
                    visited.add(states[-1][0])

    # Explore
    # print("INITIAL")
    # print(states)
    while states:
        state_temp = states.pop()
        state = state_temp[0]
        prev = state_temp[1]
        # print(states)
        # print(state, len(states))
        if state.is_end():
            # print(prev)
            return True
        next_states = state.get_next_states(functions, maxi)
        for s_temp in next_states:
            if s_temp not in visited:
                visited.add(s_temp)
                states.append((s_temp, prev[:] + [state]))
    return False


def starts_with(f_str, cp):
    if len(f_str) == 0 or len(cp) == 0:
        return True
    if len(f_str) > len(cp):
        return f_str[len(cp)] == " " and f_str[:len(cp)] == cp
    elif len(f_str) < len(cp):
        return cp[len(f_str)] == " " and cp[:len(f_str)] == f_str
    else:
        return cp == f_str


def get_sub_functions(functions):
    from function import Function
    res = []
    for function in functions:
        if isinstance(function, Function):
            res += function.get_sub_functions()
    return res
