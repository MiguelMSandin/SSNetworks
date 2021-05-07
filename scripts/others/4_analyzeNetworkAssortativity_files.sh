#!/bin/bash

ATTR=$1

DIR="nets/assortativity"

[ ! -d $DIR ] && mkdir -p $DIR

for FILE in  $(ls nets | grep \.net$)
do    
    echo "Analyzing ${FILE}"

    scripts/4_analyzeNetworkAssortativity.py -f "nets/$FILE" -a $ATTR -o "$DIR/${FILE/.net/.assortativity}"

    echo ""
done
