library(data.table)
library(ggplot2)
library(scales)
library(tidyr)
library(dplyr)
library(gt)
library(gtExtras)
library(patchwork)
library(hrbrthemes)
library(Hmisc)
library(gtsummary)
hrbrthemes::import_roboto_condensed()

exec_data <- fread("results.csv", header=TRUE)

calc_acc <- function(data){
  correct_sum <- data %>%
    filter(true_label==predicted_label) %>%
    summarise(sum(value))
  total_sum <- data %>%
    summarise((sum(value)))
  min(correct_sum)/min(total_sum)
}

prepapre_confusion_matrix_plot <- function(data) {
  train_data_len <- min(data$train_len)
  plt <- ggplot(data, aes(true_label, predicted_label, fill=value)) +
    geom_tile(show.legend = FALSE) +
    geom_text(aes(label = value), color = "white", size = 4) +
    xlab("Prawdziwy typ") +
    ylab("Przewidziany typ") +
    theme_ipsum_rc() +
    ggtitle(sprintf("Macierz pomyłek Dokładność: %s",
                    label_percent()(calc_acc(data))),
            subtitle = sprintf("Ilość danych treningowych: %d", train_data_len)) +
    coord_fixed() +
    theme(
      axis.title.x = element_text(size=15),
      axis.title.y = element_text(size=15),
    )
  ggsave(sprintf("plots/mat_%d.png", train_data_len), plt, bg="white", dpi=400)
}

prepare_time_plot <- function (data) {
  ggplot(data, aes(x=data$train_len, y=data$time)) +
    xlab("Eksperyment") +
    ylab("Czas[s]") +
    ggtitle("Wykres czasu wykonania od ilości danych treningowych") +
    theme_ipsum_rc() +
    scale_x_continuous(breaks = data$train_len) +
    geom_bar(stat='identity') +
    theme(
      axis.title.x = element_text(size=10),
      axis.title.y = element_text(size=10),
    )
}

prepare_acc_plot <- function(data) {
  ggplot(data, aes(x=train_len, y=acc)) +
    theme_ipsum_rc() +
    xlab("Ilość danych treningowych") +
    ylab("Dokładność") +
    ggtitle("Zależność dokładności od ilości danych treningowych") +
    geom_point(shape=21, color="black", fill="#69b3a2", size=6) +
    scale_x_continuous(breaks = data$train_len) +
    scale_y_continuous(labels = scales::percent)
}

prepare_dist_plot <- function(data) {
  data <- data %>%
    gather(key="feature", value="val", 1:4)
  ggplot(data, aes(x=val, fill=feature)) +
    geom_histogram(alpha=0.5, position="identity")+
    ylab("Ilość") +
    xlab("Wartość") +
    theme_ipsum_rc() +
    theme(
      legend.position="none",
      panel.spacing = unit(1, "lines"),
      strip.text = element_text(size = 20),
      axis.title.x = element_text(size=10),
      axis.title.y = element_text(size=10),
    ) +
    ggtitle("Rozkład wartości cech w zależności od grupy") +
    facet_grid(class~feature, scales="free_x")
}

prepare_summary_table <- function(data){
  data %>%
    tbl_summary(
      by=class,
      statistic = list(all_continuous() ~"{mean} ({sd})")
    ) %>%
    modify_caption("Średnia i wariancja cech w zależności od klasy") %>%
    as_gt()
}

exp_groups <- exec_data %>%
  group_by(train_len) %>%
  group_split()

stats <- exec_data %>%
  group_by(train_len) %>%
  summarise(
    acc=sum(value[predicted_label==true_label])/sum(value),
    time=min(time))

lapply(exp_groups, prepapre_confusion_matrix_plot)
# ggsave("plots/accuracy_plot.png", prepare_acc_plot(stats), bg="white")
# ggsave("plots/time_plot.png", prepare_time_plot(stats), bg="white")
real_data <- fread("iris.data")
ggsave("plots/distr.png", prepare_dist_plot(real_data), bg="white", height = 10, width = 15, dpi=400)
# gtsave(prepare_summary_table(real_data), "plots/summary_table.png")








