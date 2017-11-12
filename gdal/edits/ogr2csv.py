import os
import argparse
import logging
import csv
from re import search
from osgeo import ogr
from osgeo.gdalconst import *


def extract_features(vector_path, columns):
    assert vector_path
    assert columns
    assert isinstance(columns, dict)
    logging.info("Extract features of '{}'".format(vector_path))

    vector = ogr.Open(vector_path, GA_ReadOnly)
    layer = vector.GetLayer()
    layer_defn = layer.GetLayerDefn()

    features = {}
    feature = layer.GetNextFeature()
    while feature is not None:
        for i in range(0, layer_defn.GetFieldCount()):
            name_ref = layer_defn.GetFieldDefn(i).GetNameRef()
            if name_ref in columns:
                features[columns[name_ref]] = feature.GetField(i)
        feature = layer.GetNextFeature()
    return features


def files(path, regex="zonal_stats_*(.*).shp"):
    mfiles = []
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path) and search(regex, file_name):
            mfiles.append(file_path)
    return mfiles


def features(path, fields):
    return [extract_features(file_path, fields) for file_path in files(path)]


def write(file_name, field_names, values):
    assert file_name
    assert field_names
    assert values
    assert isinstance(field_names, dict)
    assert isinstance(values, list)

    with open(file_name, "w") as csv_file:
        logging.info("Write csv '{}'".format(file_name))

        writer = csv.DictWriter(csv_file, fieldnames=field_names.values(), lineterminator="\n")
        writer.writeheader()
        for value in values:
            assert isinstance(value, dict)
            writer.writerow(value)


if __name__ == "__main__":
    # C:\Anaconda\envs\geo\python.exe E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\ogr2csv.py -v "G:\CAMPOS_DGPS\PARCELAS_SEPARADAS" -f "zonal_stats.csv" -l "E:\heitor.guerra\ZonalStats\ogr2csv.log"
    parser = argparse.ArgumentParser(description="OGR to CSV")
    parser.add_argument("-v", "--vectorpath", type=str, required=True, help="Directory or Vector file.")
    parser.add_argument("-f", "--file", type=str, required=True, help="Name of the file exported.")
    parser.add_argument("-l", "--log", type=str, help="Logs to a file. Default 'console'.")
    args = parser.parse_args()

    if not os.path.isdir(args.vectorpath):
        raise RuntimeError("Vector path '{}' not found".format(args.vectorpath))

    if args.log:
        logging.basicConfig(filename=args.log, level=logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler())
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("Running 'ogr2csv' to path '{}'...".format(args.vectorpath))

    columns = {
        "zs_file": "file",
        "zs_min": "min",
        "zs_mean": "mean",
        "zs_max": "max",
        "zs_std": "std",
        "zs_sum": "sum",
        "zs_count": "count",
        "zs_area": "area",
        "zs_cv": "cv"
    }

    write(args.file, columns, features(args.vectorpath, columns))
