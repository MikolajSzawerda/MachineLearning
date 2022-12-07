library(grid)
library(data.table)
library("ggplot2")
library(gridExtra)
library(grid)
library(tidyr)
library(dplyr)
library(gt)
library(gtExtras)
library(Hmisc)
library(psych)
library(GGally)


red_data <- fread("../data/winequality-red.csv")
red_data <- data.frame(red_data)

white_data <- fread("../data/winequality-white.csv")
white_data <- data.frame(white_data)

# hist(red_data$quality)
# hist(white_data$quality)

red_data$quality <- sapply(red_data$quality, function (x) if(x>5) 1 else -1)
white_data$quality <- sapply(white_data$quality, function (x) if(x>5) 1 else -1)

hist(red_data$quality)
hist(white_data$quality)

write.csv(red_data, "../data/winedata-red_mapped.csv")
write.csv(white_data, "../data/winedata-white_mapped.csv")
write.csv(rbind(red_data, white_data), "../data/winedata_mapped.csv")

# red_data['color'] <- 1
# white_data['color'] <- -1
#
# data <- rbind(red_data, white_data)
# shuffled_data <- data[sample(seq_len(nrow(data))), ]
#
# write.csv(shuffled_data, "../data/winedata.csv")
#
