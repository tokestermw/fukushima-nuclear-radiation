"""

"""
import numpy as np
import pdb

class IDW:

    def __init__(self, lat, lon, val):
        self.lat = lat
        self.lon = lon
        self.val = val

    def inverse_distance_weighting(self, x, y):
        dist = distance_matrix(self.lat, self.lon, x, y)

        # In IDW, weights are 1 / distance
        weights = 1.0 / dist

        # Make weights sum to one
        weights /= weights.sum(axis=0)

        # Multiply the weights for each interpolated point by all observed Z-values
        self.z = np.dot(weights.T, self.val)
        pass

def distance_matrix(x0, y0, x1, y1):
    obs = np.vstack((x0, y0)).T
    interp = np.vstack((x1, y1)).T

    d0 = np.subtract.outer(obs[:,0], interp[:,0])
    d1 = np.subtract.outer(obs[:,1], interp[:,1])

    return np.hypot(d0, d1)
