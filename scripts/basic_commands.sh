#!/bin/bash

# Running BLASTn all-against-all
bash scripts/1.1_blastn_allAgainstAll.sh raw/FILE.fasta

# Cleaning blast output
chmod +x scripts/*py
scripts/1.2_blastnClean.py -f nets/FILE_allAgainstAll.similarities -o nets/FILE_allAgainstAll_clean.similarities
# scripts/1.2_blastnClean.py -f nets/FILE2_allAgainstAll.similarities -o nets/FILE2_allAgainstAll_clean.similarities

# Build network
scripts/2.1_buildNetwork.py -f nets/FILE_allAgainstAll_clean.similarities -i "80+85+90+95" -c 80 -o nets/FILE.net
# scripts/2.1_buildNetwork.py -f nets/FILE2_allAgainstAll_clean.similarities -i "20+30+40+50+60+70+80+90" -c 70 -e 0.00005 -o nets/FILE2.net

# Analyze basic properties of the network
bash scripts/others/3_analyzeNetwork_files.sh

# Analyze assortativity
bash scripts/others/4_analyzeNetworkAssortativity_files.sh raw/FILE.attr
# bash scripts/others/4_analyzeNetworkAssortativity_files.sh raw/FILE2.attr

# Analyze shortest path
bash scripts/others/5_analyzeNetworkShortestPath_files.sh raw/FILE.short "Environmental+Reference"
# bash scripts/others/5_analyzeNetworkShortestPath_files.sh raw/FILE2.short "Eukaryotic+Other"


