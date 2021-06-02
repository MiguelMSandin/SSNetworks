#----
#---- Libraries ----

library(data.table)
library(tidyr)
library(tibble)
library(dplyr)
library(stringr)
library(reshape2)

#library(vegan)
#library(ape)

library(ggplot2)
library(ggridges)
require(scales)
library(RColorBrewer)



#----
#---- Working directory ----
setwd("~/SSNetworks-main/")
#----
#---- Network statistics ----

# Firstly we set the directory of the network properties
dir <- "nets/stats/"

# We loop through all the files so we open them all at once and change some formatting so R is happy
nets <- c()
for(i in grep("_network$", dir(dir), value=TRUE)){
  nets <- cbind(nets, fread(paste0(dir, i), header=FALSE)[,2])
}; rm(i)
nets <- as.data.frame(t(nets))
colnames(nets) <- c("file", "nnode", "nedge", "connect", "clust", "cc")
rownames(nets) <- seq(1:length(grep("_network$", dir(dir), value=TRUE)))

# Changing the name of the file for the identity thresholds we have selected
nets$fileShort <- nets$file %>% gsub(".*_", "id", .) %>% gsub("\\..*$", "", .)

# Formatting the table to ggplot input 
net <- melt(nets, id.vars=c("file", "fileShort"))
net$value <- as.numeric(net$value)

pnets <- ggplot(net, aes(x=fileShort, y=value))+
  geom_point()+
  facet_wrap(~variable, scales="free")+
  theme_bw()
pnets

dir.create("nets/plots")
pdf("nets/plots/Plot_networks_stats.pdf", width=11.69, height=8.27, paper='special')
plot(pnets)
dev.off()    
#

#----
#---- Connected Components statistics ----

rm(list=ls()[!ls() %in% c("dir")])

# basically we do the same as in the previous part but focusing only in the CCs

ccs <- c()
for(i in grep("_network_CCs$", dir(dir), value=TRUE)){
  tmp <- fread(paste0(dir, i))
  tmp$file <- as.character(i)
  ccs <- rbind(ccs, tmp)
}; rm(i, tmp)

ccs$fileShort <- ccs$file %>% gsub("\\..*", "", .) %>% gsub(".*_", "id", .)

cc <- ccs %>% group_by(file, fileShort) %>% summarise(N=length(unique(Connected_component)))


plotCCs <- ggplot(cc, aes(x=fileShort, y=N))+
  geom_point()+
  theme_bw()
plotCCs

pdf("nets/plots/Plot_CCs_number.pdf", width=11.69, height=8.27, paper='special')
plot(plotCCs)
dev.off()

# Adding attributes and exploring how the CCs are distributed ______________________________________
# Here you should change the path and name to yout attribute file __________________________________
attributes <- fread("raw/FILE.attr")

nodes <- c()
for(i in grep("_nodes$", dir(dir), value=TRUE)){
  tmp <- fread(paste0(dir, i))
  tmp$file <- as.character(i)
  nodes <- rbind(nodes, tmp)
}; rm(i, tmp)

nodes$fileShort <- nodes$file %>% gsub("\\..*", "", .) %>% gsub(".*_", "id", .)

# Pay attention to the names you have given to the sequences in the attribute file _________________
nodes <- merge(nodes, attributes, by.x="Node", by.y="seq", all.x=TRUE)
if(any(is.na(nodes))){warning("Something went wrong, please check that every node in the network file has the same name as in the attribute file!!")}


# Here you should play a bit with the attribute you have given _____________________________________
# This example is made for an attribute that could be either Environmental (Env) or Reference (Ref) 

file <- nodes %>% group_by(fileShort, Connected_component) %>% summarise(uniques=paste(unique(description), collapse="|"))
file$uniques <- fifelse(file$uniques=="Environmental"|
                          file$uniques=="Reference", file$uniques, "Mixed")
table(file$uniques)
sort(unique(file$uniques))

plotCCsAttr <- ggplot(file, aes(x=fileShort, fill=uniques))+
  geom_bar(stat="count", position=position_dodge())+
  scale_fill_manual(values=c("springgreen3", "steelblue3", "grey40"),
                    labels=c("Env", "Ref", "Both"))+
  scale_y_log10() + annotation_logticks(sides = 'l')+
  theme_bw()
plotCCsAttr

pdf("nets/plots/Plot_CCs_number_description.pdf", width=11.69, height=8.27, paper='special')
plot(plotCCsAttr)
dev.off()


#

#----
#---- Nodes centralities ----

rm(list=ls()[!ls() %in% c("dir")])

nodes <- c()
for(i in grep("_nodes$", dir(dir), value=TRUE)){
  tmp <- fread(paste0(dir, i))
  tmp$file <- as.character(i)
  nodes <- rbind(nodes, tmp)
}; rm(i, tmp)

nodes$fileShort <- nodes$file %>% gsub("\\..*", "", .) %>% gsub(".*_", "id", .)

nodes$Degree <- as.numeric(nodes$Degree)
nodes$Betweenness <- as.numeric(nodes$Betweenness)
nodes$Closeness <- as.numeric(nodes$Closeness)
nodes$Eccentricity <- as.numeric(nodes$Eccentricity)

node <- melt(nodes, id.vars=c("Connected_component", "Node", "file", "fileShort"))

bxpAll <- ggplot(node, aes(x=fileShort, y=value))+
  geom_jitter(alpha=0.6, position=position_jitter(0.3))+
  geom_boxplot(alpha=0.2)+
  facet_wrap(~variable, scales="free")+
  theme_bw()
bxpAll

pdf("nets/plots/BoxPlot_nodes_centralities.pdf", width=11.69, height=8.27, paper='special')
plot(bxpAll)
dev.off()


# Now adding colours for the attributes ____________________________________________________________

attributes <- fread("raw/FILE.attr")

nodea <- merge(node, attributes, by.x="Node", by.y="seq", all.x=TRUE)
if(any(is.na(nodes))){warning("Something went wrong, please check that every node in the network file has the same name as in the attribute file!!")}

# Choose your favorite attribute ___________________________________________________________________
bxpAtt <- ggplot(nodea, aes(x=description, y=value, fill=description))+
  geom_boxplot(alpha=0.8)+
  geom_jitter(alpha=0.2, position=position_jitter(0.3), aes(fill=description))+
  scale_fill_manual(values=c("springgreen3", "steelblue3", "grey40"))+
  facet_grid(variable~fileShort, scales="free_y")+
  theme_bw()
bxpAtt

pdf("nets/plots/BoxPlot_nodes_centralities_description.pdf", width=11.69, height=8.27, paper='special')
plot(bxpAtt)
dev.off()


#----
#---- Assortativity ----

rm(list=ls()[!ls() %in% c()])

dir <- "nets/assortativity/"

assor <- c()
for(i in grep("\\.assortativity$", dir(dir), value=TRUE)){
  tmp <- fread(paste0(dir, i))
  tmp$file <- i
  assor <- rbind(assor, tmp)
}; rm(i, tmp)

assor$fileShort <- assor$file %>% gsub("\\..*", "", .) %>% gsub(".*_", "id", .)

plotAssor <- ggplot(assor, aes(x=fileShort, y=assortativity_groups))+
  geom_point()+
  facet_wrap(~group, scales="free")+
  theme_bw()
plotAssor

pdf("nets/plots/Plot_assortativities.pdf", width=11.69, height=8.27, paper='special')
plot(plotAssor)
dev.off()


#----
#---- Shortest path ----

rm(list=ls()[!ls() %in% c()])

dir <- "nets/shortest/"

short <- c()
for(i in grep("\\.shortest$", dir(dir), value=TRUE)){
  tmp <- fread(paste0(dir, i))
  tmp$file <- as.character(i)
  short <- rbind(short, tmp)
}; rm(i, tmp)

short$fileShort <- short$file %>% gsub("\\..*", "", .) %>% gsub(".*_", "id", .)

short$shortestn <- with(short, ifelse(is.infinite(shortest), max(shortest[which(shortest < Inf)])+1, shortest))

plotShort <- ggplot(short, aes(x=shortestn, y=fileShort, fill=fileShort))+
  #geom_histogram()+
  geom_density_ridges() +
  theme_bw()
plotShort

# This is plot is very pretty, but not very informative... so we don't save it
#pdf("plots//Plot_shortest_path_reference_sequence.pdf", width=11.69, height=8.27, paper='special')
#plot(plotShort)
#dev.off()

plotShort2 <- ggplot(short, aes(x=shortestn))+
  geom_bar(aes(y=..prop.., fill=factor(..x..)), stat="count")+
  facet_wrap(~fileShort)+
  scale_y_continuous(name="Environmental nodes (%)", labels=percent_format())+
  scale_fill_brewer(palette="RdBu", direction=-1,
                    name=paste("Shortest distance to\na reference sequence\n(number of nodes)"), 
                    labels = c(seq(min(short$shortestn):(max(short$shortestn)-1)), "Inf"))+
  theme_bw()
plotShort2

pdf("nets/plots/Plot_shortest_path_reference_sequence_relative.pdf", width=11.69, height=8.27, paper='special')
plot(plotShort2)
dev.off()

plotShort3 <- ggplot(short, aes(x=shortestn))+
  geom_bar(stat="count", aes(fill=factor(shortestn)))+
  facet_wrap(~fileShort, scales="free_y")+
  scale_y_log10() + annotation_logticks(sides = 'l')+
  scale_fill_brewer(palette="RdBu", direction=-1,
                    name=paste("Shortest distance to\na reference sequence\n(number of nodes)"), 
                    labels = c(seq(min(short$shortestn):(max(short$shortestn)-1)), "Inf"))+
  theme_bw()
plotShort3

pdf("nets/plots/Plot_shortest_path_reference_sequence_absolute.pdf", width=11.69, height=8.27, paper='special')
plot(plotShort3)
dev.off()


#----
