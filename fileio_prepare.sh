sysbench --test=fileio \
         --file-total-size=700G \
         --threads=16 \
         --file-num=64 \
         --file-block-size=16384 \
         prepare
