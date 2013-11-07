## just like in script.R, play with models
## R explored with kriging, I'm going to explore artificial neural networks

# get subset of data

import pandas as pd
import json

import matplotlib
matplotlib.use('Agg') # don't plot in a separate window (make sure to save fig)
import matplotlib.pyplot as plt
from matplotlib import cm
#import pylab

import numpy as np

from scipy.interpolate import Rbf

dat = pd.io.parsers.read_csv("../data/station_day_avg.csv")
dat.columns = ['station_id', 'lat', 'lon', 'date', 'radiation']

js = json.loads(open('dump.json').read())

# set data
lat = np.array([i['location']['nb'] for i in js])
lon = np.array([i['location']['ob'] for i in js])
val = np.array([i['weight'] for i in js])

# get grid
cuts = 100
lat_grd = np.linspace(min(lat), max(lat), cuts)
lon_grd = np.linspace(min(lon), max(lon), cuts)
x, y = np.meshgrid(lat_grd, lon_grd)

# fit and interpolate
rbf = Rbf(lat, lon, val, function = "gaussian")
z = rbf(x, y)

# plot!
plt.subplot(1, 1, 1)
plt.pcolor(y, x, z, cmap = cm.jet)
plt.scatter(lon, lat, 30, val, cmap = cm.jet)
plt.colorbar()
plt.savefig('plots/rbf2d.pdf')
plt.close()
