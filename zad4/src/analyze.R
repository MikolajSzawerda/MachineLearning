library(grid)
library(data.table)
library(gridExtra)
library(grid)
library(tidyr)
library(dplyr)
library(gt)
library(gtExtras)
library(ggplot2)
library(ggalt)
library(scales)
library(ggpubr)
theme_set(theme_classic())

exec_data <- fread("../results/results2.csv")
exec_data <- data.frame(exec_data)


calculate_accuracy <- function(confusion_columns) {
  sum(as.numeric(confusion_columns[1:2]) / sum(as.numeric(confusion_columns[1:4])))
}


create_labels <- function(row) {
  param <- if (row['kernel'] == "rbf") sprintf("σ=%s", row['kernel_param']) else ""
  sprintf("Jądro: %s %s Kara: %s", row['kernel'], param, as.numeric(row['penalty_param']))
}


choose_best_by_group <- function(df) {
  df$label <- apply(df, 1, create_labels)
  df$accuracy <- apply(df[, 10:13], 1, calculate_accuracy)
  df %>%
    group_by(label) %>%
    arrange(desc(accuracy)) %>%
    filter(row_number() == 1)
}


choose_worst_by_group <- function(df) {
  df$label <- apply(df, 1, create_labels)
  df$accuracy <- apply(df[, 10:13], 1, calculate_accuracy)
  df %>%
    group_by(label) %>%
    arrange(accuracy) %>%
    filter(row_number() == 1)
}


prepare_confusion_plot <- function(row, spec) {
  row <- duplicate(row)
  confusion_matrix <- data.frame(row[10:13])
  confusion_matrix$value <- sapply(confusion_matrix, function(x) as.numeric(x))
  confusion_matrix$x <- sapply(rownames(confusion_matrix), function(x) substr(x, 1, 1))
  confusion_matrix$y <- sapply(rownames(confusion_matrix), function(x) substr(x, 2, 2))
  acc <- as.numeric(calculate_accuracy(row[10:13]))
  title <- sprintf("%s Dokładność: %s", create_labels(row), label_percent()(acc))
  gg <- ggplot(confusion_matrix, aes(confusion_matrix$y, confusion_matrix$x, fill = confusion_matrix$value)) +
    geom_tile(show.legend = FALSE) +
    geom_text(aes(label = confusion_matrix$value), color = "white", size = 4) +
    xlab("Prawdziwa wartość") +
    ylab("Przewidziana wartość") +
    ggtitle(title) +
    coord_fixed()
  ggsave(paste("../plots/", row['model_name'], "_", spec, "_.png", sep = ""), gg, width = 5, height = 5, units = "in")
}


prepare_dumbbell_plot <- function(rows) {
  rows <- duplicate(rows)
  rows$tpr <- apply(rows, 1, function(x) as.numeric(x['TP']) / (as.numeric(x['TP']) + as.numeric(x['FN'])))
  rows$fpr <- apply(rows, 1, function(x) as.numeric(x['FP']) / (as.numeric(x['TN']) + as.numeric(x['FP'])))
  rows$label <- apply(rows, 1, create_labels)
  rows <- rows[order(rows$label),]


  ggplot(rows, aes(x = fpr, xend = tpr, y = label, group = label)) +
    geom_dumbbell(color = "blue",
                  size = 0.75) +
    scale_x_continuous(label = scales::percent) +
    geom_text(data = rows, aes(x = fpr, y = label, label = label_percent()(fpr)), vjust = -0.75) +
    geom_text(data = rows, aes(x = tpr, y = label, label = label_percent()(tpr)), vjust = -0.75) +
    xlab("FPR - TPR") +
    ylab(NULL) +
    ggtitle("Współczynnik fałszywych pozytywnych do prawdziwych pozytywnych") +
    theme(plot.title = element_text(hjust = 0.5, face = "bold"),
          plot.background = element_rect(fill = "#f7f7f7"),
          panel.background = element_rect(fill = "#f7f7f7"),
          panel.grid.minor = element_blank(),
          panel.grid.major.y = element_blank(),
          panel.grid.major.x = element_line(),
          axis.ticks = element_blank(),
          legend.position = "top",
          panel.border = element_blank())
}


prepare_accuracy_plot <- function(rows) {
  rows <- duplicate(rows)
  rows$label <- apply(rows, 1, create_labels)
  rows$accuracy <- apply(rows[, 10:13], 1, calculate_accuracy)

  ggplot(rows, aes(x = label, y = accuracy)) +
    geom_bar(stat = "identity", width = .5, fill = "steelblue") +
    scale_y_continuous(label = scales::percent) +
    xlab(label = NULL) +
    ylab(label = "dokładność") +
    ggtitle("Współczynnik dokładności") +
    theme(axis.text.x = element_text(angle = 25, vjust = 0.5))
}


prepare_tpr_fpr_plot <- function(rows) {
  rows$tpr <- apply(rows, 1, function(x) as.numeric(x['TP']) / (as.numeric(x['TP']) + as.numeric(x['FN'])))
  rows$fpr <- apply(rows, 1, function(x) as.numeric(x['FP']) / (as.numeric(x['TN']) + as.numeric(x['FP'])))
  rows$Typ <- apply(rows, 1, create_labels)
  rows$accuracy <- apply(rows[, 10:13], 1, calculate_accuracy)
  ggplot(rows, aes(x = fpr, y = tpr, color = Typ)) +
    xlab("Współczynnik fałszywe-pozytywne") +
    ylab("Współczynnik prawdziwe-pozytywne") +
    ggtitle("TPR(FPR)") +
    geom_point(size = 5, alpha = 0.8) +
    theme(plot.title = element_text(hjust = 0.5, face = "bold"),
          plot.background = element_rect(fill = "#f7f7f7"),
          panel.background = element_rect(fill = "#f7f7f7"),
          panel.grid.minor = element_blank(),
          panel.grid.major.y = element_blank(),
          panel.grid.major.x = element_line(),
          axis.ticks = element_blank(),
          legend.position = "top",
          panel.border = element_blank())
}


prepare_summary_table <- function(rows) {
  rows$tpr <- apply(rows, 1, function(x) as.numeric(x['TP']) / (as.numeric(x['TP']) + as.numeric(x['FN'])))
  rows$fpr <- apply(rows, 1, function(x) as.numeric(x['FP']) / (as.numeric(x['TN']) + as.numeric(x['FP'])))
  rows$label <- apply(rows, 1, create_labels)
  rows$accuracy <- apply(rows[, 10:13], 1, calculate_accuracy)
  groups <- rows %>%
    group_by(label) %>%
    summarise(tpr_m = mean(tpr), tpr_dev = sd(tpr),
              fpr_m = mean(fpr), fpr_dev = sd(fpr),
              exec_time = mean(time), acc = label_percent()(mean(accuracy))) %>%
    arrange(desc(acc))

  groups %>%
    gt() %>%
    fmt_number(
      columns = 2:6,
      decimals = 2,
      suffixing = TRUE
    ) %>%
    cols_label(
      tpr_m = "TPR",
      fpr_m = "FPR",
      tpr_dev = "TPR σ",
      fpr_dev = "FPR σ",
      exec_time = "Czas wykonania[s]",
      acc = "Dokładność",
      label = "Typ",
    ) %>%
    tab_header("Podsumowanie wyników")
}

png("../plots/tpr_fpr_plot.png", width = 2000, height = 2000, res = 200)
prepare_tpr_fpr_plot(exec_data)
dev.off()

gtsave(prepare_summary_table(exec_data), "../plots/summary_table.png")

best <- choose_best_by_group(exec_data)
apply(best, 1, function(x) prepare_confusion_plot(x, "best"))
worst <- choose_worst_by_group(exec_data)
apply(worst, 1, function(x) prepare_confusion_plot(x, "worst"))

png("../plots/dumbbell_best.png", width = 2500, height = 2000, res = 300)
prepare_dumbbell_plot(best)
dev.off()
png("../plots/dumbbell_worst.png", width = 2500, height = 1800, res = 300)
prepare_dumbbell_plot(worst)
dev.off()

png("../plots/accuracy_best.png", width = 4000, height = 2000, res = 400)
prepare_accuracy_plot(best)
dev.off()
#
png("../plots/accuracy_worst.png", width = 4000, height = 2000, res = 400)
prepare_accuracy_plot(worst)
dev.off()
