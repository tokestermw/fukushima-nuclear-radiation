"""
Grab all the radiation measurements within x km of epicenter.

Location of Fukushima Daiichi
37deg25'22.7'' N 141deg01' 58.5''
37.422972,141.032917

Web app to translate distance on Earth
http://www.movable-type.co.uk/scripts/latlong.html

Wayne Dyck's implementation of the Haversine formuula
http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/
"""

from math import radians, sin, cos, atan2, sqrt

def scan(startpoint, endpoint, km):
    """
    Calculate between two lat longs, and check to see if they are with xkm.
    Uses the Haversine formula:
      http://en.wikipedia.org/wiki/Haversine_formula

    startpoint ~ tuple (lat, lon)
    endpoint ~ tuple (lat, lon)
    km ~ distance check if smaller than km
    """
    latA, lonA = startpoint
    latB, lonB = endpoint
    radius = 6371 # Earth's radius (km)

    dlat = radians(latB - latA)
    dlon = radians(lonB - lonA)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(latA)) \
      * cos(math.radians(latB)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    dist = radius * c

    return km - dist > 0
