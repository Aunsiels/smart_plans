class IndexedGrammar(object):
    """IndexedGrammar
    Describes the indexed grammar.
    """

    def __init__(self, rules):
        """__init__
        Initializes an indexed grammar
        :param rules: The rules of the grammar, in reduced form put into a Rule
        object
        """
        self.rules = rules
        # Precompute all non-terminals
        self.non_terminals = rules.getTerminals()
        # We cache the marked items in case of future update of the query
        self.marked = dict()
        # Initialize the marked symboles
        # Mark the identity
        for A in self.non_terminals:
            self.marked[A] = []
            temp = set()
            temp.add(A)
            self.marked[A].append(temp)
        # Mark all end symboles
        for A in self.non_terminals:
            if exists(self.rules.getRules(),
                      lambda x: x.isEndRule() and x.getLeftTerm() == A):
                self.marked[A].append(set())

    def duplication_processing(self, rule):
        """duplication_processing
        Processes a duplication rule
        :param rule: The duplication rule to process
        """
        was_modified = False
        need_stop = False
        for x in self.marked[rule.getRightTerms()[0]]:
            for y in self.marked[rule.getRightTerms()[1]]:
                temp = x.union(y)
                # Check if it was marked before
                if temp not in self.marked[rule.getLeftTerm()]:
                    was_modified = True
                    self.marked[rule.getLeftTerm()].append(temp)
                    # Stop condition, no need to continuer
                    if rule.getLeftTerm() == "S" and len(temp) == 0:
                        need_stop = True
        return (was_modified, need_stop)

    def production_process(self, rule):
        """production_process
        Processes a production rule
        :param rule: The production rule to process
        """
        was_modified = False
        # f_rules contains the consommation rules associated with
        # the current production symbol
        f_rules = self.rules.getConsommationRules().setdefault(
            rule.getProduction(), [])
        # l_rules contains the left symbol plus what is marked on
        # the right side
        l_temp = [(x.getLeft(),
                  list(self.marked[x.getRight()])) for x in f_rules]
        marked_symbols = [x.getLeft() for x in f_rules]
        # Process all combinations of consumption rule
        was_modified |= addrec(l_temp,
                               self.marked[rule.getLeftTerm()],
                               self.marked[rule.getRightTerm()])
        # End condition
        if set() in self.marked["S"]:
            return (was_modified, True)
        if rule.getRightTerm() in marked_symbols:
            for s in l_temp:
                if rule.getRightTerm() == s[0] or \
                        set() in self.marked[rule.getRightTerm()]:
                    for sc in s[1]:
                        if sc not in\
                                self.marked[rule.getLeftTerm()]:
                            was_modified = True
                            self.marked[rule.getLeftTerm()].append(
                                sc)
                            if rule.getLeftTerm() == "S" and \
                                    len(sc) == 0:
                                return (was_modified, True)
        return (was_modified, False)

    def is_empty(self, debug=True):
        """is_empty Checks whether the grammar generates a word or not"""
        # To know when no more modification are done
        was_modified = True
        # To know the number of iteration (debug)
        count = 0
        while was_modified:
            if debug:
                print("Stage ", count, " number marked : ",
                      length_marked(self.marked))
                # print_marked(self.marked)
            count += 1
            was_modified = False
            for rule in self.rules.getRules():
                # If we have a duplication rule, we mark all combinations of
                # the sets marked on the right side for the symbole on the left
                # side
                if rule.isDuplication():
                    dup_res = self.duplication_processing(rule)
                    was_modified |= dup_res[0]
                    if dup_res[1]:
                        if debug:
                            print("number marked : ",
                                  length_marked(self.marked))
                        return False
                elif rule.isProduction():
                    prod_res = self.production_process(rule)
                    if prod_res[1]:
                        if debug:
                            print("number marked : ",
                                  length_marked(self.marked))
                            # print_marked(self.marked)
                        return False
                    was_modified |= prod_res[0]
        if debug:
            print("number marked : ", length_marked(self.marked))
        return True


def exists(l, f):
    """exists
    Check whether at least an element x of l is True for f(x)
    :param l: A list of elements to test
    :param f: The checking function (takes one parameter and return a
    boolean)
    """
    for x in l:
        if f(x):
            return True
    return False


def addrec(l_sets, markedLeft, markedRight, temp=set(), temp_in=set()):
    """addrec
    Explores all possible combination of consumption rules to mark a
    production rule.
    :param l_sets: a list containing tuples (C, M) where:
        * C is a non-terminal on the left of a consumption rule
        * M is the set of the marked set for the right non-terminal in the
        production rule
    :param markedLeft: Sets which are marked for the non-terminal on the
    left of the production rule
    :param markedRight: Sets which are marked for the non-terminal on the
    right of the production rule
    :param temp: Contains the union of all sets considered up to that point
    :param temp_in: Contains the non-terminals on the left of consumption
    rules which have been considered up to that point
    :return Whether an element was actually marked
    """
    # End condition, nothing left to process
    if len(l_sets) == 0:
        # Check if at least one non-terminal was considered, then if the set
        # of non-terminals considered is marked of the right non-terminal in
        # the production rule, then if a new set is marked or not
        if len(temp_in) > 0 and temp_in in markedRight and \
                temp not in markedLeft:
            markedLeft.append(temp)
            return True
        return False
    res = False
    # For all sets which were marked for the current comsumption rule
    for s in l_sets[0][1]:
        res |= addrec(l_sets[1:], markedLeft, markedRight, temp.union(s),
                      temp_in.union({l_sets[0][0]}))
    # Here we skip the current comsumption rule
    res |= addrec(l_sets[1:], markedLeft, markedRight, temp, temp_in)
    return res


def length_marked(marked):
    """length_marked
    Gets the number of marked couples (mainly for debugging)
    :param marked: The dictionary of marked couples
    """
    res = 0
    for x in marked:
        res += len(marked[x])
    return res


def print_marked(marked):
    """print_marked
    Prints the marked couples (mainly for debugging)
    :param marked: The dictionary of marked couples
    """
    keys = sorted(marked.keys())
    for x in keys:
        print(x, marked[x])
