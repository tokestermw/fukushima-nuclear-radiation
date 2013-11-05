## -----------------------------------
## Play around with the data and plot for station_join.csv

library(data.table)

df <- read.csv("data/station_day_avg.csv", header = FALSE)
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
# stationdata.pdf
plot(idatetime$idate, dt$val, pch = '.')

## -----------------------------------
## Play around with the data and plot for measurements.csv

df2 <- read.csv("data/measurements_2011_subset.csv", header = FALSE)
names(df2) <- c("datetime", "lat", "lon", "val", "type")

dt2 <- data.table(df2)
rm(df2)

idatetime2 <- IDateTime(dt2$datetime)

## plot compare to station_join
# measurement.pdf
plot(idatetime2$idate, dt2$val, pch = '.')

## -----------------------------------
## Now go into inverse distance weighting, ordinary kriging
## http://casoilresource.lawr.ucdavis.edu/drupal/node/442

library(gstat)
library(sp)

dt.unique <- dt[, list(lat = unique(lat), lon = unique(lon)), by = list(station_id)]

e <- dt[idatetime$idate == "2011-10-28", list(lat, lon, val)]
coordinates(e) <- ~ lon + lat

# bubble.pdf
bubble(e, zcol = "val")

x.range <- seq(min(dt$lat), max(dt$lat), len = 100)
y.range <- seq(min(dt$lon), max(dt$lon), len = 100)

grd <- expand.grid(x = x.range, y = y.range)

# grid.pdf
plot(grd, cex = .2, pch = 2)
points(dt.unique[, list(lat, lon)], pch = 16, col = "red", cex = 1)

coordinates(grd) = ~ y + x
i <- idw(val ~ 1, e, grd)

# idw.pdf
spplot(i["var1.pred"], cuts = 10, scales = list(draw = TRUE),
       col.regions = heat.colors(100), pretty = TRUE, contour = TRUE)

g <- gstat(id = "radiation", formula = val ~ 1, data = e)

#plot(variogram(g, map=TRUE, cutoff=.2, width=200))

# variograms from four directions
v <- variogram(g, alpha = c(0, 45, 90, 135))

# variogram.pdf
plot(v, ylim = c(-1, max(v$gamma)))

v.fit <- fit.variogram(v, model = vgm(model = "Lin"))

## not enough spatially correlated points to get a good kriging going!

g2 <- gstat(g, id = "radiation", model = v.fit)

p <- predict(g2, model = v.fit, newdata = grd)

spplot(p, zcol = 'radiation.pred', cuts = 10, scales = list(draw = TRUE),
       col.regions = heat.colors(100), pretty = TRUE, contour = TRUE)

## get data this way
# c(p@coords, p$radiation.pred, p$radiation.var)
