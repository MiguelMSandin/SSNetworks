#----
#---- Libraries ----

library(data.table)
library(tidyr)
library(tibble)
library(dplyr)
library(stringr)
#library(reshape2)


#----
#---- Working directory ----
setwd("~/Desktop/Uppsala/project/dummy/")
#----
#---- Creating a nodes + attribute table ---- 

file_name <- "raw/FILE.fasta"

# From fasta
file <- seqinr::read.fasta(file_name, seqtype= "AA", as.string = T)
file <- data.frame(names=gsub(">", "", paste(seqinr::getAnnot(file))), sequence=paste(file))

# From similarity file
#file <- fread(file_name)

# Creating variables
out <- data.frame(seq=unique(file[,1])); colnames(out) <- c("seq")

# Let's consider the sequences have the following name structure: accessionNumber|taxonomy1\taxonomy2\taxonomy3\taxonomyi
# And I want to extract the Accession Number:
out$acnu <- sub("\\|.*", "", out$seq)
# the taxonomy:
out$taxo <-  sub("^..\\d+\\|","", out$seq)
# the first taxonomic group:
out$group <- out$seq %>% sub("^(([^\\|]+\\|){2}).+$","\\1", .) %>% gsub("\\|$", "", .) %>% gsub(".*\\|", "", .)
table(out$group)
# And the last taxonomic group
out$species <- sub(".*([A-Z][a-z]+)", "\\1", out$seq)

# And now I want to consider everything that has an '_X' as 'Environmental' and everything without as 'Reference' diversity
out$description <- with(out, ifelse(grepl("_X", species), "Environmental", "Reference"))
table(out$description)

# But feel free to use your imagination!

write.table(out, gsub("\\..*$", ".attr", file_name), sep="\t", row.names=FALSE, quote=FALSE)


