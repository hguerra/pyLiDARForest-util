# -*- coding: utf-8 -*-

import logging
import os
import pprint
import re
import unidecode
import pandas as pd
import pandas.io.sql as psql
import psycopg2 as pg

from time import time
from osgeo import ogr


def files(filepath, ext):
    has_extension = lambda filename: os.path.splitext(filename)[1].lower() == ext
    is_file = lambda filename: os.path.isfile(os.path.join(filepath, filename)) and has_extension(filename)
    return [os.path.join(filepath, filename) for filename in os.listdir(filepath) if is_file(filename)]


def normalize(s, encoding="latin-1", replace_hyphen=False, replace_multiple_space=False, remove_prepositions=False,
              join=False):
    str_empty = ""
    str_space = " "
    single_quotation_marks = "'"
    if isinstance(s, str):
        s = unicode(s, encoding)
    s = unidecode.unidecode(s)
    s = s.strip().lower()

    s = s.replace(single_quotation_marks, str_empty)
    double_quotation_marks = '"'
    s = s.replace(double_quotation_marks, str_empty)
    prepositions_pt = ("da", "das", "de", "do", "dos")

    if replace_hyphen:
        str_hyphen = "-"
        s = s.replace(str_hyphen, str_space)

    if replace_multiple_space:
        pattern_multiples_space = "\s\s+"
        s = re.sub(pattern_multiples_space, str_space, s)

    if join:
        s = s.replace(str_space, str_empty)

    if remove_prepositions:
        compound_name = s.split()
        if len(compound_name) > 2:
            for i, name in enumerate(compound_name):
                if name in prepositions_pt:
                    del compound_name[i]
            s = str_space.join(compound_name)
    return s


def geom_from_wkt(geom, epsg):
    return "ST_GeomFromText('{}', {})".format(geom, epsg)


def extract_geom(shapefile):
    ds = ogr.Open(shapefile)
    bb = ds.GetLayer()
    assert bb

    basename = os.path.splitext(os.path.basename(shapefile))[0]
    basename = normalize(basename, replace_hyphen=True, replace_multiple_space=True, remove_prepositions=True)

    wkt = None
    authority_code = 5880
    feat = bb.GetNextFeature()
    while feat:
        geom = feat.geometry()
        if geom:
            logging.info("Geometry found in shapefile '{}'.".format(basename))
            wkt = geom_from_wkt(geom.ExportToWkt(), authority_code)
            break
        feat = bb.GetNextFeature()
    del ds

    if not wkt:
        logging.error("Error to find geometry in shapefile '{}'.".format(basename))
    return basename, wkt


def as_data_frame(sql, pickle="df.pickle", host="localhost", user="eba", password="ebaeba18", database="eba"):
    log_msg = "Loading data frame from '{}'..."

    t0_load = time()
    if os.path.isfile(pickle):
        logging.info(log_msg.format("pickle"))
        df = pd.read_pickle(pickle)
    else:
        connection = pg.connect(host=host, user=user, password=password, database=database)

        logging.info(log_msg.format("PostgreSQL"))
        df = psql.read_sql(sql, connection)
        df.to_pickle(pickle)
    logging.info("Time elapsed to load data: %.2fs" % (time() - t0_load))
    return df


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    my_print = pprint.PrettyPrinter(indent=4).pprint

    # simple example
    # boudingbox = r"E:\heitor.guerra\db_insert\simple_plotdata\ALFLOR_PC.shp"
    # print(extract_geom(boudingbox))

    # multiples shapefiles
    shapefiles_path = r"E:\heitor.guerra\db_insert\simple_plotdata"

    geoms = {}
    for boundingbox in files(shapefiles_path, ".shp"):
        plot, geom = extract_geom(boundingbox)
        geoms[plot] = geom

    # my_print(geoms)

    # creating sql file to update database
    sql_distict_plots = "select pl.name, pl.id from plot pl where pl.geom is null order by pl.id;"
    sql_update_plot = "update plot set geom = {} where id = {};"
    sql_run_function_to_update_agb = "SELECT fheight_agb_living_trees();"

    sqls = []
    distict_plots = as_data_frame(sql_distict_plots, pickle="distict_plots.pickle", database="simple_plotdata")
    for idx, row in distict_plots.iterrows():
        plot_name = row["name"]
        plot_id = row["id"]

        if plot_name not in geoms:
            logging.error("Plot '{}' does not have a shapefile in directory '{}'.".format(plot_name, shapefiles_path))
        else:
            geom = geoms[plot_name]
            sqls.append(sql_update_plot.format(geom, plot_id))
    sqls.append(sql_run_function_to_update_agb)

    if len(sqls) == 1:
        logging.error("No new geometries found in the directory '{}'. Please update your directory.".format(shapefiles_path))
    else:
        sql_file = r"update_agb.sql"
        with open(sql_file, mode="w") as f:
            for line in sqls:
                f.write(line + "\n")

        logging.info("done.")