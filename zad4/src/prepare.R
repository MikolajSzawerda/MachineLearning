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


red_data['color'] <- 1
white_data['color'] <- -1

data <- rbind(red_data, white_data)
shuffled_data <- data[sample(seq_len(nrow(data))), ]

write.csv(shuffled_data, "../data/winedata.csv")

