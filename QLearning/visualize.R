library(data.table)
library(ggplot2)
library(scales)
library(tidyr)
library(dplyr)
library(gt)
library(gtExtras)
library(patchwork)
library(hrbrthemes)
hrbrthemes::import_roboto_condensed()

exec_data <- fread("results/experiments.csv")

prepare_time_plot <- function (data) {
  data$title <- sprintf("%s %s", data$strategy, sprintf(data$learning_rate, fmt="%#.2f"))
  ggplot(data[order(data$title)], aes(x=data$title, y=time)) +
    xlab("Eksperyment") +
    ylab("Czas[s]") +
    ggtitle("Wykres czasu wykonania") +
    theme_ipsum_rc() +
    geom_bar(stat='identity') +
    theme(
      axis.title.x = element_text(size=10),
      axis.title.y = element_text(size=10),
    )
}

prepare_summary_table <- function (data) {
  data %>%
    group_by(strategy) %>%
    select(learning_rate, time, r_m, r_std) %>%
  gt() %>%
    fmt_number(
      columns = 2:last_col(),
      decimals = 2,
      suffixing = TRUE
    ) %>%
    cols_label(
      learning_rate = "Wspł. uczenia",
      time = "Czas wykonania[s]",
      r_m = "Średnia nagroda",
      r_std = "std nagrody",
    )
}

get_experiment_points <- function(experiment){
    data <- fread(sprintf("results/%s_final.csv", experiment['filename']))
    data %>%
      transmute(strategy=experiment['strategy'],
                learning_rate=experiment['learning_rate'],
                param=experiment['param'],
                discount=experiment['discount'],
                reward=if_else(reward<0, reward/100, as.double(reward)))
}

prepare_hist_plot <- function(data){
  ggplot(data, aes(x=reward, fill=learning_rate)) +
    geom_histogram(binwidth=1, alpha=0.5, position="identity") +
    ylab("Ilość") +
    xlab("Nagroda") +
    theme_ipsum_rc() +
    theme(
      legend.position="none",
      panel.spacing = unit(0.1, "lines"),
      strip.text.x = element_text(size = 8),
      axis.title.x = element_text(size=10),
      axis.title.y = element_text(size=10),
    )
}

get_evolution_points <- function (experiment){
  data <- fread(sprintf("results/%s_episodes.csv", experiment['filename']), header=TRUE)
  points <- data %>%
    rename("it"="V1") %>%
    rowwise() %>%
    transmute(it=it*50+1,
              x_max = max(c_across(2:last_col())),
              x_min = min(c_across(2:last_col())),
              x_mean = mean(c_across(2:last_col())),
              x_std = sd(c_across(2:last_col())),
              strategy=experiment['strategy'],
              learning_rate=experiment['learning_rate'])
}

prepare_evolution_plot <- function(data) {
  ggplot(data, aes(x=it)) +
    geom_point(aes(y=x_max, colour="max"), alpha=0.5) +
    geom_point(aes(y=x_min, colour="min"), alpha=0.5) +
    scale_colour_manual(name="Legenda", values = c("max"="red", "min"="blue")) +
    ylab("Nagroda") +
    xlab("Iteracja") +
    theme_ipsum_rc() +
    theme(
      plot.title = element_text(size=15),
      axis.title.x = element_text(size=10),
      axis.title.y = element_text(size=10),
    )
}

prepare_comparison_plots <- function (data){
  discount <- sprintf(min(data["discount"]), fmt="%#.2f")
  param <- sprintf(min(data["param"]), fmt="%#.2f")
  title <- sprintf("Discount: %s Strategy param: %s", discount, param)
  filename <- sprintf("plots/comparison_%d_%d", as.integer(min(data["discount"])*10), as.integer(min(data["param"])*10))

  plt1 <- rbindlist(apply(data, 1, get_evolution_points)) %>%
    prepare_evolution_plot +
    facet_grid(strategy~learning_rate) +
    ggtitle("Zależność min/max nagrody od iteracji, współczynnika uczenia i strategii", subtitle = title)
  ggsave(sprintf("plots/comparison_%d_%d_evol.png", as.integer(min(data["discount"])*10), as.integer(min(data["param"])*10)), plt1, width = 16, height = 8, units = "in", bg="white")

  plt2 <- rbindlist(apply(data,1, get_experiment_points)) %>%
    prepare_hist_plot +
    facet_grid(strategy~learning_rate) +
    ggtitle("Histogram nagród po uczeniu w zależności od współczynnika uczenia i strategii", subtitle = title)
    ggsave(sprintf("plots/comparison_%d_%d_hist.png", as.integer(min(data["discount"])*10), as.integer(min(data["param"])*10)), plt2, width = 16, height = 8, units = "in", bg="white")

  plt3 <- prepare_time_plot(data) +
    ggtitle(label="Czas wykonania", subtitle = title)
  ggsave(sprintf("%s_time.png", filename), plt3, width = 16, height = 8, units = "in", bg="white")

  plt4 <- prepare_summary_table(data) %>%
    tab_header(title="Podsumowanie wyników", subtitle = title)
  gtsave(plt4, sprintf("%s_table.png", filename))
}


data <- exec_data %>%
  group_by(discount, param) %>%
  group_split()

lapply(data, prepare_comparison_plots)
