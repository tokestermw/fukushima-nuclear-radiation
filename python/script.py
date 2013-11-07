## just like in script.R, play with models
## R explored with kriging, I'm going to explore artificial neural networks

# get subset of data

import pandas as pd
import json

dat = pd.io.parsers.read_csv("../data/station_day_avg.csv")
dat.columns = ['station_id', 'lat', 'lon', 'date', 'radiation']

