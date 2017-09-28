# https://pcjericks.github.io/py-gdalogr-cookbook/
import sys

try:
    from osgeo import ogr, osr, gdal

    print("GDAL VERSION: {}".format(gdal.__version__))
    gdal_driver_list = [gdal.GetDriver(i).GetDescription() for i in range(gdal.GetDriverCount())]
    ogr_driver_list = [ogr.GetDriver(i).GetDescription() for i in range(ogr.GetDriverCount())]

    print("\nGDAL DRIVERS:")
    print(gdal_driver_list)

    print("\nOGR DRIVERS:")
    print(ogr_driver_list)
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')
