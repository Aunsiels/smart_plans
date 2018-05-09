# How To

## Prerequisites

python3, networkx, tkinter, graphviz

## Interface

### Running the Interface

Run the GUI by using the command:

``` bash
./interface.sh
```

### Function Definitions

Then, you can edit the query and the functions. The query is of the form r1, r2, ..., rn. The functions are of the form f :- r1, r2, ..., rn for the linear ones (prolog notation). For tree function, the notation is similar to the Newick format where all nodes are named [Wikipidia Article](https://en.wikipedia.org/wiki/Newick_format). The nodes are separated by ";" whereas the relations are separated with ",". For example:

f1 :- ((f;g)a,b;e)c,d.

### Function Visualization

To visualize function, go to "Run > Show Functions" or press &lt;F2&gt;.

### Existence of Smart Plan

To check whether a smart plan can be built with the given functions for the query, go to "Run > Existence" or press &lt;F1&gt;.

### Find a Plan

To get one of the smart plan out of the functions, go to "Run > Prolog" or press &lt;F3&gt;.

### Get the Rules in the Grammar

To get the rules used in the grammar and which are given to Prolog, go to "Run > Show Prolog Rules" or press &lt;F4&gt;.

## Other Informations

### Function files

You can create function by putting them into a file. The synthax is similar to prolog. For example, the function f1 = a b c- can be written.

f1 :- a, b, c-.

Other examples can be found in the examples directory.

### Query file

A query file is simply the relations in the query separated by a comma

### Run the program

``` bash
sh run.sh maxDepth functionFile query_file
```

For example:

``` bash
sh run.sh 10 examples/example2.fct examples/query.txt
sh run.sh 10 examples/example4.fct examples/query2.txt
```
