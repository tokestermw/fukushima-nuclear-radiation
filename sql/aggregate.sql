-- Prepare data for Python script filter.py

create table station_join (station_id integer, lat float, lon float, datetime text, val float);
.separator ','
.import 'station_join_sub.csv' station_join
