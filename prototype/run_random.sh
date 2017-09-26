#!/bin/bash

# Parameters max_depth n_relations n_functions max_size_functions

mkdir -p data

start_time=$(($(date +%s%N)/1000000))

mkdir -p tmp

python3 function_generator.py $2 $3 $4 tmp/functions$1-$2-$3-$4.fct tmp/query$1-$2-$3-$4.txt

RESULT=$(python3 main.py $1 tmp/functions$1-$2-$3-$4.fct tmp/query$1-$2-$3-$4.txt > tmp/temp_rules$1-$2-$3-$4.pl && swipl -f tmp/temp_rules$1-$2-$3-$4.pl -q main)

echo $RESULT

COUNT=$(echo $RESULT | tr -cd , | wc -c)
COUNT=$(expr $COUNT + 1)

end_time=$(($(date +%s%N)/1000000))
elapsed_time=$(expr $end_time - $start_time)
printf "%s,$elapsed_time\r\n" $COUNT  >> data/elapsed_time$1-$2-$3-$4.log
