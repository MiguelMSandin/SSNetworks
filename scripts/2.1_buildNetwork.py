#!/usr/bin/env python3

import argparse
from collections import defaultdict
import re

parser = argparse.ArgumentParser(description="Creates a network file from a similarity blast output. In order to ease downstream analysis, files will be exported to the input file name followed by the identity threshold, the cover, if selected, and the '.net' extension (i.e.; 'file_80.net', 'file_85i_80c.net').")

# Add the arguments to the parser
parser.add_argument("-f", "--file", dest="file_in", required=True,
                    help="Input file. This assumes a file with the following columns: 'qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen'.")
parser.add_argument("-i", "--identity", dest="identity", required=True,
                    help="Identity threshold(s) to establish a connection between nodes. If more than one, separate them with a '+' into a string (i.e.; '80+85+90+95').")
parser.add_argument("-c", "--cover", dest="cover", required=False, default=None,
                    help="If selected, also applies a minimal cover threshold to establish a connection between nodes.")
parser.add_argument("-k", "--clean", dest="cleaning", required=False, action="store_true", default=None,
                        help="If selected, the input file is cleaned from reciprocal hits (A-B = B-A) before creating the network file.")
args = parser.parse_args()

print("")
# Clean the file if needed
if args.cleaning is not None:
    print("  Cleaning the file:")
    print("    Setting hit names")
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

    print("    Writing cleaned file with '", accepted, "' hits", sep="")
    cleanFile = re.sub("\..*$", "_clean.similarities", args.file_in)
    with open(cleanFile, "w") as outfile:
        for hit in list(clean.keys()):
            print(hit + "\t" + clean[hit], file=outfile)
    
    print("      Removed hits: ", removed)
    print("      Self matching:", selfHit)
    print("  Cleaned file exported to: '", re.sub("\..*$", "_clean.similarities", args.file_in), "'", sep="")

# Setting name of input file
if args.cleaning:
    input_file = re.sub("\..*$", "_clean.similarities", args.file_in)
else:
    input_file = args.file_in

# Now looping through the different identity thresholds (if more than one) and selecting nodes
iden = args.identity
for i in iden.split('+'):
    if args.cover is not None:
        print("  Creating a network file with '", i, "%' similarity threshold and '", args.cover, "' minimum cover", sep="")
        tmp = re.sub("\..*$", "", input_file) + "_" + i + "i" + "_" + args.cover + "c.net"
    else:
        print("  Creating a network file with '", i, "%' similarity threshold", sep="")
        tmp = re.sub("\..*$", "", input_file) + "_" + i + ".net"
    with open(tmp, "w") as outfile:
        for line in open(input_file):
            data = line[:-1].split("\t")
            seq1 = data[0]
            seq2 = data[1]
            seqid = data[3]
            if args.cover is not None:
                cover1 = 100.0 * (int(data[6])-int(data[5])) / int(data[7])
                cover2 = 100.0 * (int(data[9])-int(data[8])) / int(data[9])
                if (seq1 != seq2) and (int(float(seqid)) >= int(float(i))) and (cover1 >= int(args.cover)) and (cover2 >= int(args.cover)):
                    out = str(seq1) + "\t" + str(seq2) + "\t" + str(seqid)
                    print(out, file=outfile)
            else:
                if (seq1 != seq2) and (int(float(seqid)) >= int(float(i))):
                    out = str(seq1) + "\t" + str(seq2) + "\t" + str(seqid)
                    print(out, file=outfile)
    print("    Network file exported to: '", tmp, "'", sep="")

print("Done")
print("")
