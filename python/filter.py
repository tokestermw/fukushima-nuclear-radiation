# Group by dates while putting a filter for a couple reasons:
# 1. reduce the dataset for interpolation
# 2. reduce the dataset for the maps
# 3. reduce autocorrelation for the interpolation
# 4. provide a way to play with different filters
# 5. kriging just doesn't perform well with duplicate points!

import sqlite3 as sql
import math

conn = sql.connect("../data/station_join.db")

conn.create_function('log', 1, math.log)

c = conn.cursor()

## now average group by station_id and date
# get rid of quotes around the date strings
c.execute("""
update station_join set datetime=trim(replace(datetime, """", ""));
""")

# make it a date
c.execute("""
update station_join set datetime=strftime('%Y-%m-%d', datetime);
""")

# now take average -> log, group by day
c.execute("""
create table station_day_avg as
select station_id, lat, lon, datetime, avg(log(val)) from station_join
group by datetime, station_id;
""")

# then output to a csv
c.execute("""
.mode csv
.output station_day_avg.csv
select * from station_day_avg;
.output stdout
""")

conn.commit()

c.close()
conn.close()

## --
conn = sql.connect("../data/measurements_2011.db")

conn.create_function('log', 1, math.log)

c = conn.cursor()

# make it a date
c.execute("""
update measurements set datetime=strftime('%Y-%m-%d', datetime);
""")

c.execute("""
update measurements set val=log(val);
""")

# then output to a csv
c.execute("""
.mode csv
.output measurements_sub.csv
select * from measurements;
.output stdout
""")

conn.commit()

c.close()
conn.close()
