#!/usr/local/bin/python

# Grab all the radiation measurements within x km of epicenter.

# Location of Fukushima Daiichi
# 37deg25'22.7'' N 141deg01' 58.5''
# 37.422972,141.032917

# Web app to translate distance on Earth
# http://www.movable-type.co.uk/scripts/latlong.html

# Wayne Dyck's implementation of the Haversine formuula
# http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/

FUKUSHIMA_DAIICHI = (37.422972, 141.032917)
RADIUS = 6371 # Earth's radius (km)

from math import radians, sin, cos, atan2, sqrt
import sys, os

def scan(startpoint, endpoint, km):
    """
    Calculate distance between two lat longs, and check to see if they are with xkm.
    Uses the Haversine formula:
      http://en.wikipedia.org/wiki/Haversine_formula

    startpoint ~ tuple (lat, lon)
    endpoint ~ tuple (lat, lon)
    km ~ distance check if smaller than km
    """
    latA, lonA = startpoint
    latB, lonB = endpoint

    dlat = radians(latB - latA)
    dlon = radians(lonB - lonA)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(latA)) \
      * cos(radians(latB)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    dist = RADIUS * c

    return km - dist > 0

def append_scan_to_data(fname, column, km):
    """
    Subsets data wrt space and outputs to *_subset.csv.
    lat, lon data need to be in consecutive columns in that order.
    """
    lat, lon = [column, column + 2]
    with open(fname) as f:
        c = open(fname[:-4] + '_subset.csv', 'w')
        next(f) # skip first header line
        for line in f:
            splt = line.split(',')
            endpoint = tuple([float(i) for i in splt[lat:lon]])
            within = scan(FUKUSHIMA_DAIICHI, endpoint, km)
            if within:
                c.write(line)

        c.close()
    return True

if __name__ == '__main__':
    print 'Make sure to remove or rename *_subset.csv first'

    script_path, fname, column, km = sys.argv
    append_scan_to_data(fname, int(column), float(km))
