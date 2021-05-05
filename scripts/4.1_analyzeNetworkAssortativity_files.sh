#!/bin/bash

[ ! -d "stats_assortativity" ] && mkdir -p "stats_assortativity"

for FILE in  $(ls | grep \.net$)
do    
    echo "Analyzing ${FILE}"

    /home/mmendezsandin/Desktop/Uppsala/project/ecoEvo/scripts/networks/4_analyzeNetworkAssortativities.py -f $FILE -a tsar_groups.attr -o "stats_assortativity/${FILE/.net/.assortativity_groups}"

    echo ""
done
