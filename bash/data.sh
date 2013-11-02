#!/bin/bash

## cut the measurements.csv into time, lat-lon, radiation value and unit
cat ../data/measurements.csv | cut -d, -f1-5 > ../data/measurements_cut.csv

## change tsv into a csv for station_data
awk '{gsub("\t",",",$0); print;}' station_data.tsv > station_data.csv
cat ../data/station_data.csv | cut -d, -f1-3 > ../data/station_data_cut.csv

## subset data to only 2011
grep 2011- station_data_cut.csv > station_data_2011.csv
grep 2011- measurements_cut.csv > measurements_2011.csv

## remove japanese columns from station_id.csv
cat ../data/station_id.csv | cut -d, -f1,2,4,7,12,13 > ../data/station_id_cut.csv

## subset gov data from Fukushima, Ibaraki, Miyagi,

## remove all intermediate files to save harddrive space
