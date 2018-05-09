#!/bin/bash

# Parameters max_depth n_relations n_functions max_size_functions n_iterations

mkdir -p data
mkdir -p tmp

if [ ! -f data/elapsed_time$1-$2-$3-$4.log ]; then
    printf "n_functions,time\r\n" > data/elapsed_time$1-$2-$3-$4.log
fi

for i in `seq 2 $5`
do
    sh run_random.sh $1 $2 $3 $4
done

#sed -i ':a;N;$!ba;s/\n/,/g' data/elapsed_time$1-$2-$3-$4.log
#sed -i 's/,,/,/g' data/elapsed_time$1-$2-$3-$4.log

