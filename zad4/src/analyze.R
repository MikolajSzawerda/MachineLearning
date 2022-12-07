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
theme_set(theme_classic())

exec_data <- fread("../results/enriched_results.csv")
exec_data <- data.frame(exec_data)

calculate_accuracy <- function(confusion_columns){
  sum(as.numeric(confusion_columns[1:2])/sum(as.numeric(confusion_columns[1:4])))
}

create_labels <- function(row){
  param <- if (row['kernel'] == "rbf") sprintf("σ=%s", row['kernel_param']) else ""
  sprintf("Jądro: %s %s Kara:%s", row['kernel'], param, row['penalty_param'])
}

prepare_confusion_plot <- function(row) {
  confusion_matrix <- data.frame(row[10:13])
  confusion_matrix$value <- sapply(confusion_matrix, function(x) as.numeric(x))
  confusion_matrix$x <- sapply(rownames(confusion_matrix), function(x) substr(x, 1, 1))
  confusion_matrix$y <- sapply(rownames(confusion_matrix), function(x) substr(x, 2, 2))
  acc <- as.numeric(calculate_accuracy(row[10:13]))
  title <- sprintf("%s Dokładność: %s", create_labels(row), label_percent()(acc))
  ggplot(confusion_matrix, aes(confusion_matrix$y, confusion_matrix$x, fill = confusion_matrix$value)) +
    geom_tile() +
    geom_text(aes(label = confusion_matrix$value), color = "white", size = 4) +
    xlab("Prawdziwa wartość") +
    ylab("Przewidziana wartość") +
    ggtitle(title)+
    coord_fixed()

}

prepare_dumbbell_plot <- function(rows) {
  rows$tpr <- apply(rows, 1, function (x) as.numeric(x['TP'])/(as.numeric(x['TP'])+as.numeric(x['FN'])))
  rows$fpr <- apply(rows, 1, function (x) as.numeric(x['FP'])/(as.numeric(x['TN'])+as.numeric(x['FP'])))
  rows$label <- apply(rows, 1, create_labels)

  ggplot(rows, aes(x=fpr, xend=tpr, y=label, group=label)) +
    geom_dumbbell(color="#a3c4dc",
                  size=0.75,
                  point.colour.l="#0e668b") +
    scale_x_continuous(label=scales::percent) +
    geom_text(data=rows, aes(x=fpr, y=label, label=label_percent()(fpr)), vjust = -0.75)+
    geom_text(data=rows, aes(x=tpr, y=label, label=label_percent()(tpr)), vjust = -0.75)+
    xlab("FPR - TPR") +
    ylab(NULL)+
    ggtitle("Współczynnik fałszywych pozytywnych do prawdziwych pozytywnych")+
    theme(plot.title = element_text(hjust=0.5, face="bold"),
        plot.background=element_rect(fill="#f7f7f7"),
        panel.background=element_rect(fill="#f7f7f7"),
        panel.grid.minor=element_blank(),
        panel.grid.major.y=element_blank(),
        panel.grid.major.x=element_line(),
        axis.ticks=element_blank(),
        legend.position="top",
        panel.border=element_blank())
}

prepare_accuracy_plot <- function (rows){
  rows$label <- apply(rows, 1, create_labels)
  rows$accuracy <- apply(rows[,10:13], 1, calculate_accuracy)

  ggplot(rows, aes(x=label, y=accuracy))+
    geom_bar(stat="identity", width=.5, fill="steelblue") +
    scale_y_continuous(label=scales::percent) +
    xlab(label=NULL)+
    ylab(label="dokładność")+
    ggtitle("Współczynnik dokładności")+
    theme(axis.text.x = element_text(angle=25, vjust=0.5))
}

apply(exec_data, 1, prepare_confusion_plot )
# prepare_dumbbell_plot(exec_data)
# prepare_accuracy_plot(exec_data)


