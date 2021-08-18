#!/bin/bash
res_dir="/root/results"
mkdir -p ${res_dir}
for test_mode in rndrd rndwr rndrw
do
  for th in 1 2 4 8 16 32 64 128
  do
    echo "Starting benchmark for ${test_mode} threads ${th}"
    sysbench fileio \
             --file-total-size=700G \
             --time=1800 \
             --max-requests=0 \
             --threads=${th} \
             --file-num=64 \
             --file-io-mode=sync \
             --file-test-mode=${test_mode} \
             --file-extra-flags=direct \
             --file-fsync-freq=0 \
             --file-block-size=16384 \
             --report-interval=1 \
             run > "${res_dir}/${test_mode}_${th}.out"
  done
done
