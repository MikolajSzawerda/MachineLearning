library(grid)
library(data.table)
library("ggplot2")
library(gridExtra)
library(grid)
library(tidyr)


data <- fread("./results/results.csv")
diagonal_data <- data[p1_depth==p2_depth]

draw_games <- function(data) {
  game_nr <- 0
  for (i in seq_len(nrow(data))) {
    it_row <- data[i,]

    prepare_board <- function(i) {
      if (it_row[[i]] != "") {
        return(tableGrob(matrix(unlist(strsplit(it_row[[i]], split = "")), ncol = 3)))
      }
    }

    boards <- lapply(7:15, prepare_board)
    boards <- Filter(Negate(is.null), boards)
    result <- "Remis"
    if (it_row[[4]] != "draw") {
      result <- sprintf("Wygrał %s", it_row[[4]])
    }
    board_title <- sprintf("Głębokość gracza X: %s, Głębokość gracza O: %s, Wynik: %s", it_row[[2]], it_row[[3]], result)
    png(sprintf("./results/test_%s.png", game_nr), width = 600, height = 150)
    grid.arrange(grobs = boards[!is.na(boards)], nrow = 1, top = board_title)
    dev.off()
    game_nr <- game_nr + 1
  }
}

results<-data[,.(p1_depth, p2_depth, result)]
results<-spread(results, p2_depth, result)
png("./results/execution_time.png")
p<-ggplot(data=diagonal_data, mapping=aes(x=factor(p1_depth), y=time))+geom_point(color="steelblue", size=3)
p<-p+scale_y_continuous(breaks=seq(0, max(diagonal_data$time), 0.5))
p+labs(x="Głębokość", y="Czas wykonania[s]", title="Wykres czasu wykonania od głębokości")
dev.off()
png("./results/results_table.png")
grid.table(results)
dev.off()
# draw_games(diagonal_data)
