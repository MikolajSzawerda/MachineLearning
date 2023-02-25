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


red_data$quality <- sapply(red_data$quality, function(x) if (x > 5) 1 else -1)
white_data$quality <- sapply(white_data$quality, function(x) if (x > 5) 1 else -1)


red_data <- red_data[sample(seq_len(nrow(red_data))),]
write.csv(red_data, "../data/winedata-red_mapped.csv")
white_data <- white_data[sample(seq_len(nrow(white_data))),]
write.csv(white_data, "../data/winedata-white_mapped.csv")
comb <- rbind(red_data, white_data)
write.csv(comb[sample(seq_len(nrow(comb))),], "../data/winedata_mapped.csv")

png("../plots/data_histograms.png", width = 2000, height = 1500, res = 200)
hist.data.frame(comb)
dev.off()

summary <- t(as.data.frame(apply(comb, 2, summary)))
names <- list(rownames(summary))
summary <- data.table(summary)
summary$name <- names
tb <- summary[, c(7, 1, 4, 6)] %>%
  gt() %>%
  tab_header("Charakterystyka cech")
gtsave(tb, "../plots/data_summary.png")

