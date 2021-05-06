# Sequence Similarity Network (SSN)  

Miguel M. Sandin  
Last modification: 2021-05-05  
miguelmendezsandin@gmail.com  

## Before starting  
Please, bear in mind that the scope of this materials came from **an internal collaborative effort** and should only be considered as a **quick-and-dirty introduction** to SSN building. It is far from exhaustive in both theory, practical details and further references on SSN and it is written by a non-specialist in the topic. Therefore shouldn't be taken as a reference or complete framework for the study of SSN.  
  
---
  
## Dependencies  
- [BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download)  
- [Cytoscape](https://cytoscape.org/) 
- [python](https://www.python.org/)  
    -   **Required modules**: argparse, collections, networkx, pandas, re, statistics.  
- [R](https://www.r-project.org/)  
    -   **Required packages**: data.table, ggplot2, ggrides, scales, RColorBrewer.  
    -   **Optional packages**: dplyr, tidyr, tibble, stringr, seqinr.  
### Optional  
- [Rstudio](https://rstudio.com/products/rstudio/download/) 

---

## General introduction, why SSN?  
Phylogenetic trees have been largely used for the detailed exploration of phylogenetic patterns among biological entities allowing the understanding of relationships inaccessible by other means. With the advent of phylogenomics, previously unresolved patterns have been clarified and their understanding has been improved. Yet, deep phylogenetic relationships, believed to have happened more than a billion years ago, remain blurry and mostly inaccessible from our clear understanding. In addition, eukaryotic genomes (and genes) are complex, interacting within and between different biological entities and at different levels (i.e.; genes, genomes, individuals, holobionts, populations, metapopulations, communities, ecosystems, ...) and therefore generating chimeric outputs ([van Etten and Bhattacharya, 2020](https://www.sciencedirect.com/science/article/abs/pii/S0168952520302067)). The correct interpretation of such interactions is crucial for furthering the understanding of the evolution and diversity that we observe nowadays.  
  
### So, why SSN and not yet another phylogenetic tree?  
Well firstly, SSN are not intended to replace phylogenetic analysis, but complement them. SSN are (mostly) based in local pairwise alignment similarity and therefore is not inferring phylogenetic signal (i.e.; A->G = A->C = A->T). Yet, SSN is not relying on a global alignment and the output (and threfore its interpretation) is less susceptible to unresolved positions of highly variable or fast evolving regions or sequences (that would align depending on the algorithm or even prone to miss-alignments).  
  
SSN most of the times targets other scientific question than phylogenetic relationships. Phylogenetic trees are the most powerful tool for the exploration of phylogenetic patterns. This tool is based in the assumption of a bifurcating especiation, which is highly accepted for the independent biological entity. However, speciation is a complex process from an holistic perspective where interactions among different biological entities shape the central core of our studies, mostly genes and genomes. Yet the exploration of genome origins, deep and ancient phylogenetic relationships, or co-evolution host-symbionts are obscure and more complex processes than a bifurcating speciation concept, where multiple interactions are possible. The analyses of SSN provide tools for tackling a multitude of evolutionary complex phenomena, such as **gene transfers**, either **composite genes and genomes** ([Alvarez-Ponce et al. 2013](https://www.pnas.org/content/110/17/E1594)) or within **holobionts** ([Meheust et al., 2013](https://www.pnas.org/content/113/13/3579)), and therefore better understand evolutionary transitions, which remain difficult to explore from a bifurcating speciation perspective ([Bapteste et al., 2013](https://www.sciencedirect.com/science/article/abs/pii/S0168952513000863); [Papale et al. 2020](https://www.sciencedirect.com/science/article/pii/S0966842X19302926)).   
  
### And what about ecological analaysis?
### What is a SSN telling that is not another ordination analysis?  
Again, SSN are complementing previous well-established analysis such as multivariate analyses (PERMANOVA, Simper, ...) or ordination analyses (nMDS, PCA, PCoA, ...), that are mostly focusing on abundance or diversity of the given studied taxa. The use of SSN play important roles in testing ecological hypothesis previously unveiled through other means by establishing multiple possible connections based in shared gene/protein similarity. Here we can test and quantify the clustering trends of attributes related to your sequences (**assortativity**, [Foster et al., 2015](https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-015-0125-5)), or how many transitions are needed to go from one attribute to another (**shortest path**, [Arroyo et al., 2020](https://academic.oup.com/gbe/article/12/9/1664/5857131)).    

---
  
## Data selection  
When SSN reconstruction the selection of the data is the most important step, as in phylogenetic analyses. Here you should include every group of sequences/proteins you want to compare, according to your scientific question. This is the most crucial and limiting step because each sequence has to be align to one another and the number of alignments is quadratic to the number of sequences. Keep in mind that since it is pairwise alignment, you can always remove sequences (or pairwise similarities) you finally decided not take into account without altering the rest of the data, but there will be a trade of between computational resources and biological meaning.  
  
To quickly go through this pipeline, I would recommend using a relatively small subset of your data (~<1 mB fasta file formatted), in order to speed up computational analyses and to get to see different outputs. Otherwise you can use any of the two files provided in the ‘raw’ folder:  
  
-*`FILE.fasta`*: contains a random(ish) selection of 18S Radiolaria sequences trying to cover most of their diversity (plus some Phaeodaria sequences as an outgroup so you can also use the same file in phylogenetic analyses for comparisons).  
  
-*`FILE2.fasta`*: Contains a random(ish) selection of protein genome sequences extracted from [Alvarez-Ponce et al. 2013](https://www.pnas.org/content/110/17/E1594) ([Dryad repository](https://datadryad.org/stash/dataset/doi:10.5061/dryad.qr81p)). 
  
---
  
## Getting started  
Let's assume we have gather in a single fasta file all the sequences/proteins we want to explore, and we call it '`FILE.fasta`'. This file will be our starting point for the creation, visualization and analysis of the network.  
  
In order to keep an order and a structure, we are going to be working in a given working directory where '`FILE.fasta`' will be in a folder called '**raw**', the scripts in a folder called '**scripts**', and the output from this pipeline will be exported to a folder called '**nets**'. So you can have other folders in the same directory with other analysis for the same fasta file (e.g.; multiple sequence alignments, phylogenetic analysis, BLAST NCBI search, sequencing results, metadata, etc.).  
  
For a **graphical guide**, please check the slides [presentation](https://github.com/MiguelMSandin/SSNetworks/blob/main/ppt/210506_networks_intro.pdf) in the [ppt](https://github.com/MiguelMSandin/SSNetworks/tree/main/ppt) folder.
  
### 1_blastn_allAgainstAll.sh 
To start, we perform a **local** pairwise similarity comparison among all sequences using BLASTn, or in other words, a blast all-against-all. For that, firstly we create a database of `FILE.fasta` and then calculate the similarity. We are using 8 processors, so please change the script (line: 18) according to your needs/resources.  
  
`bash scripts/1_blastn_allAgainstAll.sh raw/FILE.fasta`  
  
The output has been exported to `nets/FILE_allAgainstAll.similarities`.  
  
>**Note1**: If you are using protein sequences you should change line 13-14 and 19-20.
>**Note2**: Consider other local alignment algorithms such as 'Diamond' ([Buchfink et al. 2014](https://www.nature.com/articles/nmeth.3176)), that it has been tested to be almost as accurate as BLAST and three times faster. Also, depending on your scientific question you might be interested in **global** similarity comparison instead; consider using `vsearch --allpairs_global` ([Rognes et al. 2016](https://pubmed.ncbi.nlm.nih.gov/27781170/)) or any other algorithm for a different similarity identity.
  
#### 1.2_blastnClean.py  
Now we should remove reciprocal hits (i.e.; A-B=B-A) from the blastn search, and we can do that with the script `1.2_blastnClean.py` as follows:  
  
`scripts/1.1_blastnClean.py -f nets/FILE_allAgainstAll.similarities -o nets/FILE_allAgainstAll_clean.similarities`  
  
>**Note1**: For further details on its usage, or the usage of any other python script, type `scripts/1.2_blastnClean.py -h`. If this is not working you may want to make the scripts executable as follows: '`chmod +x scripts/1.2_blastnClean.py`  
>**Note2**: Pay attention to where you have located python in your computer and modify the first line of each python script accordingly (`#!/usr/bin/env python3`).  
  
---
  
### 2.1_buildNetwork.py
The next step is to create the network file from the cleaned blastn output (after removing self-hits; i.e., A-A). A network is basically a graph where you have two sequences (or nodes) connected by an edge. Whether two nodes are connected or not, will depend on the threshold we settle, this is why we should include more than one in order to see a *gradient* of connections. In this example we are going to be using 4 different identity thresholds: 80%, 85%, 90% and 95% and including a minimum mutual match coverage of the 80%, but feel free to use your favourite thresholds or even not including the mutual cover if you are using similar(ish) length sequences (remember using `scripts/2.1_buildNetwork.py -h`for further details):  
  
`scripts/2.1_buildNetwork.py -f nets/FILE_allAgainstAll_clean.similarities -i "80+85+90+95" -c 80 -o nets/FILE.net`  
  
In the folder 'nets' we can see 4 different files corresponding to the networks of each identity threshold selected. These files have three columns, the pair of sequences (or nodes) compared, corresponding to column 1 and 2, and their similarity identity, in column 3. Each line represents the connections among nodes, or an edge:  

|    |    |    |
|----|----|----|
|seq1|seq2|id12|
|seq1|seq3|id13|
|seq2|seq4|id23|
|... |... |... |

  
#### Cytoscape  
At this point we can already visualize a network in Cytoscape (for example). To do so, open Cytoscape and import (or click and drag) the network; in the pop-up window, select *Advanced Options* and de-select *Use first line as column names*. Then click in *Column 1* and select *Source Node* (green dot) and in *Column 2* select *Target Node* (orange dot), if you want you can also change the name of *Colum 3* to (for example) *pident*. And voila! you can already visualize and play with the arrangement of your network. Although if you are using big datasets, it may take a while or consume a lot of RAM (consider using other resources, i.e.: `ssh -Y`).  
Yet might be relevant to include some colouring in the network for a better interpretation. We can then use some attributes of the nodes, such as the taxonomy, the environment where the sequence have been retrieved, the number of reads of every sequence, the sequencing origin, etc.  
  
### 2.2_attributes_file.R  
With this script you can extract information out of the sequence names and create an attribute table called '**FILE.attr**'. If you already have a tab-delimited table with appropriate headers, you can skip this step.  
  
>**Important**: The first column should have the exact same name as the nodes in the network (although there is no need to remove sequences not present in the network). And remember to add a name for the attributes, so following scripts know what attribute is working on:  

| Sequece_name    |Taxonomy     |Environment     |...  |
|-----|-----|-----|-----|
|seq1 |taxoA|envA |...  |
|seq2 |taxoB|envB |...  |
|seq3 |taxoC|envC |...  |
|seq4 |taxoD|envC |...  |
|...  |...  |...  |...  |

  
#### Cytoscape  
We can include the attribute table we have just created by clicking in *Import Table from File*, and the table should already be formatted properly. Now in *Style* we can easily (or not, depending on how big your network is) change the aesthetics of the network to give a biological meaning of such interactions.  
  
---
  
### 3_analyzeNetwork.py
With this script we can calculate basic properties of a network and its nodes. If a network is composed of more than one connected component (CC), it also analyzes each one of them independently. For every network file it exports two files (using OUTPUT as the specified output name):  

- **OUTPUT_network**: Shows for a given network (and its CCs if more than one; **OUTPUT_network_CCs**):  
	- number of nodes  
    - number of edges  
    - connectivity  
    - clustering coefficient  
    - number of CCs  
  
- **OUTPUT_nodes**: For each node it shows:  
    - degree: or number of edges related to the given node  
    - betweenness: or frequency of being in a shortest path  
    - closeness: or the average shortest distance between a node and all other nodes  
    - eccentricity: or the average longest distance between a node and all other nodes  

>**Note**: Depending on the version of the module 'networkx' you are using you may want to change lines 26-27, 63-64 and 81-82.  
  
But since we have selected more than one identity threshold in the previous step (2.1), we can run the script '3_analyzeNetwork_files.sh' that will go through all the '.net' files we have in the 'nets' folder, run the script '3_analyzeNetwork.py' and export the results to a folder called 'nets/stats' (and it actually creates the folder if it doesn't exist).  
  
`bash scripts/others/3_analyzeNetwork_files.sh`  
  
But if you absolutely want to run file by file you can always do it as follows:  
  
`mkdir nets/stats`  
`scripts/3_analyzeNetwork.py -f nets/FILE_80i_80c.net -o nets/stats/FILE_80i_80c.stats`  
`scripts/3_analyzeNetwork.py -f nets/FILE_85i_80c.net -o nets/stats/FILE_85i_80c.stats`  
`scripts/3_analyzeNetwork.py -f nets/FILE_90i_80c.net -o nets/stats/FILE_90i_80c.stats`  
`scripts/3_analyzeNetwork.py -f nets/FILE_95i_80c.net -o nets/stats/FILE_95i_80c.stats`  
  
---
  
### 4_analyzeNetworkAssortativity.py
We can now start looking for patterns, for example, among the attributes of the sequences. With this script we can analyze the tendency of the attributes of the sequences/nodes to cluster together or not. In other words the assortativity of the attributes or groups. This script will export a file with three columns, the attribute analyzed, the assortativity for each attribute and the different states of the attribute. And if there are more than one CC, another file will be exported for every CC.  
  
As in the previous step, we can run this analysis for all the nets using the script `4_analyzeNetworkAssortativity_files.sh` as follows:  
  
`bash scripts/others/4_analyzeNetworkAssortativity_files.sh raw/FILE.attr`  
  
>**Note**: We are including the attribute file (FILE.attr) as the first, and only, parameter after the bash script, so you don't have to change the script if you are using two, or more, different attribute files.  
  
And again, if you want to run file by file:  
  
`mkdir nets/stats`  
`scripts/4_analyzeNetworkAssortativity.py -f nets/FILE_80i_80c.net -a raw/FILE.attr -o nets/assortativity/FILE_80i_80c.assortativity`  
`scripts/4_analyzeNetworkAssortativity.py -f nets/FILE_85i_80c.net -a raw/FILE.attr -o nets/assortativity/FILE_85i_80c.assortativity`  
`scripts/4_analyzeNetworkAssortativity.py -f nets/FILE_90i_80c.net -a raw/FILE.attr -o nets/assortativity/FILE_90i_80c.assortativity`  
`scripts/4_analyzeNetworkAssortativity.py -f nets/FILE_95i_80c.net -a raw/FILE.attr -o nets/assortativity/FILE_95i_80c.assortativity`  
  
---
  
### 5_analyzeNetworkShortestPath.py
Other *interesting* analysis could be to calculate the number of nodes you have to cross from any given node with an attribute *state_A* to arrive until the closest node with an attribute *state_B*, also called 'shortest path analysis'. This understand you have an attribute with a binary state (two different states and not more), so one of the states will be considered *from* and the other *to* and will analyze the shortest path from the state *from* to the state *to*.  
   
Since for this analysis we are only interested in one attribute (with only two states), we have to provide another attribute file, which to avoid confussion will be called '**FILE.short**'. And we remove the headers!.  
  
Again, we run the script `others/5_analyzeNetworkShortestPath_files.sh` in order to perform this analysis for all the networks:  
  
`bash scripts/others/5_analyzeNetworkShortestPath_files.sh raw/FILE.short "from+to"`  
  
Or network by network:  
  
`mkdir nets/shortest`  
`scripts/5_analyzeNetworkShortestPath.py -f nets/FILE_80i_80c.net -a raw/FILE.short -b "from+to" -o nets/shortest/FILE_80i_80c.shortest`  
`scripts/5_analyzeNetworkShortestPath.py -f nets/FILE_85i_80c.net -a raw/FILE.short -b "from+to" -o nets/shortest/FILE_85i_80c.shortest`  
`scripts/5_analyzeNetworkShortestPath.py -f nets/FILE_90i_80c.net -a raw/FILE.short -b "from+to" -o nets/shortest/FILE_90i_80c.shortest`  
`scripts/5_analyzeNetworkShortestPath.py -f nets/FILE_95i_80c.net -a raw/FILE.short -b "from+to" -o nets/shortest/FILE_95i_80c.shortest`  
  
>**Note**: If you are using the files provided you should change "from+to" to "Environmental+Reference", so we will explore the shortest path from an *environmental* sequence to a *Reference* sequence.  

---
  
### statsNetworks.R  
Finally we can make sense of all the previous analysis and get to see the results with the R script `statsNetworks.R` (*recommended to open it in Rstudio*). The script is self explained, so please read carefully the headers and comments so you know what you are doing.  
  
---
  
## References  
-Alvarez-Ponce, D., Lopez, P., Bapteste, E., McInerney, J.O., 2013. Gene similarity networks provide tools for understanding eukaryote origins and evolution. PNAS. E1594–E1603. doi:[10.1073/pnas.1211371110](https://www.pnas.org/content/110/17/E1594)  
-Arroyo, A.S., Iannes, R., Bapteste, E., and Ruiz-Trillo, I., 2020. Gene Similarity Networks Unveil a Potential Novel Unicellular Group Closely Related to Animals from the Tara Oceans Expedition. Genome Biol. Evol. 12(9):1664–1678. doi:[10.1093/gbe/evaa117B](https://academic.oup.com/gbe/article/12/9/1664/5857131)  
-Bapteste, E., van Iersel, V., Janke, A., Kelchner, S., Kelk, S., McInerney, J.O., Morrison, D.A., Nakhleh, L., Steel, M., Stougie, L., and Whitfield, J. 2013. Networks: expanding evolutionary thinking. Trends in Genetics August 2013, Vol. 29, No. 8. doi:[10.1016/j.tig.2013.05.007](https://www.sciencedirect.com/science/article/abs/pii/S0168952513000863)  
-Forster, .D, Bittner, L., Karkar, S., Dunthorn, M., Romac, S., Audic, S., Lopez, P., Stoeck, T., Bapteste, B. 2015. Testing ecological theories with sequence similarity networks: marine ciliates exhibit similar geographic dispersal patterns as multicellular organisms. BMC Biology 13:16. doi:[10.1186/s12915-015-0125-5](https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-015-0125-5)  
-Méheust, R., Zelzion, E., Bhattacharya, D., Lopez, P., and Bapteste, E.. 2013. Protein networks identify novel symbiogenetic genes resulting from plastid endosymbiosis. doi:[10.1073/pnas.1517551113](https://www.pnas.org/content/113/13/3579)  
-Papale, F., Saget, J.,Bapteste, E., 2020. Networks consolidate the core concepts of evolution by natural selection. Trends Microbiol. 28, 254–265. doi:[10.1016/j.tim.2019.11.006](https://www.sciencedirect.com/science/article/pii/S0966842X19302926)  
-Van Etten, J. and Bhattacharya, D., 2020. Horizontal Gene Transfer in Eukaryotes: Not if, but How Much? Trends in Genetics, Month 2020, Vol. 36, 12, 915-925. doi:[10.1016/j.tig.2020.08.006](https://www.sciencedirect.com/science/article/abs/pii/S0168952520302067)  
## Softwares  
-Buchfink, B., Xie, C., Huson, D.H., 2014. Fast and sensitive protein alignment using DIAMOND. Nat Methods 12:59–60. doi: [10.1038/nmeth.3176](https://www.nature.com/articles/nmeth.3176)  
-R Core Team 2017. R: A language and environment for statistical computing. R Foundation for Statistical Computing, Vienna, Austria. URL https://www.R-project.org/  
-RStudio Team 2020. RStudio: Integrated Development for R. RStudio, PBC, Boston, MA URL [http://www.rstudio.com/](http://www.rstudio.com/)  
-Rognes, T., Flouri, T., Nichols, B., Quince, C., Mahé, F., 2016. VSEARCH: a versatile open source tool for metagenomics. PeerJ 4, e2584.  doi: [10.7717/peerj.2584](https://pubmed.ncbi.nlm.nih.gov/27781170/)  
-Shannon P, Markiel A, Ozier O, Baliga NS, Wang JT, Ramage D, Amin N, Schwikowski B, Ideker T. 2003 Cytoscape: a software environment for integrated models of biomolecular interaction networks. Genome Research Nov; 13(11): 2498-504. doi:[10.1101/gr.1239303](https://pubmed.ncbi.nlm.nih.gov/14597658/)  
-Van Rossum, G., & Drake, F. L. 2009. Python 3 Reference Manual. Scotts Valley, CA: CreateSpace. [https://cytoscape.org/](https://cytoscape.org/)  

## Acknowledgements
My introduction to Sequence Similarity Networks was thanks to a conversation with Alicia S. Arroyo and her very motivating [research](https://academic.oup.com/gbe/article/12/9/1664/5857131). Such interaction lead me to attend an excellent [workshop](http://www.evol-net.fr/index.php?option=com_content&view=article&id=79&Itemid=547) on SSN organized by the [AIRE team](http://www.evol-net.fr/) with Eric Bapteste, Eduardo Corel and Philippe Lopez as main researchers. Therefore I'm very grateful for their time, outstanding explanations and motivation.  


