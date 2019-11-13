#!/bin/bash

sudo -v

rm "/home/marzullo/Desktop/Stream Benchmarking/fio/trivial-readwrite-1g.0.0"

# Start the fio benchmark with the fio_config
gnome-terminal -- bash -c "fio fio_config --output=results.txt --output-format=json"

# Poll for the started fio trace
loops=100
pid=0

while [ $loops -gt 0 ]; do
    sleep 0.1
    loops=$(($loops-1))
    pid=$(ps aux | grep fio | grep -v grep | awk '{print $2}')

    if [ $pid -gt 0 ]
        then
        loops=0
    fi    
done

echo Found pid $pid

# Start blktrace
sudo gnome-terminal -- bash -c "./blktrace -d /dev/sda -P $pid -o - | ./blkparse -i -"

# Start algorithm
sudo gnome-terminal -- bash -c "python3 ~/Desktop/DiskAnalysis/analysis/marzullo.py"

