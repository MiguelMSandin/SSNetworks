#!/usr/bin/env python3

import argparse
import networkx as nx
import statistics as st

parser = argparse.ArgumentParser(description="Analyzes basic properties of a network (number of nodes, number of edges, connectivity, clustering coefficient and number of connected components), its connected components independently, if any, and its nodes (degree, betweeness, closeness and eccentricity).")

# Add the arguments to the parser
requiredArgs = parser.add_argument_group('required arguments')

requiredArgs.add_argument("-f", "--file", dest="file_in", required=True,
                    help="Input file. A network file with three columns: 'qseqid sseqid id'.")

requiredArgs.add_argument("-o", "--output", dest="file_out", required=True,
                    help="Output file. Returns two files: 'file_out_network' and 'file_out_nodes' with the properties of the network and the statistics for each node respectively.")

args = parser.parse_args()

print("\n  Reading network")
G=nx.read_edgelist(args.file_in, delimiter="\t", data=(("id",float),))

nodes=list(G.nodes())
edges=list(G.edges())

# Splitting the graph into connected components
#CCs = nx.connected_component_subgraphs(G)  # When using a 'networkx' version below 2.1
CCs = (G.subgraph(CCs) for CCs in nx.connected_components(G))
count = 0
for CC in CCs:
    count = count + 1

# Setting names of output file
outNetwork = args.file_out + "_network"
outNodes = args.file_out + "_nodes"

print("\n  Calculating properties of the network")
with open(outNetwork, "w") as outfile:
    print(("Input file: " + "\t" + str(args.file_in)), file=outfile)
    # Number of nodes
    print("    Number of nodes", end="")
    print(("Number of nodes" + "\t" + str(len(nodes))), file=outfile)
    # Number of edges
    print(": done \n    Number of edges", end="")
    print(("Number of edges" + "\t" + str(len(edges))), file=outfile)
    # Average number of neighbours 
    print(": done \n    Connectivity", end="")
    tmp = dict(nx.degree(G))
    tmp = tmp.values()
    tmp = st.mean(tmp)  
    print(("Connectivity" + "\t" + str(tmp)), file=outfile)    
    #print(("Connectivity" + "\t" + str(nx.average_degree_connectivity(G))), file=outfile)
    # Clustering coefficient: E/((N(N-1))/2)
    print(": done \n    Clustering coefficient", end="")
    print(("Clustering coefficient" + "\t" + str(nx.density(G))), file=outfile)
    # Connected components
    print(": done \n    Connected components", end="")
    print(("Connected components" + "\t" + str(count)), file=outfile)
    print(": done\n")

if count > 1:
    print("  There are '", count, "' connected components (CC). Analyzing each one of them individually as an indpedendent network:", sep="")
    outNetworkCCs = args.file_out + "_network_CCs"
    #CCs = nx.connected_component_subgraphs(G)  # When using a 'networkx' version below 2.1
    CCs = (G.subgraph(CCs) for CCs in nx.connected_components(G))
    c = 0
    with open(outNetworkCCs, "w") as outfile:
        print("Connected_component \t Nnodes \t Nedges \t Connectivity \t Density", file=outfile)  
        for CC in CCs:
            c = c +1
            print("\r    Working on CC ", c, "/", count, sep="", end="")
            nnodes = len(list(CC.nodes()))
            nedges = len(list(CC.edges()))
            tmp = dict(nx.degree(CC))
            tmp = tmp.values()
            connec = st.mean(tmp)
            densit = nx.density(CC)          
            print((str(c) + "\t" + str(nnodes) + "\t" + str(nedges) + "\t" + str(connec) + "\t" + str(densit)), file=outfile)
        print("\n")

print("  Calculating properties of the nodes")
#CCs = nx.connected_component_subgraphs(G)  # When using a 'networkx' version below 2.1
CCs = (G.subgraph(CCs) for CCs in nx.connected_components(G))
with open(outNodes, "w") as outfile:
    print("Connected_component \t Node \t Degree \t Betweenness \t Closeness \t Eccentricity", file=outfile)
    c = 0
    for CC in CCs:
        c = c + 1
        if count > 1:
            print("\r    Working on CC ", c, "/", count, sep="", end="")            
        # Degree: Number of edges related to a node
        degree = nx.degree(CC)
        # Betweenness: Frequency of being in a shortest path
        betweeness = nx.betweenness_centrality(CC)
        # Closeness: Average shortest distance between a node and all other nodes
        closeness = nx.closeness_centrality(CC)
        # Eccentricity: Average longest distance between a node and all other nodes
        eccentricity = nx.eccentricity(CC)
        for node in CC.nodes():
            print((str(c) + "\t" + str(node) + "\t" + str(degree[node]) + "\t" + str(betweeness[node]) + "\t" + str(closeness[node]) + "\t" + str(eccentricity[node])), file=outfile)
    print("\n\nDone")
