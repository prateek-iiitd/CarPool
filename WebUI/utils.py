__author__ = 'prateek'

import math

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


def clusterize_latlngs(cordinates, total_distance):
    clusters = []
    reference = cordinates[0]
    clusters+=[reference]
    for i in xrange(1,len(cordinates)-1):
        if distance(reference, cordinates[i])>1:
            reference = cordinates[i]
            clusters+=[reference]
    clusters+=[cordinates[-1]]

    return clusters
