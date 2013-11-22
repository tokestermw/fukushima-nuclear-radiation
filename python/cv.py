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

## now get citizen data
m = c.execute("""
select lat, lon, val from measurements_thin where datetime = "2011-09-24"
""").fetchall()
m = np.array(m)

## kriging interpolate and get the average difference between the two!
smooth = interpolate(d[:,0], d[:,1], np.log(d[:,2]))
smooth.pick_points(m[:,0], m[:,1])
smooth.kriging()

np.median(np.log(m[:,2] / 300.0 * 1000.0) / smooth.z)
# 0.98836025991936916

np.mean(np.log(m[:,2] / 300.0 * 1000.0) / smooth.z)
# 0.98464300976754637

def compare_median(x):
    out = np.zeros(len(x))
    for i in range(len(x)):
        out[i] = np.median(np.log(m[:,2] / x[i] * 1000.0) / smooth.z)
    return out

# now plot median for every conversion
x = np.array(range(100, 500, 5))
y = compare_median(x)

# 270 is best
plt.plot(x, y, 'r', markersize = 10)
plt.axhline(y = 1.0, xmin = 0, xmax = 1000)
plt.ylabel("Leave One Out Cross-Validation Score")
plt.xlabel("Log(Radiation)")
plt.savefig("plots/conversion_profile.pdf")
plt.close()

