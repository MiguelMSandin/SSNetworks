#!/bin/bash

[ ! -d "blastn/stats" ] && mkdir -p "blastn/stats"

for FILE in $(ls blastn | grep \.net$)
do    
    echo "Analyzing ${FILE}"

    scripts/3_analyzeNetwork.py -f "blastn/$FILE" -o "blastn/stats/${FILE/.net/.stats}"
    
    echo ""
done
