#!/usr/bin/env python3

import argparse
import networkx as nx
import re

parser = argparse.ArgumentParser(description="Clean a network from connected components (CCs) smaller than 'S' (-s), CCs with only one attribute group (-t) or from  a list of given nodes (-l).")

# Add the arguments to the parser
parser.add_argument("-f", "--file", dest="file_in", required=True,
                    help="Net file. A file with three columns, origin node, destination node and identity value.")

parser.add_argument("-o", "--output", dest="file_out", required=True,
                    help="Output file.")

parser.add_argument("-s", "--connectedSize", dest="size", required=False, default=None,
                    help="Remove Connected Components with less than 's' nodes.")

parser.add_argument("-a", "--connectedAttribute", dest="attribute", required=False, default=None,
                    help="Remove Connected Components with only one attribute group. It is needed a file with with two columns, the nodes and the chosen attribute corresponding to the node.")

parser.add_argument("-l", "--listNodes", dest="listNodes", required=False, default=None,
                    help="Remove nodes listed in the selected list (a file with the selected nodes in each line).")

parser.add_argument("-c", "--compressed", dest="compress", required=False, default=None, action="store_true",
                    help="Reads a gzip compressed net file.")

args = parser.parse_args()

print("")

if re.search("\.gz$", args.file_in) is not None and args.compress is None:
    print("  You have provided a compressed file and haven't selected the compress option (-c/--compressed)")
    print("  I'll have to do it for you...")
    compres = True
else:
	compres=False

if args.compress is not None or compres:
    import gzip
    print("  Reading compressed network")
    G=nx.read_edgelist(args.file_in, delimiter="\t", data=(("id",float),), encoding='utf-8')
else:
    print("  Reading network")
    G=nx.read_edgelist(args.file_in, delimiter="\t", data=(("id",float),))

nodes=list(G.nodes())
edges=list(G.edges())
ein=len(edges)

if args.attribute is not None:
    print("  Reading attributes file", end="")
    attribute = {}
    for line in open(args.attribute):
        line = line[:-1].split("\t")
        key = line[0]
        key = re.sub(" $", "", key)
        value = line[1]
        value = re.sub("^ ", "", value)
        attribute[key] = value
    print(" and assign attributes to network")
    group = {}
    for node in nodes:
        group[node] = attribute.get(node)
    nx.set_node_attributes(G, group, "groups")
    
if args.listNodes is not None:
    print("  Reading list of nodes to be removed")
    listNodes = set()
    for line in open(args.listNodes):
        l = re.sub("\n$", "", line)
        listNodes.add(l)

print("  Cleaning network")
c = 0
s = 0
t = 0
l = 0
toRemove = set()
count = nx.number_connected_components(G)
CCs = (G.subgraph(CCs) for CCs in nx.connected_components(G))
for CC in CCs:
    c += 1
    print("\r    Working on CC ", c, "/", count, sep="", end="")
    keep = True
    if args.size is not None:
        if len(CC) < int(4):
            keep = False
            for node in CC:
                s += 1
                toRemove.add(node)
    if args.attribute is not None and keep:
        groups = nx.get_node_attributes(CC, "groups")
        groups = groups.values()
        groups = set(groups)
        if len(groups) <= 1:
            keep = False
            for node in CC:
                t += 1
                toRemove.add(node)
    if args.listNodes is not None:
        for node in CC:
            if node in listNodes:
                l += 1
                toRemove.add(node)

print("\n")
if args.size is not None:
    print("    Cleaned ", s, " nodes belonging to CCs with less than ", args.size, " nodes", sep="")
if args.attribute is not None:
    print("    Cleaned ", t, " nodes belonging to CCs with only one attribute group", sep="")
if args.listNodes is not None:
    print("    Cleaned ", l, " nodes from ", len(listNodes), " listed to be removed", sep="")

print("  Removing nodes")
G.remove_nodes_from(toRemove)
nout = len(list(G.nodes()))
eout=len(list(G.edges()))
cout = nx.number_connected_components(G)

print("  Writing network")
print("          Edges \t Nodes \t CCs")
print("    In:  ", ein, "\t", len(nodes), "\t", count)
print("    Out: ", eout, "\t", nout, "\t", cout)
nx.write_edgelist(G, args.file_out, delimiter="\t", data=["id"])

print("\nDone\n")
