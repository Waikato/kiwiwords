
######
# Plot a heatmap from the embeddings evaluation
###

emb_res <- read.csv(file = "emb_res.csv",header=TRUE, sep='\t')
emb_res <- emb_res[emb_res$model=='experiments/Word2Vec',]

library(ggplot2)

emb_res$w_value <- as.factor(emb_res$w_value)
emb_res$d_value <- as.factor(emb_res$d_value)
v <- ggplot(emb_res, aes(w_value, d_value, z = med.mao.eng))
v + geom_tile(aes(fill = med.mao.eng))+ scale_fill_gradient(low="white", high="black",limits=c(0,250) )+ 
  labs(x="window size",y ="vector size", title = "Median Rank") + theme(plot.title = element_text(hjust = 0.5))

pic.name <- "tune_emb.pdf"

ggsave(pic.name)
print(paste("Plot saved to",pic.name))