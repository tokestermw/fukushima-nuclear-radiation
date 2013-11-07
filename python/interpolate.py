"""
I
"""

from scipy.interpolate import Rbf

FUKUSHIMA_DAIICHI = (37.422972, 141.032917)

class interpolate:

    def __init__(self, lat, lon, val):
        self.lat = lat
        self.lon = lon
        self.val = val

    def set_area(self):
        """
        Set the bounding box / circle for the interpolation.
        """
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
        Rbf(x = self.lat, y = self.lon, d = self.val, function = pickthefunction)
        pass

    def idw():
        pass

    def kriging():
        pass

    def nn():
        pass
