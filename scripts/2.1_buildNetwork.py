#!/usr/bin/env python3

import argparse
from collections import defaultdict
import re

parser = argparse.ArgumentParser(description="Creates a network file from a similarity blast output.")

# Add the arguments to the parser
requiredArgs = parser.add_argument_group('required arguments')

requiredArgs.add_argument("-f", "--file", dest="file_in", required=True,
                    help="Input file. This assumes a file with the following columns: 'qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen'.")

requiredArgs.add_argument("-i", "--identity", dest="identity", required=True,
                    help="Identity threshold(s) to establish a connection between nodes. If more than one, separate them with a '+' into a string (i.e.; '80+85+90+95').")

requiredArgs.add_argument("-o", "--output", dest="file_out", required=True,
                    help="Output file. Returns the network file. Files will be exported to the output file name ('output') followed by the selected thresholds and the '.net' extension (i.e.; 'output_80.net').")

parser.add_argument("-c", "--cover", dest="cover", required=False, default=None,
                    help="Applies a minimal cover threshold to establish a connection between nodes, in addition to the identity and evalue, if selected, thresholds.")

parser.add_argument("-e", "--evalue", dest="evalue", required=False, default=None,
                    help="Applies a maximal evalue threshold to establish a connection between nodes, in addition to the identity and cover, if selected, thresholds.")

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
        c=", '" + str(args.cover) + "' minimum cover"
        C="_" + str(args.cover) + "c"
    else:
        c=""
        C=""
    if args.evalue is not None:
        e=", '" + str(args.evalue) + "' maximum evalue"
        E="_" + str(args.args) + "e"
    else:
        e=""
        E=""
    print("  Creating a network file with '", i, "%' similarity threshold", c, e, sep="")
    tmp = args.file_out + "_" + i + "i" + C + E + ".net"
    with open(tmp, "w") as outfile:
        for line in open(input_file):
            data = line[:-1].split("\t")
            seq1 = data[0]
            seq2 = data[1]
            seqid = data[3]
            if (seq1 != seq2) and (int(float(seqid)) >= int(float(i))):
                statement1=True
            else:
                statement1=False
            if args.cover is not None:
                cover1 = 100.0 * (int(data[6])-int(data[5])) / int(data[7])
                cover2 = 100.0 * (int(data[9])-int(data[8])) / int(data[10])
                if (cover1 >= int(args.cover)) and (cover2 >= int(float(args.cover))):
                    statement2=True
                else:
                    statement2=False
            else:
                statement2=None
            if args.evalue is not None:
                ev = data[2]
                if (int(float(ev)) <= int(float(args.evalue))):
                    statement3=True
                else:
                    statement3=False
            else:
                statement3=None
            if statement1 and (statement2 or statement2==None) and (statement3 or statement3==None):
                out = str(seq1) + "\t" + str(seq2) + "\t" + str(seqid)  
                print(out, file=outfile)
    print("    Network file exported to: '", tmp, "'", sep="")

print("Done")
print("")

