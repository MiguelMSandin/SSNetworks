#!/usr/bin/env python3

import argparse
import networkx as nx

parser = argparse.ArgumentParser(description="Analyzes a network.")

# Add the arguments to the parser
parser.add_argument("-f", "--file", dest="file_in", required=True,
                    help="Input file. A network file with three columns: 'qseqid sseqid id'.")
parser.add_argument("-a", "--attributeFile", dest="file_attr", required=True,
                    help="Attributes file. A file with the nodes in the first column and the binary attribute in the second column. Columns separated by '\\t'.")
parser.add_argument("-b", "--binaryStates", dest="binary_states", required=True,
                    help="The binary states of the attribute to look for the shortest path from 'from' to 'to' entered as a string and separated by a '+' (i.e.; 'from+to')")
parser.add_argument("-o", "--output", dest="file_out", required=True,
                    help="Output file. A file with the shortest path of every node labelled as 'from' to a node labelled as 'from'")
args = parser.parse_args()

print("\n  Reading network")
G=nx.read_edgelist(args.file_in, delimiter="\t", data=(("id",float),))

print("  Reading attributes") 
with open(args.file_attr) as attributes:
    attr = {}
    for line in attributes:
        line = line.strip().split('\t')
        key = line[0]
        val = line[1]
        attr[key] = val

print("  Setting attributes and states") 
# Now matching order of every node with the attribute
group = {}
for node in G.nodes():
    group[node] = attr.get(node)

nx.set_node_attributes(G, group, "groups")

# Setting the names of the states to look from 'from' to 'to'
states = args.binary_states
states_from = states.strip().split('+')[0]
states_to = states.strip().split('+')[1]

lfrom = len([n for n in G.nodes() if G.nodes[n]["groups"] == states_from])
lto = len([n for n in G.nodes() if G.nodes[n]["groups"] == states_to])

print("\n  Nodes in network: \t", len(G.nodes()),
      "\n    Nodes with state 'from' (attribute name '", states_from, "'): \t", lfrom, 
      "\n    Nodes with state 'to'   (attribute name '", states_to, "'): \t", lto, sep="")

print("\n  Calculating") 
#CCs = nx.connected_component_subgraphs(G)  # When using a 'networkx' version below 2.1
CCs = (G.subgraph(CCs) for CCs in nx.connected_components(G))
with open(args.file_out, "w") as outfile:
    print("connected_component \t node_from \t shortest \t node_to", file=outfile)
    c = 0
    i = 0
    for CC in CCs:
        c = c + 1
        nfrom = [n for n in CC.nodes() if CC.nodes[n]["groups"] == states_from]
        nto = [n for n in CC.nodes() if CC.nodes[n]["groups"] == states_to]
        for n in nfrom:
            i = i + 1
            print("\r    Working on node ", i, "/", lfrom, sep="", end="")
            if states_to in nx.get_node_attributes(CC, "groups").values():
                #shortest = sorted([nx.shortest_path(CC, n, ntoi) for ntoi in nto], key=len)[0]
                shortest = sorted([nx.shortest_path(CC, n, ntoi) for ntoi in nto], key=lambda x: len(x))[0]
                end = shortest[len(shortest)-1]
                shortest = len(shortest)-1
            else:
                shortest = "Inf"
                end = "Node_to_not_in_CC"
            print((str(c) + "\t" + str(n) + "\t" + str(shortest) + "\t" + str(end)), file=outfile)
        
print("\nDone")


