#!/bin/bash

start_time=$(($(date +%s%N)/1000000))

python3 experiments/experiment_empty.py
python3 experiments/experiment_empty2.py
python3 experiments/experiment_empty3.py

end_time=$(($(date +%s%N)/1000000))
elapsed_time=$(expr $end_time - $start_time)
printf "Elaspsed Time : $elapsed_time\r\n"
