
######
# Plot a heatmap from the embeddings evaluation
###

emb_res <- read.csv(file = "emb_res.csv",header=TRUE, sep='\t')

emb_res <- emb_res[emb_res$model=='experiments/Word2Vec',]

library(ggplot2)

emb_res$w_value <- as.factor(emb_res$w_value)
emb_res$d_value <- as.factor(emb_res$d_value)
v <- ggplot(emb_res, aes(w_value, d_value, z = median.rank))
v + geom_tile(aes(fill = median.rank))+ scale_fill_gradient(low="white", high="black",limits=c(-10,5000) )+ 
  labs(x="window size",y ="vector size", title = "Median Rank") + theme(plot.title = element_text(hjust = 0.5))

ggsave("tune_emb.pdf")
