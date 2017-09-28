#!/bin/bash

start_time=$(($(date +%s%N)/1000000))

python3 test_empty.py
python3 test_empty2.py

end_time=$(($(date +%s%N)/1000000))
elapsed_time=$(expr $end_time - $start_time)
printf "Elaspsed Time : $elapsed_time\r\n"
