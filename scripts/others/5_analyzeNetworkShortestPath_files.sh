#!/bin/bash

ATTR=$1
STATES=$2

DIR="nets/shortest"

[ ! -d $DIR ] && mkdir -p $DIR

for FILE in  $(ls nets/ | grep \.net$)
do    
    echo "Analyzing ${FILE}"

    scripts/5_analyzeNetworkShortestPath.py -f "nets/$FILE" -a $ATTR -b $STATES -o "$DIR/${FILE/.net/.shortest}"

    echo ""
done
