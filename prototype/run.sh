#!/bin/bash

# max_depth function_file query_file

mkdir -p tmp

python main.py $1 $2 $3 > tmp/temp_rules.pl && swipl -f tmp/temp_rules.pl -q main

echo ""
