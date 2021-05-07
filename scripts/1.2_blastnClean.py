#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Removes reciprocal hits (A-B = B-A).")

# Add the arguments to the parser
parser.add_argument("-f", "--file", dest="file_in", required=True,
                    help="Input file. This assumes a file with the following columns: 'qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen'.")
parser.add_argument("-o", "--output", dest="file_out", required=True,
                    help="Output file. Returns the filtered file to the specified location.")
args = parser.parse_args()

print("")
print("  Setting hit names")
clean = {}
removed = 0
accepted = 0
selfHit = 0
for line in open(args.file_in):
    line = line.strip().split()
    seq1 = line[0]
    seq2 = line[1]
    
    if seq1 == seq2:
        selfHit = selfHit + 1
    
    hit = str(seq1) + "\t" + str(seq2)
    hitr =str(seq2) + "\t" + str(seq1)
    
    if hit in clean:
        removed = removed + 1        
    elif hitr in clean:
        removed = removed + 1   
    else:        
        values = str(line[2]) + "\t" + str(line[3]) + "\t" + str(line[4]) + "\t" + str(line[5]) + "\t" + str(line[6]) + "\t" + str(line[7]) + "\t" + str(line[8]) + "\t" + str(line[9]) + "\t" + str(line[10])
        
        clean[hit] = values
        accepted = accepted + 1

print("  Writing cleaned file with '", accepted, "' hits", sep="")
with open(args.file_out, "w") as outfile:
    for hit in list(clean.keys()):
        print(hit + "\t" + clean[hit], file=outfile)

print("    Removed hits:\t", removed)
print("    Self matching:\t", selfHit)
print("Done")
print("")
