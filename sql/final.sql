-- get data into the 

create table station_day_avg (station_id integer, lat float, lon float, datetime text, val float);
.separator ','
.import 'station_day_avg.csv' station_day_avg

create table measurements_thin (datetime text, lat float, lon float, val float, typ text);
.separator ','
.import 'measurements_thin.csv' measurements_thin
