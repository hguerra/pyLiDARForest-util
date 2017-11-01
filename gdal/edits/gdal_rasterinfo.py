import numpy as np

from osgeo import gdal
from osgeo.gdalconst import *

# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()

if __name__ == "__main__":
    # filename = r"E:\heitor.guerra\tests\extrapolar\EVI_max.tif"
    # filename = r"E:\heitor.guerra\tests\jorge\pft50y_area.nc"
    filename = r"E:\heitor.guerra\db_insert\zonal_stats\rasters\part_5\palsar_hh_17.tif"
    src_ds = gdal.Open(filename, GA_ReadOnly)

    metadata = src_ds.GetMetadata()
    print("[ METADATA ]: {}".format(metadata))

    nrows = src_ds.RasterYSize
    cols = src_ds.RasterXSize
    print ("[ Rows, Cols ]: {}, {} = {}".format(nrows, cols, nrows * cols))

    geoTransform = src_ds.GetGeoTransform()
    width = geoTransform[1]
    height = geoTransform[5]

    xmin = geoTransform[0]
    ymax = geoTransform[3]
    xmax = xmin + width * cols
    ymin = ymax + height * nrows

    print("Extent: {}".format(str([xmin, xmax, ymin, ymax])))
    print("width: {}, height: {}".format(width, -height))

    raster_count = src_ds.RasterCount
    print ("[ RASTER BAND COUNT ]: {}".format(raster_count))
    for band in range(1, raster_count + 1):
        print ("[ GETTING BAND ]: {}".format(band))

        srcband = src_ds.GetRasterBand(band)
        stats = srcband.GetStatistics(True, True)
        nodata = srcband.GetNoDataValue()

        print("[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % (stats[0], stats[1], stats[2], stats[3]))
        print("[ NODATA ] = %f" % nodata)

        # rast_array = np.array(srcband.ReadAsArray())
        # count = 0
        # for row in rast_array:
        #     for val in row:
        #         count += 1
        # print(count)
        # del rast_array
