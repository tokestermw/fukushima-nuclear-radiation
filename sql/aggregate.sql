-- Prepare data for Python script filter.py

create table station_join (station_id integer, lat float, lon float, datetime text, val float);
.separator ','
.import 'station_join_sub.csv' station_join

create table measurements (datetime text, lat float, lon float, val float, typ text);
.separator ','
.import 'measurements_2011_subset.csv' measurements
