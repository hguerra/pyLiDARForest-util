import json
import logging
import os
from re import search

from osgeo import ogr

from app.db.update.update_columns import UpdateTable


def directories(path):
    has_prefix = lambda name: name.startswith("T-")
    absolutepath = lambda name: os.path.join(path, name)
    return {
        UpdateTable.extract_number(dirname): absolutepath(dirname)
        for dirname in os.listdir(path)
        if os.path.isdir(absolutepath(dirname)) and has_prefix(dirname)
    }


def boudingbox_path(number, transect_dir):
    BASE_NAME_TRANSECT = "POLIGONO_T-"
    BASE_EXTENSION = ".shp"
    is_boudingbox = lambda dirname: dirname.startswith("POLIGONO")

    if os.path.isdir(transect_dir):
        bbfile = BASE_NAME_TRANSECT + number + BASE_EXTENSION
        for pol_dir in os.listdir(transect_dir):
            if is_boudingbox(pol_dir):
                return os.path.join(transect_dir, pol_dir, bbfile)
    else:
        raise RuntimeError("Directory '{}' not found".format(transect_dir))


def srs(number, transect_dir):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    path = boudingbox_path(number, transect_dir)
    if not path:
        raise RuntimeError("Bouding box {} not found in '{}'".format(number, transect_dir))
    ds = driver.Open(path)
    layer = ds.GetLayer()
    ref = layer.GetSpatialRef()
    ds.Destroy()
    return ref


def epsg(zone, geogcs, datum):
    if not (search("(GCS)*(SIRGAS)*(2000)", geogcs) or search("(D)*(SIRGAS)*(2000)", datum)):
        raise RuntimeError("GEOGCS '{}' not found".format(geogcs))

    sirgas = {
        14: "31968",
        15: "31969",
        16: "31970",
        17: "31971",
        18: "31972",
        19: "31973",
        20: "31974",
        21: "31975",
        22: "31976",
        -17: "31977",
        -18: "31978",
        -19: "31979",
        -20: "31980",
        -21: "31981",
        -22: "31982",
        -23: "31983",
        -24: "31984",
        -25: "31985"
    }

    return sirgas[zone]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    transects = r"G:\TRANSECTS"
    projs_json = "transects_epsg.json"

    logging.info("Loading projs...")
    if os.path.isfile(projs_json):
        with open(projs_json, "r") as json_data:
            projs = json.load(json_data)
    else:
        projs = {}
        for number, transect_dir in directories(transects).iteritems():
            if number in projs:
                continue
            sref = srs(number, transect_dir)
            geogcs = sref.GetAttrValue("GEOGCS")
            datum = sref.GetAttrValue("DATUM")
            zone = sref.GetUTMZone()
            projs[number] = epsg(zone, geogcs, datum)
            del sref

        logging.info("Writing projs...")
        with open(projs_json, "w") as f:
            json.dump(projs, f, indent=4, sort_keys=True)

    print(projs)
