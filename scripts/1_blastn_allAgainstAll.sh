#!/bin/bash

FILE=$1

[ ! -d "blastn" ] && mkdir -p "blastn"
OUTPUT=$(basename -- $FILE)
OUTPUT="blastn/${OUTPUT/.fasta/_allAgainstAll.similarities}"

DB="${FILE/.fasta/.db}"

# First let's make a database out of the file
echo "  Creating a database from '$(basename -- $FILE)'"
makeblastdb -dbtype nucl -in $FILE -out $DB
echo ""

# Now running all against all search
echo "  Running blastn 'all-against-all'"
blastn -query $FILE -db $DB -evalue 1e-10 -max_target_seqs 3000 -max_hsps 1 -num_threads 8 -outfmt "6 qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen" -out $OUTPUT
echo ""

echo "Done"
