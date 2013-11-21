import numpy as np
import sqlite3 as sql
import matplotlib.pyplot as plt
import seaborn
from interpolate import interpolate 

## kriging cross validation
def cv(lat, lon, val, model_par):
    results = np.array([])
    for k in range(len(lat)): # leave one out cross validation
        mask = [i for i in range(len(lat)) if i != k]
        ok = kriging.OK(lat[mask], lon[mask], val[mask])
        ok.krige(lat[k], lon[k], model_par, 'exponential')
        z_smoothed = ok.Zg
        results = np.append(results, (z_smoothed - val[k])**2)
    return results

conn = sql.connect("../data/final.db")

c = conn.cursor()

d = c.execute("""
select lat, lon, val from station_day_avg where datetime = "2011-09-24"
""").fetchall()
d = np.array(d)

model_par = {} # parameters of the model (trained beforehand)
model_par['nugget'] = 0
model_par['range'] = 1
model_par['sill'] = 2.0

out_cv = cv(d[:,0], d[:,1], np.log(d[:,2]), model_par)

## plot level of val vs cv score
plt.plot(np.log(d[:,2]), out_cv, 'ro', markersize = 10)
plt.ylabel("Leave One Out Cross-Validation Score")
plt.xlabel("Log(Radiation)")
plt.savefig("plots/cv_vs_val.pdf")
plt.close()

## plot lat and lon vs cv score
plt.scatter(d[:,1], d[:,0], s = out_cv*500, alpha = .5)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("plots/cv_vs_latlon.pdf")
plt.close()

## correlation between methods

## performance between methods wrt to lat, lon
model = interpolate(d[:,0], d[:,1], np.log(d[:,2]))


## universal kriging or regression since central mean (so see error at the highest point)
