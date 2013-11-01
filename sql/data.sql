-- join the lat lons of station_data_2011.csv and station_id.csv
create table station_data(station_id text, datetime text, val float)
.separator ","
.import 'station_data_2011.csv' station_data

create table station_id(station_id text, site_id text, site_name text, prefecture_name text, lat float, lon float);
.import 'station_id_cut.csv' station_id

## convert station_id to lat lon
