#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser(description="Removes reciprocal (A-B = B-A) and identical (A-A) hits from a tab separated list. The first and second columns are taken as identifiers. The rest of the columns are irrelevant.")

requiredArgs = parser.add_argument_group('required arguments')

requiredArgs.add_argument("-f", "--file", dest="file_in", required=True,
                    help="Input file.")

parser.add_argument("-o", "--output", dest="file_out", required=False, default=None,
                    help="Output file. By default will add '_clean' to the input file name (respecting the extension).")

parser.add_argument("-r", "--redundant", dest="redundant", required=False, action="store_true",
                    help="If selected, will export the reciprocal and identical hits to 'output_reciprocal.ext' and 'output_identical.ext' respectively. Being 'output' the selected output name and the 'ext' the given extension.")

parser.add_argument("-v", "--verbose", dest="verbose", required=False, action="store_false",
					help="If selected, will not print information to the console.")

args = parser.parse_args()

# Output file
if args.file_out is None:
	outFile = re.sub("\\.[^\\.]+$", "_clean", args.file_in) + re.sub(".*\\.", ".", args.file_in)
else:
	outFile = args.file_out

if args.verbose:
	print("  Setting hit names")
entries = 0
clean = {}
reciprocal = {}
selfHit = {}
for line in open(args.file_in):
	entries += 1
	seq = line.strip().split()
	seq1 = seq[0]
	seq2 = seq[1]
	if seq1 == seq2:
		selfHit[hit] = line
	hit = str(seq1) + "\t" + str(seq2)
	hitr =str(seq2) + "\t" + str(seq1)
	if hit in clean:
		reciprocal[hit] = line
	elif hitr in clean:
		reciprocal[hit] = line
	else:
		clean[hit] = line

if args.verbose:
	print("  Writing cleaned file to: '", outFile, "'", sep="")
with open(outFile, "w") as outfile:
    for hit in list(clean.keys()):
        print(clean[hit], end="", file=outfile)

if args.redundant:
	outReciprocal = re.sub("\\.[^\\.]+$", "_reciprocal", outFile) + re.sub(".*\\.", ".", outFile)
	outSelf = re.sub("\\.[^\\.]+$", "_identical", outFile) + re.sub(".*\\.", ".", outFile)
	if args.verbose:
		print("  Writing reciprocal hits to: '", outReciprocal, "'", sep="")
	with open(outReciprocal, "w") as outfile:
		for hit in list(reciprocal.keys()):
			print(reciprocal[hit], end="", file=outfile)
	if args.verbose:
		print("  Writing self hits to: '", outSelf, "'", sep="")
	with open(outFile, "w") as outfile:
		for hit in list(selfHit.keys()):
			print(selfHit[hit], end="", file=outfile)

if args.verbose:
	r = len(reciprocal)
	s = len(selfHit)
	a = len(clean)
	print("    Entries:         ", entries, sep="")
	print("    Removed:         ", r+s, " (", round((r+s)/entries*100,2), "%)", sep="")
	print("      Reciprocal:    ", r, " (", round((r)/entries*100,2), "%)", sep="")
	print("      Self matching: ", s, " (", round((s)/entries*100,2), "%)", sep="")
	print("    Out:             ", a, " (", round(a/entries*100,2), "%)", sep="")
	print("Done")
