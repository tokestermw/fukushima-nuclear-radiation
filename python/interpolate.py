"""
I
"""

from scipy.interpolate import Rbf

class interpolate():

    def __init__(self, lat, lon, z):
        self.lat = lat
        self.lon = lon
        self.z = z

    def set_area(self):
        """
        Set the bounding box / circle for the interpolation.
        """
        pass

    def rbf(self, pickthefunction):
        Rbf(x = self.x, y = self.y, d = self.z, function = pickthefunction)
        pass

    def idw():
        pass

    def kriging():
        pass

    def nn():
        pass
