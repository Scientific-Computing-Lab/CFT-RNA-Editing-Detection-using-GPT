library(argparse)
library(dplyr)
library(readr)

parser <- ArgumentParser(description='Creating files by dividing them into different thresholds')

parser$add_argument("-i", action="store", dest = "input_file", help="input file. ")
parser$add_argument("-o",action="store", dest = "output_dir", help="output dir")


user_args <- parser$parse_args()


Liver <- read.csv(user_args$input_file)

precenet = 15

# Add "yes"/"no" column based on 15% threshold
data_15 <- Liver %>%
  mutate(Above_15_Percent = ifelse(EditingIndex*100 >= precenet, "yes", "no"))

# Separate rows into "yes" and "no" for the 1% table
yes_rows_15 <- data_15 %>% filter(Above_15_Percent == "yes")
no_rows_15 <- data_15 %>% filter(Above_15_Percent == "no")

# Randomly sample an equal number of "no" rows
sampled_no_rows_15 <- no_rows_15 %>% sample_n(nrow(yes_rows_15), replace = FALSE)

# Combine "yes" and sampled "no" rows for the 15% table
table_15_percent <- bind_rows(yes_rows_15, sampled_no_rows_15) %>%
  mutate(yes_no_editing_site = ifelse(EditingIndex*100 >= precenet, "yes", "no"))

site_15_percent <- table_15_percent %>% select(structure,L,R,yes_no_editing_site)
write_csv(site_15_percent,file=paste0(user_args$output_dir,"/data_for_prepare_classification_15P.csv"))

all_site <-  table_15_percent %>% select(-yes_no_editing_site,-Above_15_Percent)
site_1_percent <- all_site %>% mutate(yes_no_editing_site = ifelse(EditingIndex*100 >= 1, "yes", "no")) %>% select(structure,L,R,yes_no_editing_site)
write_csv(site_15_percent,file=paste0(user_args$output_dir,"/data_for_prepare_classification_1P.csv"))

site_5_percent <- all_site %>% mutate(yes_no_editing_site = ifelse(EditingIndex*100 >= 5, "yes", "no")) %>% select(structure,L,R,yes_no_editing_site)
write_csv(site_15_percent,file=paste0(user_args$output_dir,"/data_for_prepare_classification_5P.csv"))

site_10_percent <- all_site %>% mutate(yes_no_editing_site = ifelse(EditingIndex*100 >= 10, "yes", "no")) %>% select(structure,L,R,yes_no_editing_site)
write_csv(site_15_percent,file=paste0(user_args$output_dir,"/data_for_prepare_classification_10P.csv"))

