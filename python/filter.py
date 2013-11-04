# Group by dates while putting a filter for a couple reasons:
# 1. reduce the dataset for interpolation
# 2. reduce the dataset for the maps
# 3. reduce autocorrelation for the interpolation
# 4. provide a way to play with different filters

import sqlite3 as sql
import math
import numpy as np

conn = sql.connect("../data/station_join.db")

conn.create_function('log', 1, np.log)

def filt(x):
    # use a numpy array
    ind = x > 0.0
    return np.mean(np.log(x[ind]))

conn.create_function('filter', 1, filt)

c = conn.cursor()

class Filter:

    def __init__(self, group_type):
        self.group_type = group_type
        pass

    def avg():
        pass
