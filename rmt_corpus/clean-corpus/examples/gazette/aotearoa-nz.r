library(data.table)
library(ggplot2)

aotearoa <- fread('aotearoa-nz.csv')

g <- ggplot(aotearoa[latitude > -47 & latitude < -34 & longitude > 165 & longitude < 180] , aes(x=longitude, y=latitude, color=reo==0, fill=reo==0)) + 
    geom_point(alpha=0.2, stroke=0, size=1) +
    coord_map() +
    theme_void() + theme(legend.position="none")

ggsave(g, filename='aotearoa-nz.png', width=10, height=15, dpi=600)
