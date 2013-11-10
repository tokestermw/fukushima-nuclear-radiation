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

from itertools import izip

from bisect import bisect_left

dat = pd.io.parsers.read_csv("../data/station_day_avg.csv")
dat.columns = ['station_id', 'lat', 'lon', 'date', 'radiation']

js = json.loads(open('dump.json').read())

# set data
lat = np.array([i['location']['nb'] for i in js])
lon = np.array([i['location']['ob'] for i in js])
val = np.array([i['weight'] for i in js])

# get grid
cuts = 100
lat_grd = np.linspace(min(lat), max(lat), cuts*2)
lon_grd = np.linspace(min(lon), max(lon), cuts/2)
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

## plot reshaped data to get back into json
plt.scatter(np.reshape(x, (-1, 1)), np.reshape(y, (-1, 1)), 5, np.reshape(z, (-1, 1)), cmap = cm.jet)
plt.savefig('plots/check.pdf')
plt.close()

## now interpolated dataset back into json
# i have jsonify
jsout = []
xlong = np.reshape(x, (-1, 1))
ylong = np.reshape(y, (-1, 1))
zlong = np.reshape(z, (-1, 1))
for i in xrange(cuts*cuts):
    jsout.append({'location':{'nb': xlong[i][0], 'ob': ylong[i][0]}, 'weight': zlong[i][0]})

jsout = [{'location': {'nb':i[0][0], 'ob':i[1][0]}, 'weight':i[2][0]} for i in izip(xlong, ylong, zlong)]

## now check out how I would check to see
js = json.loads(open('dump.json').read())
js2 = json.loads(open('dump2.json').read())
jsS = json.loads(open('dumpS.json').read())

lat_ind = []
lon_ind = []
for i in range(len(js2)):
    lat_rng = GRID_RANGE['lat'][0] < js2[i][1] < GRID_RANGE['lat'][1]
    lon_rng = GRID_RANGE['lon'][0] < js2[i][2] < GRID_RANGE['lon'][1]
    if lat_rng and lon_rng:
        lat_ind.append(bisect_left([k['location']['nb'] for k in jsS], js2[i][1]))
        lon_ind.append(bisect_left([k['location']['ob'] for k in jsS], js2[i][2]))
    else:
        lat_ind.append(0)
        lon_ind.append(0)

js_smoothed = []
for i in range(len(js2)):
    if lat_ind[i] == 0 and lat_ind[i] == 0:
        js_smoothed.append(0)
    else:
        js_smoothed.append(lat_ind[i])

## now let's try just picking the points
rbf = Rbf(lat, lon, val, function = "gaussian")
z = rbf(np.array([i[1] for i in js2]), np.array([i[2] for i in js2]))

