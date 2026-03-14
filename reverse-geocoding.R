setwd("C:/Users/LENOVO/sandbox/portfolio/geomarketing-coffeeshop-palopo")
library(data.table)
library(tidygeocoder)
library(dplyr)
data
output_1 = 
  data %>%
  reverse_geocode(
    lat = lat,
    long = long,
    method = "osm",
    full_results=TRUE
)
View(output_1)
output_1_matrix  <- as.matrix(output_1)
write.csv(output_1_matrix, "dataset/rgeo-data.csv")
sapply(output_1, typeof)
fwrite(output_1, "dataset/rgeo-data.csv")

getwd()
