## cut the measurements.csv into time, lat-lon, radiation value and unit
cat ../data/measurements.csv | cut -d, -f1-5 > ../data/measurements_cut.csv

## change tsv into a csv for station_data
awk '{gsub("\t",",",$0); print;}' station_data.tsv > station_data.csv
cat ../data/station_data.csv | cut -d, -f1-3 > ../data/station_data_cut.csv

## subset data to only 2011
grep 2011- ../data/station_data_cut.csv > ../data/station_data_2011.csv
grep 2011- ../data/measurements_cut.csv > ../data/measurements_2011.csv

## remove empty measurements 
sed '/,,/d' ../data/measurements_2011.csv > ../data/measurements_2011_temp.csv && mv ../data/measurements_2011_temp.csv ../data/measurements_2011.csv

## remove the commas from Horiguchi, Hitachinaka City and Ishikawa, Mito
awk '{gsub("guchi, Hitachi", "guchi Hitachi", $0); print;}' station_id.csv > station_idtemp.csv && mv station_idtemp.csv station_id.csv
awk '{gsub("kawa, Mito", "kawa Mito", $0); print;}' station_id.csv > station_idtemp.csv && mv station_idtemp.csv station_id.csv

## remove japanese columns from station_id.csv
cat ../data/station_id.csv | cut -d, -f1,2,4,7,12,13 > ../data/station_id_cut.csv

## now run ../sql/data.sql to join the station_id and station_data

## run ../python/data.py, to subset wrt radius
../python/data.py '../data/station_join.csv' 1 50

../python/data.py '../data/measurements_2011.csv' 1 50

## get rid of all of the -999 values
sed '/-999/d' ../data/station_join_subset.csv > ../data/station_join_sub.csv

## remove all intermediate files to save harddrive space

