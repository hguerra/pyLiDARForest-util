import argparse
import logging

from osgeo import gdal, ogr, osr
from osgeo.gdalconst import *

# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()


def polygonize(filename, layer, src_band_n=1, maskband=None, dst_field=-1, options=[], prog_func=gdal.TermProgress):
    gdal_ds = gdal.Open(filename, GA_ReadOnly)
    if not gdal_ds:
        raise RuntimeError("Unable to open {}".format(filename))
    srcband = gdal_ds.GetRasterBand(src_band_n)
    return gdal.Polygonize(srcband, maskband, layer, dst_field, options, callback=prog_func)


def pg_layer(table, raster, srs, geom_type=ogr.wkbPolygon, server="localhost", dbname="eba", user="eba",
             password="ebaeba18"):
    conn_str = "PG: host=%s dbname=%s user=%s password=%s" % (server, dbname, user, password)
    conn = ogr.Open(conn_str)
    layer = conn.CreateLayer(table, srs, geom_type, ['OVERWRITE=YES'])

    result = polygonize(raster, layer)
    logging.info("Polygonize with success: {}".format(str(result)))
    del conn


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OGR polygonize")
    parser.add_argument("-s", "--server", type=str, default="localhost")
    parser.add_argument("-d", "--dbname", type=str, default="eba")
    parser.add_argument("-u", "--user", type=str, default="eba")
    parser.add_argument("-p", "--password", type=str, default="ebaeba18")
    parser.add_argument("-e", "--epsg", type=int, default=5880)
    parser.add_argument("-l", "--log", type=str, default=None, help="Logs to a file. Default 'console'.")
    parser.add_argument("-t", "--table", type=str, required=True)
    parser.add_argument("-r", "--rasterpath", type=str, required=True, help="Raster file.")
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(filename=args.log, level=logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler())
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        logging.info("Running 'polygonize' to path '{}'...".format(args.table))
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(args.epsg)

        pg_layer(args.table, args.rasterpath, srs, server=args.server, dbname=args.dbname, user=args.user,
                 password=args.password)
    except Exception as e:
        logging.error("Error to 'polygonize' file: {}".format(str(e)))
