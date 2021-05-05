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
setwd("~/Desktop/Uppsala/project/ecoEvo/data/tsar/")
setwd("~/Desktop/Uppsala/project/ecoEvo_rads/data/pacBio/")
#----
#----
#---- Creating a nodes + attribute table ---- 

file_name <- "tsar.fasta"

# From fasta
file <- seqinr::read.fasta(file_name, seqtype= "AA", as.string = T)
file <- data.frame(names=gsub(">", "", paste(seqinr::getAnnot(file))), sequence=paste(file))

# From similarity file
#file <- fread(file_name)


# Creating variables
out <- data.frame(seq=unique(file[,1])); colnames(out) <- c("seq")

out$otu <- str_extract(out$seq, ".*Otu\\d+")
out$reads <- out$seq %>% gsub(".*Otu", "Otu", .) %>% gsub("^(([^_]+_){2}).+$", "\\1", .) %>% gsub("_$", "", .) %>% gsub(".*_", "", .)
out$reads <- as.numeric(out$reads)
summary(out$reads)
out$reads_log <- log(as.numeric(out$reads))
summary(out$reads_log)
out$assignation <- gsub(".*_", "", out$seq)
out$assignation <- factor(out$assignation, levels=c("Species", "Genus", "Family", "Order", "Class", "Subdivision", "Division", "Supergroup", "Domain"))
table(out$assignation)

out$group <- out$seq %>% gsub(".*TSAR_", "", .) %>% gsub("_.*", "", .)
table(out$group)
out$group <- with(out, fifelse(group=="Cercozoa", "Rhizaria", group))

out$subgroup <- out$seq %>% sub(".*TSAR_", "", .) %>% sub("^.*?_", "", .) %>% sub("_.*", "", .)
for(i in unique(out$group)){cat(i, ":\n", paste(names(table(subset(out, group==i)$subgroup)), sep=" "), "\n", table(subset(out, group==i)$subgroup), "\n")}; rm(i)

#out$group <- out$seq %>% gsub(".*Radiolaria_", "", .) %>% gsub("^(([^_]+_){2}).+$", "\\1", .) %>% gsub("_$", "", .)
#out$group <- fifelse(grepl("Acantharea", out$group), "Acantharea", gsub(".*_", "", out$group))
#out$group <- fifelse(grepl("Acantharea|Collodaria|Spumellarida|Nassellaria|RAD\\-A|RAD\\-B|RAD\\-C", out$group), out$group, "NA")
#out$group <- factor(out$group, levels=c("Acantharea", "Spumellarida", "Nassellaria", "Collodaria", "RAD-A", "RAD-B", "RAD-C", "NA"))
#table(out$group)

out$species <- ifelse(out$assignation=="Species" | out$assignation=="Genus", out$seq %>% sub("(.*)_\\w+", "\\1", .) %>% sub(".*([A-Z][a-z]+)", "\\1", .), NA)
table(out$species)

out$description <- with(out, ifelse(is.na(species) | grepl("_X|MAST|NASSO|Te_sp", species), "Environmental", "Reference"))
table(out$description)
out$description2 <- with(out, ifelse(description=="Environmental", paste0(group, "_Env"), as.character(group)))
table(out$description2)

out$environment <- out$seq %>% gsub(".*Otu\\d+_\\d+_", "", .) %>% gsub("_Eukaryota.*", "", .)
table(out$environment)

write.table(out, gsub("\\..*$", ".attr.tsv", file_name), sep="\t", row.names=FALSE, quote=FALSE)



      #----