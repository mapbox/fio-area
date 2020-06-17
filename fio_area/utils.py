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

    zmap = {True: 326, False: 327}

    if (maxZone - minZone + 1) > zonethresh:
        raise ValueError("Feature crosses too many zones")

    else:
        return "epsg:{0}{1}".format(zmap[is_n], ctrZone)

def densify_segment(start, end, densify=10):
    x_a, y_a = start
    x_b, y_b = end

    x = np.linspace(x_a, x_b - (x_b - x_a) / densify, densify)
    y = np.linspace(y_a, y_b - (y_b - y_a) / densify, densify)

    for xy in zip(x, y):
        yield xy



def densify_geometry(geometry, densify=10):
    """Simply interval densification"""
    if geometry["type"] == "Polygon":

        for idx, part in enumerate(geometry["coordinates"]):
            geometry["coordinates"][idx] = [c for a, b in zip(part[:-1], part[1:]) for c in densify_segment(a, b, densify=densify)]

        return geometry
def projectShapes(feature, toCRS, densify=None):
    project = partial(
        pyproj.transform, pyproj.Proj(fcrs.from_epsg(4326)), pyproj.Proj(toCRS))

    if densify is not None:
        print(densify)
        feature["geometry"] = densify_geometry(feature["geometry"], densify)

    return shpTrans(project, shape(feature["geometry"]))


def findExtrema(features):
    epsilon = 1.0e-10

    totalArr = np.array([c for f in features["geometry"]["coordinates"] for c in f])

    xMax = totalArr[:, 0].max() + epsilon
    xMin = totalArr[:, 0].min() - epsilon
    yMax = totalArr[:, 0].max() + epsilon
    yMin = totalArr[:, 0].min() - epsilon

    return [xMin, yMin, xMax, yMax]


def addArea(feature, calc_crs, densify=10):

    if calc_crs is None:
        eCode = getZone(findExtrema(feature))
    else:
        eCode = calc_crs
    area = projectShapes(feature, eCode, densify=densify).area

    return area


def _area_adder(features, calc_crs, densify=10):
    for f in features:
        areacalc = addArea(f, calc_crs, densify=densify)
        f["properties"]["area"] = areacalc
        yield f, areacalc


def _poly_filter(features):
    for f in features:
        if f["geometry"]["type"] == "MultiPolygon" or f["geometry"][
            "type"
        ] == "Polygon":
            yield f
