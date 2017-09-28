import json
import os.path as ospath
from os import listdir
from re import search
from stuff.dbutils import dbutils


def extract_number(transect):
    matcher = search("T*([0-9]+)", transect)
    if matcher:
        return matcher.group(1).rjust(4, "0")
    return transect


def files(csv_path):
    csv_extension = ".csv"
    return {
        extract_number(filename): filename
        for filename in listdir(csv_path)
        if ospath.isfile(ospath.join(csv_path, filename)) and ospath.splitext(filename)[1] == csv_extension
    }


if __name__ == "__main__":
    metric_path = r"E:\heitor.guerra\db_insert\metrics"
    metric_files = files(metric_path)

    distinct = "SELECT DISTINCT(filename) FROM metrics;"
    db = dbutils("localhost", "eba", "ebaeba18", "eba", "pg_default")

    transects = {}
    distinct = db.getdata(distinct)
    for row in distinct:
        filename = row[0]
        transects[extract_number(filename)] = filename

    # print("### Metrics in CSV ###")
    # metrics = sorted(metric_files.keys())
    # for metric in metrics:
    #     if metric not in transects:
    #         print("Transect '{}' not found".format(metric))

    print("\n### Bouding box ###")
    geoms_json = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\geom\geoms.json"
    with open(geoms_json, "r") as json_data:
        geoms = json.load(json_data)

        print("Metrics that are not in DB:\n")
        for number in sorted(geoms.keys()):
            if number not in transects:
                print("Transect '{}' not found in DB".format(number))

        print("\nTransects that do not have a shapefile:\n")
        for number in sorted(transects.keys()):
            if number not in geoms:
                print("Transect '{}' does not have a shapefile".format(number))