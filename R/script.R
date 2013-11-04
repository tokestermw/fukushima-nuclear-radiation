## Play around with the data and plot

library(data.table)

df <- read.csv("data/station_join_subset.csv", header = FALSE)
names(df) <- c("station_id", "lat", "lon", "datetime", "val")

dt <- data.table(df)
rm(df)

# group by station_id
dt.mean <- dt[, list(val = mean(val)), by = list(station_id)]

filt <- function(x) {
  ind <- x > 0
  mean(log(x[ind]))
}

dt.filtered_mean <- dt[, list(val = filt(val)), by = list(station_id)]
