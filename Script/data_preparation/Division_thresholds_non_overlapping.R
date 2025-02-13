library(argparse)
library(dplyr)
library(readr)

parser <- ArgumentParser(description='Creating files by dividing them into different thresholds - non-overlapping')

parser$add_argument("-i", action="store", dest = "input_file", help="input file. ")
parser$add_argument("-o",action="store", dest = "output_dir", help="output dir")


user_args <- parser$parse_args()


Liver <- read.csv(user_args$input_file)
data <- Liver

table1_high <- subset(data, EditingIndex*100 >= 1 & EditingIndex*100 < 5)
table1_low <- subset(data, EditingIndex*100 < 1)

table5_high <- subset(data, EditingIndex*100 >= 5 & EditingIndex*100 < 10)
table5_low <- subset(data, EditingIndex*100 < 5)

table10_high <- subset(data, EditingIndex*100 >= 10 & EditingIndex*100 < 15)
table10_low <- subset(data, EditingIndex*100 < 10)

table15_high <- subset(data, EditingIndex*100 >= 15)
table15_low <- subset(data, EditingIndex*100 < 15)

# Determine the minimum number of rows that can be selected for each table
n1 <- min(nrow(table1_high), nrow(table1_low))
n2 <- min(nrow(table5_high), nrow(table5_low))
n3 <- min(nrow(table10_high), nrow(table10_low))
n4 <- min(nrow(table15_high), nrow(table15_low))

n <- min(n1, n2, n3, n4) # Ensure all tables have the same number of rows

# Create the tables with the same number of rows
table1 <- rbind(table1_high[1:n, ], table1_low[1:n, ])
remaining_data <- anti_join(data, table1)
table1 <- table1 %>% mutate(yes_no_editing_site = ifelse(EditingIndex*100 >= 1, "yes", "no"))
table_1_percent <- table1 %>% select(structure,L,R,yes_no_editing_site)
write_csv(table_1_percent,file=paste0(user_args$output_dir,"/data_for_prepare_classification_1P.csv"))


table5 <- rbind(
  subset(remaining_data, EditingIndex*100 >= 5 & EditingIndex*100 < 10)[1:n, ],
  subset(remaining_data, EditingIndex*100 < 5)[1:n, ]
)

table5 <- table5 %>% mutate(yes_no_editing_site = ifelse(EditingIndex*100 >= 5, "yes", "no"))
table_5_percent <- table5 %>% select(structure,L,R,yes_no_editing_site)
write_csv(table_5_percent,file=paste0(user_args$output_dir,"/data_for_prepare_classification_5P.csv"))

remaining_data <- anti_join(remaining_data, table5)

table10 <- rbind(
  subset(remaining_data, EditingIndex*100 >= 10 & EditingIndex*100 < 15)[1:n, ],
  subset(remaining_data, EditingIndex*100 < 10)[1:n, ]
)

table10 <- table10 %>% mutate(yes_no_editing_site = ifelse(EditingIndex*100 >= 10, "yes", "no"))
table_10_percent <- table10 %>% select(structure,L,R,yes_no_editing_site)
write_csv(table_10_percent,file=paste0(user_args$output_dir,"/data_for_prepare_classification_10P.csv"))

remaining_data <- anti_join(remaining_data, table10)


table15 <- rbind(
  subset(remaining_data, EditingIndex*100 >= 15)[1:n, ],
  subset(remaining_data, EditingIndex*100 < 15)[1:n, ]
)

table15 <- table15 %>% mutate(yes_no_editing_site = ifelse(EditingIndex*100 >= 15, "yes", "no"))
table_15_percent <- table15 %>% select(structure,L,R,yes_no_editing_site)
write_csv(table_15_percent,file=paste0(user_args$output_dir,"/data_for_prepare_classification_15P.csv"))

