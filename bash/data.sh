#!/bin/bash

## cut the measurements.csv into time, lat-lon, radiation value and unit
cat ../data/measurements.csv | cut -d, -f1-5 > ../data/measurements_cut.csv

## change tsv into a csv for station_data
awk '{gsub("\t",",",$0); print;}' station_data.tsv > station_data.csv
station_data_cut.csv

## subset data to only 2011
grep 2011- station_data.csv > station_data_2011.csv
grep 2011- measurements_cut.csv > measurements_2011.csv


## subset gov data from Fukushima, Ibaraki, Miyagi,

## convert station_id to lat lon
