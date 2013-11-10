"""
I
"""
import numpy as np
from itertools import izip

from scipy.interpolate import Rbf

FUKUSHIMA_DAIICHI = (37.422972, 141.032917)

class interpolate:

    def __init__(self, lat, lon, val):
        self.lat = lat
        self.lon = lon
        self.val = val
        pass

    def set_area(self, cuts_lat, cuts_lon):
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

    def idw():
        pass

    def kriging():
        pass

    def nn():
        pass

    def convert_gmaps2json(self):
        xlong = np.reshape(self.x, (-1, 1))
        ylong = np.reshape(self.y, (-1, 1))
        zlong = np.reshape(self.z, (-1, 1))

        return [{'location': {'nb':i[0][0], 'ob':i[1][0]}, 'weight':i[2][0]} for i in izip(xlong, ylong, zlong)]
