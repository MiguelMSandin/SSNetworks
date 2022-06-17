#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser(description="")

# Add the arguments to the parser
requiredArgs = parser.add_argument_group('required arguments')

requiredArgs.add_argument("-f", "--file", dest="net", required=True,
                    help="Net file. A file with at least two columns: origin node and destination node. The rest of the columns will be ignored.")

requiredArgs.add_argument("-a", "--attributes", dest="attributes", required=True,
                    help="A tab separated table with at least two columns: the nodes and the chosen attribute corresponding to the node (with no spaces in the attribute names). The rest of the columns will be ignored.")

parser.add_argument("-c", "--compressed", dest="compress", required=False, action="store_true",
                    help="Reads a gzip compressed net file.")

args = parser.parse_args()

print("  Reading attributes file")
attributes = {}
for line in open(args.attributes):
	line = line.split("\t")
	key = line[0]
	value = line[1]
	value = re.sub("\n", "", value)
	attributes[key] = value

print("  Counting network connections")

with open(args.net, 'r') as tmp:
	for lines, line in enumerate(tmp):
		pass
tmp.close()
lines = lines + 1
l = 0
count = {}
errors = set()
for line in open(args.net):
	l += 1
	i = round(l/lines*100)
	if l == 1:
		I = i
	if i != I:
		I = i
		print("\r  Counting network connections ", i, "%", sep="", end="")
	line = line.split("\t")
	source = line[0]
	satt = attributes.get(source)
	target = line[1]
	target = re.sub("\n", "", target)
	tatt = attributes.get(target)
	if satt is None or tatt is None:
		if satt is None:
			errors.add(source)
		if tatt is None:
			errors.add(target)
	else:
		edge = sorted((satt, tatt))
		edge = ' '.join(edge)
		if edge in count.keys():
			count[edge] += 1
		else:
			count[edge] = 0

print("\n")

if len(errors) > 0:
	if len(errors) < 20:
		print("  Warning!! The following", len(errors), "nodes didn't have a match in the attributes file:")
		for e in errors:
			print("  -", e)
	if len(errors) > 19:
		import re
		tmp = re.sub("\\.[^\\.]+$", "_countAttributeConnections_errorReport.log", args.net)
		print("  Warning!!", len(errors), "nodes didn't have a match in the attributes file.")
		print("  Please check: '", tmp, "' for further details on which nodes.", sep="")
		with open(tmp, "w") as TMP:
			for e in errors:
				print(e, file=TMP)

print("\nAttribute1\tAttribute2\tConnections")
for key, value in count.items():
	key = key.split(" ")
	key1 = key[0]
	key2 = key[1]
	print(key1, "\t", key2, "\t", value)

print("\nDone")
