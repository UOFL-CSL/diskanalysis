#!/bin/bash

# Password is specified from the first argument

sudo -v

rm "/marzunvme/Stream Benchmarking/blktrace/fio/trivial-readwrite-1g.0.0"

# Start the fio benchmark with the fio_config
screen -S fio -dm bash -c "export HISTIGNORE='*sudo -S*'; echo $1 | sudo -S -v; sudo fio fio_config --output=results.txt --output-format=json; echo Done;" &

# For async io
screen -S blktrace -dm bash -c "export HISTIGNORE='*sudo -S*'; echo $1 | sudo -S -v; sudo ./blktrace -d /dev/nvme0n1 -P 0 -o - | sudo ./blkparse -i -; echo Done; exec bash" &

# Poll for the started fio trace
loops=10
pid=0

while [ $loops -gt 0 ]; do
    sleep 0.1
    loops=$(($loops-1))
    pids=$(ps -T aux | grep fio | grep -v grep | grep -v bash)

    count=$(echo "$pids" | wc -l)

    echo $count

    if [ $count -gt 2 ]
        then
        loops=0
        pid=$(echo "$pids" | awk 'END{print $3}')
    fi    
done

echo Found pid $pid

# Start blktrace
#screen -S blktrace -dm bash -c "export HISTIGNORE='*sudo -S*'; echo $1 | sudo -S -v; sudo ./blktrace -d /dev/nvme0n1 -P $pid -o - | sudo ./blkparse -i -; echo Done; exec bash" &

# Start algorithm
#sudo gnome-terminal -- bash -c "python3 ~/Desktop/DiskAnalysis/analysis/marzullo.py"

