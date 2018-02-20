# How To

## Smart Plan existence

Run the GUI by using the command:

``` bash
python3 interface.py
```

Then, you can edit the query and the functions. The query is of the form r1, r2, ..., rn. The function are of the form f :- r1, r2, ..., rn for the linear ones (prolog notation). For tree function, the notation is similar to the Newick format inverted where all nodes are named [Wikipidia Article](https://en.wikipedia.org/wiki/Newick_format). The nodes are separated by ";" whereas the relations are separated with ",". For example:
f :- ((f;g)a,b;e)c,d.


## Prolog

Currently not working

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
