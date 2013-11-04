## -----------------------------------
## Play around with the data and plot for station_join.csv

library(data.table)

df <- read.csv("data/station_join_sub.csv", header = FALSE)
names(df) <- c("station_id", "lat", "lon", "datetime", "val")

dt <- data.table(df)
rm(df)

## group by station_id (23 of them)
dt.mean <- dt[, list(val = mean(val)), by = list(station_id)]

filt <- function(x) {
  ind <- x > 0
  mean(log(x[ind]))
}

dt.filtered_mean <- dt[, list(val = filt(val)), by = list(station_id)]

## check datetime
idatetime <- IDateTime(dt$datetime)

## plot, crap not enough dates in the summer months
plot(idatetime$idate, dt$val, pch = '.')

## -----------------------------------
## Play around with the data and plot for measurements.csv

df2 <- read.csv("data/measurements_2011_subset.csv", header = FALSE)
names(df2) <- c("datetime", "lat", "lon", "val", "type")

dt2 <- data.table(df2)
rm(df2)

idatetime2 <- IDateTime(dt2$datetime)
