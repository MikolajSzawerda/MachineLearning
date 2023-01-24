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
hrbrthemes::import_roboto_condensed()

exec_data <- fread("iris.data")

a <- gather(exec_data, -V5)

# ggplot(gather(exec_data, -V5), aes(value)) +
#   geom_histogram() +
#   facet_wrap(~key, scales='free_x')

# exec_data %>%
#   ggplot(aes(fill=V5)) +
#   geom_histogram(aes(x=V4), alpha=0.6, position="identity") +
#   # geom_histogram(aes(x=V2), alpha=0.6, position="identity") +
#   facet_wrap(~V5)

exec
