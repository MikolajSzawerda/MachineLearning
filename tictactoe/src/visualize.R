library(grid)
library(data.table)
library("ggplot2")
library(gridExtra)
library(grid)
library(tidyr)
library(dplyr)
library(gt)
library(gtExtras)

data <- fread("./results/results.csv")


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
    png(sprintf("./results/game_%s.png", game_nr), width = 1600, height = 400, res = 200)
    grid.arrange(grobs = boards[!is.na(boards)], nrow = 1, top = board_title)
    dev.off()
    game_nr <- game_nr + 1
  }
}

group_games <- function(group) {
  result <- data.frame(head(group, 1))
  groupped <- sapply(group$result, function(x) if (x == "x") 1.0 else if (x == "o") 0.0 else 0.5)
  return(dplyr::tibble(
    p1_depth = list(result[1, 1]),
    p2_depth = list(result[1, 2]),
    result = list(groupped)
  ))
}

results <- data[, .(p1_depth, p2_depth, result)]
accumulated <- results %>%
  group_by(p1_depth, p2_depth)
groups <- rbindlist(lapply(group_split(accumulated), group_games), use.names = TRUE)

compare_table <- spread(groups, p2_depth, result)
colnames(compare_table)[1] <- "Głębokość gracza X"
compare_table_plt <- compare_table %>%
  gt() %>%
  gt_plt_winloss('1') %>%
  gt_plt_winloss('2') %>%
  gt_plt_winloss('3') %>%
  gt_plt_winloss('4') %>%
  gt_plt_winloss('5') %>%
  gt_plt_winloss('6') %>%
  gt_plt_winloss('7') %>%
  gt_plt_winloss('8') %>%
  gt_plt_winloss('9') %>%
  tab_options(data_row.padding = px(2)) %>%
  cols_align(align = 'left') %>%
  tab_spanner(label = "Głębokość gracza O", columns = 2:10) %>%
  tab_header(
    title = md("Rezultaty gier w zależności od głębokości poszczególnych graczy"),
    subtitle = md("<span style=\"color:blue\">Wygrana X</span> <span style=\"color:red\">Wygrana O</span> <span style=\"color:grey\">Remis</span>")
  )
gtsave(compare_table_plt, "compare_table.png", "./results")

valuable_games <- data[V1 %in% c(0, 6, 134, 1085, 1115, 366, 1214)]
draw_games(valuable_games)

diagonal_data <- data[p1_depth == p2_depth] %>%
  group_by(p1_depth, p2_depth) %>%
  summarise(mean_time = mean(time), .groups = 'drop')

png("./results/execution_time.png", width = 1500, height = 1500, res = 200)
p <- ggplot(data = diagonal_data, mapping = aes(x = factor(p1_depth), y = mean_time)) + geom_point(color = "steelblue", size = 3)
p <- p + scale_y_continuous(breaks = seq(0, max(diagonal_data$mean_time), 0.25))
p + labs(x = "Głębokość", y = "Czas wykonania[s]", title = "Wykres czasu wykonania od głębokości")
dev.off()

