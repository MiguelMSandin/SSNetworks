#!/bin/bash

DIR="nets/stats"

[ ! -d $DIR ] && mkdir -p $DIR

for FILE in $(ls nets | grep \.net$)
do    
    echo "Analyzing ${FILE}"

    scripts/3_analyzeNetwork.py -f "nets/$FILE" -o "$DIR/${FILE/.net/.stats}"
    
    echo ""
done

