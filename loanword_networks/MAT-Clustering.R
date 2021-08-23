library(ggplot2)
library(factoextra)
library(dendextend)
library(pvclust)

#Load datasets
MATReducedBinary <- read.csv("~/Side Projects/Linguistics/Final Data/Data/MATFinal.csv", sep=";")
MATReducedBinary = MATReducedBinary[1:194,]

#Obtain words in correct format
words1 = colnames(MATReducedBinary[,-(1:4)])

words = gsub('\\.', ' ', words1)
words[36] = "(te) reo"
words[37] = "(te) reo maori"
words[11] = "kaupapa (maori)"
words[16] = "kohanga (reo)"
#words[30] = "tikanga (maori)"
words[14] = "ki-o-rahi"

data.hc1 = MATReducedBinary[,5:ncol(MATReducedBinary)]
data.hc = t(data.hc1)

#Create histogram of points
sum.hist = rowSums(data.hc)
data.hist = data.frame(freq = sum.hist , word = names(sum.hist))
data.hist = data.hist[order(data.hist$freq, decreasing = T),]
labels = data.hist$word[1:20]
labels[13] = "(te) reo"
labels[17] = "(te) reo maori"
labels[19] = "Kaupapa (maori)"
p<-ggplot(data=data.hist[1:20,], aes(x = reorder(word[1:20],-freq[1:20]), y= freq[1:20])) +
  geom_bar(stat="identity", color = "blue", fill = "white") + theme(axis.text.x=element_text(angle=45, hjust=1),plot.title = element_text(hjust = 0.5))
p + xlab("Word") + ylab("Count") + ggtitle("Number of Articles each Loanword Appears in \n(showing the top 20 words) ") +
  scale_x_discrete(labels=labels)

#Remove Outliers Maori 
maori.idx = which(rownames(data.hc)=='maori')
words = words[-which(words=='maori')]

data.nomaori = data.hc[-maori.idx,]
data.hc = data.nomaori

#Assess Clustering Tendancies
(hopskins_stat = get_clust_tendency(data.hc, n=25)$hopkins_stat)


bin.dist = dist(data.hc, method = 'binary')
fviz_dist(bin.dist, gradient = list(low = "#00AFBB", mid = "white", high = "#FC4E07"))

#Compute Clustering
model.hc = hcut(bin.dist,  isdiss=T, hc_method = "ward.D2")
#model.hc = hcut(t(data.hc))

#Create Dendrogram
dend2 = as.dendrogram(model.hc)
#Reorder labels to dendrogram
words_dend = words[order.dendrogram(dend2)]

#Check clustering result
check = pvclust(t(data.hc), method.dist ='binary', method.hclust = "ward.D2", nboot = 1000)
labels(check$hclust) = words_dend
png("C:/Users/jrg22/Documents/Side Projects/Linguistics/Final Data/FigureMAT/dend-pvclust-mat-nomaori.png", width =730 , height = 420, res = 72)
plot(check, hang = -1, print.num = F, main = "")
pvrect(check,alpha=0.95, pv="au")
dev.off()




#Load in loanword properties
properties <- read.csv("~/Side Projects/Linguistics/Final Data/Data/MATFinal-cat.csv", sep=";")
properties = properties[1:44,]
idx.mat = which(properties$loan == 'maori')
loanword.properties = properties[-idx.mat,]

unique(loanword.properties$semantic_domain)

#Colour by semantic domain
col = rep(1,nrow(loanword.properties))
col[which(loanword.properties$semantic_domain== "MC")] = "#00B7DA"
col[which(loanword.properties$semantic_domain== "PN")] = "#F97743"
col[which(loanword.properties$semantic_domain== "FF")] = "#28B36A"
col[which(loanword.properties$semantic_domain== "SC")] = "#9A96E5"

col = col[order.dendrogram(dend2)]


#labels_colors(dend2)  = col
dend2 <- set(dend2, "labels_cex", 0.8)
dend2 <- set(dend2,"leaves_pch", 19)

dend2 <- set(dend2,"leaves_col", col)
dend2 <- set(dend2,"branches_col",5)
#dend2 <- set(dend2,"by_labels_branches_col", value = 2, type = "any")
dend2 <-colour_branches(dend2, col=col)
dend2 <-  set(dend2,"by_labels_branches_col", 
              value = rownames(data.hc)[which(loanword.properties$semantic_domain=="MC")], 
              type = "any",TF_values = c("#00B7DA",Inf))
dend2 <-  set(dend2,"by_labels_branches_col", 
              value = rownames(data.hc)[which(loanword.properties$semantic_domain=="PN")], 
              type = "any",TF_values = c("#F97743",Inf))
dend2 <-  set(dend2,"by_labels_branches_col", value = rownames(data.hc)[which(loanword.properties$semantic_domain=="FF")],
              type = "any",TF_values = c("#28B36A",Inf))
dend2 <-  set(dend2,"by_labels_branches_col", value = rownames(data.hc)[which(loanword.properties$semantic_domain=="SC")],
              type = "any",TF_values = c("#9A96E5",Inf))
dend2 <- set(dend2, "labels", words_dend)
#get_leaves_nodePar(dend2)[[1]]
png("C:/Users/jrg22/Documents/Side Projects/Linguistics/Final Data/FigureMAT/dend-mat-sd.png", width =9, height = 4.8, units = "in", res = 72)
par(mar=c(8,2,1,1)) 
plot(dend2, type = "rectangle", ylim = c(0,1.8), xlim = c(-1,44), cex = 2)
legend(20,1.8,legend = c("MC","PN","FF","SC"), col = c( "#00B7DA","#F97743","#28B36A","#9A96E5"), pch = 16, title = "Semantic Domain", horiz = T)
dev.off()




#Colour by Borrowing Type

dend2 = as.dendrogram(model.hc)

unique(loanword.properties$borrowing_type)

col = rep(1,nrow(loanword.properties))

col[which(loanword.properties$borrowing_type== "core")] = "#28B36A"
col[which(loanword.properties$borrowing_type== "proper noun")] = "#F97743"
col[which(loanword.properties$borrowing_type== "cultural")] = "#9A96E5"

col = col[order.dendrogram(dend2)]
words_dend = words[order.dendrogram(dend2)]
par(mar=c(8,2,1,1)) 
#labels_colors(dend2)  = col
dend2 <- set(dend2, "labels_cex", 0.8)
dend2 <- set(dend2,"leaves_pch", 19)

dend2 <- set(dend2,"leaves_col", col)
dend2 <- set(dend2,"branches_col",5)
#dend2 <- set(dend2,"by_labels_branches_col", value = 2, type = "any")
dend2 <-colour_branches(dend2, col=col)

dend2 <-  set(dend2,"by_labels_branches_col", 
              value = rownames(data.hc)[which(loanword.properties$borrowing_type=="core")], 
              type = "any",TF_values = c("#F97743",Inf))
dend2 <-  set(dend2,"by_labels_branches_col", value = rownames(data.hc)[which(loanword.properties$borrowing_type=="proper noun")],
              type = "any",TF_values = c("#28B36A",Inf))
dend2 <-  set(dend2,"by_labels_branches_col", value = rownames(data.hc)[which(loanword.properties$borrowing_type=="cultural")],
              type = "any",TF_values = c("#9A96E5",Inf))
dend2 <- set(dend2, "labels", words_dend)
#get_leaves_nodePar(dend2)[[1]]
#get_leaves_nodePar(dend2)[[1]]
png("C:/Users/jrg22/Documents/Side Projects/Linguistics/Final Data/FigureMAT/dend-mat-bt.png", width =9, height = 4.8, units = "in", res = 72)
par(mar=c(8,2,1,1)) 
plot(dend2, type = "rectangle", ylim = c(0,1.8), xlim = c(-1,44), cex = 2)
legend(20,1.8,legend = c("core","proper noun","cultural"), col = c("#28B36A","#F97743","#9A96E5"), pch = 16, title = "Borrowing Type", horiz = T)
dev.off()





#Colour by Borrowing Type

dend2 = as.dendrogram(model.hc)
#plot(dend2, horiz = T)
unique(loanword.properties$listedness)

col = rep(1,nrow(loanword.properties))

col[which(loanword.properties$listedness== "YES")] = "#EE7993"
col[which(loanword.properties$listednes== "NO")] = "#3FB170"


col = col[order.dendrogram(dend2)]
words_dend = words[order.dendrogram(dend2)]
par(mar=c(8,2,1,1)) 
#labels_colors(dend2)  = col
dend2 <- set(dend2, "labels_cex", 0.8)
dend2 <- set(dend2,"leaves_pch", 19)

dend2 <- set(dend2,"leaves_col", col)
dend2 <- set(dend2,"branches_col",5)
#dend2 <- set(dend2,"by_labels_branches_col", value = 2, type = "any")
dend2 <-colour_branches(dend2, col=col)


dend2 <-  set(dend2,"by_labels_branches_col", value = rownames(data.hc)[which(loanword.properties$listednes=="NO")],
              type = "any",TF_values = c("#3FB170",Inf))
dend2 <-  set(dend2,"by_labels_branches_col", 
              value = rownames(data.hc)[which(loanword.properties$listednes=="YES")], 
              type = "any",TF_values = c("#EE7993",Inf))
dend2 <- set(dend2, "labels", words_dend)
#get_leaves_nodePar(dend2)[[1]]

png("C:/Users/jrg22/Documents/Side Projects/Linguistics/Final Data/FigureMAT/dend-mat-list.png", width =9, height = 4.8, units = "in", res = 72)
par(mar=c(8,2,1,1)) 
plot(dend2, type = "rectangle", ylim = c(0,1.8), xlim = c(-1,44), cex = 2)
legend(20,1.8,legend = c("Yes","No"), col = c("#EE7993","#3FB170"), pch = 16, title = "Listedness", horiz = T)
dev.off()


#Colour by Size
dend2 = as.dendrogram(model.hc)
#plot(dend2, horiz = T)
unique(loanword.properties$size)

col = rep(1,nrow(loanword.properties))

col[which(loanword.properties$size== 1)] = "#9A96E5"
col[which(loanword.properties$size== 2)] = "#F97743"
col[which(loanword.properties$size== 3)] = "#28B36A"
col[which(loanword.properties$size== 6)] = "#00B7DA"
col[which(loanword.properties$size== 7)] = "#FFFF00"

col = col[order.dendrogram(dend2)]
words_dend = words[order.dendrogram(dend2)]
par(mar=c(8,2,1,1)) 
#labels_colors(dend2)  = col
dend2 <- set(dend2, "labels_cex", 0.8)
dend2 <- set(dend2,"leaves_pch", 19)

dend2 <- set(dend2,"leaves_col", col)
dend2 <- set(dend2,"branches_col",5)
#dend2 <- set(dend2,"by_labels_branches_col", value = 2, type = "any")
dend2 <-colour_branches(dend2, col=col)



dend2 <-  set(dend2,"by_labels_branches_col", 
              value = rownames(data.hc)[which(loanword.properties$size==6)], 
              type = "any",TF_values = c("#00B7DA",Inf))
dend2 <-  set(dend2,"by_labels_branches_col", 
              value = rownames(data.hc)[which(loanword.properties$size==7)], 
              type = "any",TF_values = c("#FFFF00",Inf))

dend2 <-  set(dend2,"by_labels_branches_col", 
              value = rownames(data.hc)[which(loanword.properties$size==3)], 
              type = "any",TF_values = c("#28B36A",Inf))
dend2 <-  set(dend2,"by_labels_branches_col", 
              value = rownames(data.hc)[which(loanword.properties$size==2)], 
              type = "any",TF_values = c("#F97743",Inf))
dend2 <-  set(dend2,"by_labels_branches_col", 
              value = rownames(data.hc)[which(loanword.properties$size==1)], 
              type = "any",TF_values = c("#9A96E5",Inf))
dend2 <- set(dend2, "labels", words_dend)
#get_leaves_nodePar(dend2)[[1]]

png("C:/Users/jrg22/Documents/Side Projects/Linguistics/Final Data/FigureMAT/dend-mat-size.png", width =9, height = 4.8, units = "in", res = 72)
par(mar=c(8,2,1,1)) 
plot(dend2, type = "rectangle", ylim = c(0,1.8), xlim = c(-1,44), cex = 1)
legend(20,1.8,legend = c(1,2,3,6,7), col = c("#9A96E5","#F97743","#28B36A","#00B7DA","#FFFF00"), pch = 16, title = "Size", horiz = T)
dev.off()
