# How To

## Function files

You can create function by putting them into a file. The synthax is similar to prolog. For example, the function f1 = a b c- can be written.

f1 :- a, b, c-.

Other examples can be found in the examples directory.

## Query file

A query file is simply the relations in the query separated by a comma

## Run the program

``` bash
sh run.sh maxDepth functionFile query_file
```

For example:

``` bash
sh run.sh 10 examples/example2.fct examples/query.txt
sh run.sh 10 examples/example4.fct examples/query2.txt
```
