"""
I
"""
import numpy as np
from itertools import izip

from scipy.interpolate import Rbf
from kriging import OK
from idw import IDW

FUKUSHIMA_DAIICHI = (37.422972, 141.032917)

class interpolate:

    def __init__(self, lat, lon, val):
        self.lat = lat
        self.lon = lon
        self.val = val
        pass

    def set_grid(self, cuts_lat, cuts_lon):
        """
        Set the bounding box / circle for the interpolation.
        """
        self.lat_grd = np.linspace(min(self.lat), max(self.lat), cuts_lat)
        self.lon_grd = np.linspace(min(self.lon), max(self.lon), cuts_lon)
        x, y = np.meshgrid(self.lat_grd, self.lon_grd)
        self.x = x
        self.y = y
        pass

    def pick_points(self, pick_x, pick_y):
        self.x = pick_x
        self.y = pick_y
        pass

    def rbf(self, pickthefunction = "gaussian"):
        """
        Options for pickthefunction
        'multiquadric': sqrt((r/self.epsilon)**2 + 1)
        'inverse': 1.0/sqrt((r/self.epsilon)**2 + 1)
        'gaussian': exp(-(r/self.epsilon)**2)
        'linear': r
        'cubic': r**3
        'quintic': r**5
        'thin_plate': r**2 * log(r)

        Links
        http://www.altdevblogaday.com/2011/09/04/interpolation-using-radial-basis-functions/
        http://wiki.scipy.org/Cookbook/RadialBasisFunctions
        """
        rbf = Rbf(self.lat, self.lon, self.val, function = pickthefunction)
        self.z = rbf(self.x, self.y)
        pass

    def simple_idw(self):
        """
        Simple inverse distance weighting.
        """
        idw = IDW(self.lat, self.lon, self.val)
        idw.inverse_distance_weighting(self.x, self.y)
        self.z = idw.z
        pass

    def kriging(self, pickthefunction = 'exponential'):
        """
        n ~ nugget, s ~ slope or sill, l ~ lags, r ~ range
        if model_type == 'spherical':
            G = n + (s*(1.5*l/r - 0.5*(l/r)**3)*(l<=r) + s*(l>r))
        elif model_type == 'linear':
            G = n + s*l
        elif model_type == 'exponential':
            G = n + s*(1 - np.exp(-3*l/r))
        """
        ok = OK(self.lat, self.lon, self.val)

        model_par = {} # parameters of the model (trained beforehand)
        model_par['nugget'] = 0
        model_par['range'] = 1
        model_par['sill'] = 2.0

        ok.krige(self.x, self.y, model_par, pickthefunction)
        self.z = ok.Zg
        self.s2_k = ok.s2_k
        pass

    def nn():
        pass

    def convert_gmaps2json(self):
        xlong = np.reshape(self.x, (-1, 1))
        ylong = np.reshape(self.y, (-1, 1))
        zlong = np.reshape(self.z, (-1, 1))

        return [{'location': {'nb':i[0][0], 'ob':i[1][0]}, 'weight':i[2][0]} for i in izip(xlong, ylong, zlong)]


def cv(choice, lat, lon, val):
    """
    Leave one out cross validation, returns MSE.
    """
    results = np.array([])
    for k in range(len(lat)):
        mask = [i for i in range(len(lat)) if i != k]
        model = interpolate(lat[mask], lon[mask], val[mask])
        model.pick_points(lat[k], lon[k])
        if choice == "Inverse Distance Weighting":
            model.simple_idw()
        elif choice == "Radial Basis Network":
            model.rbf()
        elif choice == "Ordinary Kriging":
            model.kriging()
        else:
            pass
        results = np.append(results, model.z)

    return results.mean()
