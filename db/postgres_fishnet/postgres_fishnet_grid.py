import argparse
import logging
import subprocess
from time import time

from osgeo import gdal
from osgeo.gdalconst import *


class Fishnet(object):
    """
    Make a 2D grid of rectangular polygons, which is sometimes called a fishnet grid.
    https://trac.osgeo.org/postgis/wiki/UsersWikiCreateFishnet
    """

    def __init__(self, raster, table):
        src_ds = gdal.Open(raster, GA_ReadOnly)
        assert src_ds

        self._ds = src_ds
        self._rows = self._ds.RasterYSize
        self._cols = self._ds.RasterXSize
        self._height, self._width, self._xmax, self._xmin, self._ymax, self._ymin = self._extent()
        self._table = table

    def info(self):
        upper_left = (self._xmin, self._ymax)
        lower_left = (self._xmin, self._ymin)
        upper_right = (self._xmax, self._ymax)
        lower_right = (self._xmax, self._ymin)
        center = (self._xmin + ((self._width / 2) * self._cols), self._ymin + ((self._height / 2) * self._rows))

        info = ["(Rows:{} , Cols: {}) = {}".format(self._rows, self._cols, self._rows * self._cols),
                "Extent: {}".format(str([self._xmin, self._xmax, self._ymin, self._ymax])),
                "Width: {}, Height: {}".format(self._width, self._height), "Upper Left {}".format(str(upper_left)),
                "Lower Left {}".format(str(lower_left)), "Upper Right {}".format(str(upper_right)),
                "Lower Right {}".format(str(lower_right)), "Center {}".format(str(center))]

        return "\n".join(info)

    def view(self):
        params = {
            "nrow": self._rows,
            "ncol": self._cols,
            "xsize": self._width,
            "ysize": self._height,
            "x0": self._xmin,
            "y0": self._ymin
        }

        st_create_fishnet = "SELECT ROW_NUMBER() OVER (ORDER BY cells.row) AS id, cells.row, cells.col, " \
                            "st_setsrid(cells.geom, 5880) AS geom FROM ST_CreateFishnet(" \
                            "{nrow}, {ncol}, {xsize}, {ysize}, {x0}, {y0}" \
                            ") AS cells;".format(**params)

        view_fishnet = "DROP VIEW view_ST_CreateFishnet;CREATE VIEW view_ST_CreateFishnet AS {}".format(
            st_create_fishnet)
        return view_fishnet

    def insert(self, mask, mask_fid_col, mask_fid_val, mask_geom_col="geom"):
        params = {
            "table": self._table,
            "nrow": self._rows,
            "ncol": self._cols,
            "xsize": self._width,
            "ysize": self._height,
            "x0": self._xmin,
            "y0": self._ymin,
            "mask": mask,
            "mask_fid_col": mask_fid_col,
            "mask_fid_val": mask_fid_val,
            "mask_geom_col": mask_geom_col
        }

        insert_table = """
BEGIN;
CREATE SEQUENCE public.{table}_seq
INCREMENT 1
MINVALUE 1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER TABLE public.{table}_seq
  OWNER TO postgres;

CREATE TABLE {table} (
  id   INTEGER NOT NULL DEFAULT nextval('{table}_seq' :: REGCLASS),
  {mask}_id INTEGER,
  row  INTEGER,
  col  INTEGER,
  processed BOOLEAN DEFAULT FALSE,
  geom GEOMETRY(Polygon, 5880),
  CONSTRAINT {table}_pkey PRIMARY KEY (id),
  CONSTRAINT {table}_fkey FOREIGN KEY ({mask}_id) REFERENCES {mask}({mask_fid_col})
)
WITH (
OIDS = FALSE
);
ALTER TABLE public.{table}
  OWNER TO eba;

CREATE UNIQUE INDEX {table}_unique_index ON public.{table} (id);
CREATE INDEX {table}_gix ON public.{table} USING GIST (geom);
COMMIT;

BEGIN;
INSERT INTO {table} ({mask}_id, row, col, geom)
  SELECT
    {mask_fid_val},
    cells.row,
    cells.col,
    st_setsrid(cells.geom, 5880) AS geom
  FROM ST_CreateFishnet({nrow}, {ncol}, {xsize}, {ysize}, {x0}, {y0}) AS cells;
COMMIT;

VACUUM ANALYZE {table};
CLUSTER {table} USING {table}_gix;
ANALYZE {table};

BEGIN;
DELETE FROM {table} polys
USING {mask} bb
WHERE bb.{mask_fid_col} = {mask_fid_val} AND NOT ST_Intersects(polys.geom, bb.{mask_geom_col});
COMMIT;""" \
            .format(**params)
        return insert_table

    def _extent(self):
        geotrans = self._ds.GetGeoTransform()
        width = geotrans[1]
        height = geotrans[5]
        xmin = geotrans[0]
        ymax = geotrans[3]
        xmax = xmin + width * self._cols
        ymin = ymax + height * self._rows
        height = -height
        return height, width, xmax, xmin, ymax, ymin

    @staticmethod
    def execute(command, verbose=False):
        logging.info("Running '{}'".format(command))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        if ((out is not None) and ("ERROR" in out)) or ((err is not None) and ("ERROR" in err)):
            logging.error("Error in command: {0} Message: {1}{2}".format(command, out, err))
            raise
        if verbose > 0:
            logging.info(out)

    @staticmethod
    def pgrun(table, sql, dbname="eba", user="eba", password="ebaeba18", psql=r"C:\Program Files\PostgreSQL\9.6\bin\psql.exe"):
        sql_name = table + ".sql"
        sql_temp = open(sql_name, "w")
        sql_temp.write(sql)
        sql_temp.close()

        command = 'SET PGPASSWORD={}\n"{}" -U {} -d {} -f "{}"'.format(password, psql, user, dbname, sql_name)
        bat_name = table + ".bat"
        bat_temp = open(bat_name, "w")
        bat_temp.write(command)
        bat_temp.close()


if __name__ == "__main__":
    gdal.UseExceptions()

    parser = argparse.ArgumentParser(description="FishNetGrid")
    parser.add_argument("-s", "--server", type=str, default="localhost")
    parser.add_argument("-d", "--dbname", type=str, default="eba")
    parser.add_argument("-u", "--user", type=str, default="eba")
    parser.add_argument("-p", "--password", type=str, default="ebaeba18")
    parser.add_argument("-l", "--log", type=str, default=None, help="Logs to a file. Default 'console'.")
    parser.add_argument("-mg", "--maskgeomcol", type=str, default="geom")
    parser.add_argument("-r", "--raster", type=str, required=True, help="Raster file.")
    parser.add_argument("-t", "--table", type=str, required=True)
    parser.add_argument("-m", "--mask", type=str, required=True)
    parser.add_argument("-mc", "--maskfidcol", type=str, required=True)
    parser.add_argument("-mv", "--maskfidval", type=str, required=True)
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(filename=args.log, level=logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler())
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        fs = Fishnet(args.raster, args.table)

        logging.info("Creating SQL...")
        sql = fs.insert(args.mask, args.maskfidcol, args.maskfidval)
        logging.info(sql)

        t0 = time()
        logging.info("Running psql...")
        sql = sql.strip()
        Fishnet.pgrun(args.table, sql, args.dbname, args.user, args.password)

        logging.info("Table created with success in {0:.2f} seconds!".format(time() - t0))
    except Exception as e:
        logging.error("Error to 'FishNetGrid' file: {}".format(str(e)))
