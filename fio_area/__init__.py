from functools import partial

import numpy as np
import pyproj
import fiona.crs as fcrs
from shapely.geometry import shape
from shapely.ops import transform as shpTrans


def getZone(bbox, zonethresh=3):
    minZone = int((bbox[0] + 180) // 6.0)
    ctrZone = int((((bbox[2] - bbox[0]) / 2.0 + bbox[0]) + 180) // 6.0)
    maxZone = int((bbox[2] + 180) // 6.0)

    is_n = (bbox[3] - bbox[1]) / 2.0 + bbox[1] > 0

    zmap = {
        True: 326,
        False: 327
    }

    if (maxZone - minZone + 1) > zonethresh:
        raise ValueError('Feature crosses too many zones')
    else:
        return 'epsg:{0}{1}'.format(zmap[is_n], ctrZone)


def projectShapes(feature, toCRS):
    project = partial(
        pyproj.transform,
        pyproj.Proj(fcrs.from_epsg(4326)),
        pyproj.Proj(toCRS))

    return shpTrans(project, shape(feature['geometry']))


def findExtrema(features):
    epsilon = 1.0e-10

    totalArr = np.array([c for f in features['geometry']['coordinates'] for c in f])

    xMax = totalArr[:, 0].max() + epsilon
    xMin = totalArr[:, 0].min() - epsilon
    yMax = totalArr[:, 0].max() + epsilon
    yMin = totalArr[:, 0].min() - epsilon

    return [xMin, yMin, xMax, yMax]


def addArea(feature, calc_crs):
    if calc_crs is None:
        eCode = getZone(findExtrema(feature))
    else:
        eCode = calc_crs

    area = projectShapes(feature, {'init': eCode}).area

    return area

def _area_adder(features, calc_crs):
    for f in features:
        areacalc = addArea(f, calc_crs)
        f['properties']['area'] = areacalc
        yield f, areacalc

def _poly_filter(features):
    for f in features:
        if f['geometry']['type'] == 'MultiPolygon' or f['geometry']['type'] == 'Polygon':
            yield f

