from function import Function
import re
import sys


def read_function(line):
    """read_function
    Read a function from a string. It must be of the form:
        f :- r1, r2, ..., rn.
    :param line: The string representing the function
    """
    l0 = line.split(":-")
    if len(l0) != 2:
        sys.exit("Wrong line: " + line)
    f_name = re.sub("\s+", ",", l0[0].strip())
    relations = [re.sub("\s+", ",", s.strip())
                 for s in re.sub("\.", "", l0[1]).split(",")]
    if len(relations) == 0:
        sys.exit("No relation: " + line)
    return Function(relations, f_name)


def main():
    """main
    Prepares the functions to input to prolog. Its takes 3 arguments:
        * The maximum depth of the search in prolog
        * A file containing all the functions, on separated lines
        * A file containing the query, on a single line
    """
    if len(sys.argv) != 4:
        sys.exit("Correct usage: python main.py max_depth function_file query")

    max_depth = int(sys.argv[1])
    # Read all functions
    functions = []
    with open(sys.argv[2]) as f:
        for line in f:
            functions.append(read_function(line))

    # Stop rules
    print("p([], _, []).")
    print("p(_, Counter, _) :- Counter =< 0, !, fail.")

    # Produce all the rules from the function
    for f in functions:
        print("\n".join(f.generate_left_rules()))
        print("\n".join(f.generate_right_rules()))

    # Read the query
    with open(sys.argv[3]) as f:
        query = ",".join([re.sub("-", "", r) + "m" * (r.count("-") % 2)
                          for r in [re.sub("\s+", ",", x.strip())
                                    for x in f.readline().split(",")]])

    # Initialization rules
    print("q(X) :- p([" + query + "], X, L), print(L).")
    print("q(X) :- X < " + str(max_depth) + ", q(X + 1).")
    print("q(_).")
    # To start automatically the program in prolog
    print(":- initialization main.")
    print("main :- q(1), halt(0).")


main()
