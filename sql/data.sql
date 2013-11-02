-- create and import station-data and station_id

create table station_id (station_id integer, site_id text, site_name text, prefecture_name text, lat float, lon float);
.separator ","
.import 'station_id_cut.csv' station_id

create unique index idx_id on station_id (station_id);

create table station_data (station_id integer, datetime text, val float,
foreign key (station_id) references station_id (station_id) );
.separator ","
.import 'station_data_2011.csv' station_data

create index idx_data on station_data (station_id);

-- join id with data 
create table station_join as
select sd.station_id, si.lat, si.lon, sd.datetime, sd.val
from station_data sd
left join station_id si on sd.station_id = si.station_id;

-- export
.mode csv
.output station_join.csv
select * from station_join;
.output stdout
