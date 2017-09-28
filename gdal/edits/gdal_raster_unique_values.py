import numpy as np

from osgeo import gdal, ogr, os, osr
from osgeo.gdalconst import *

# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()


def array2raster(newRasterfn, rasterOrigin, pixelWidth, pixelHeight, array, driver_name="GTiff", epsg=5880):
    cols = array.shape[1]
    rows = array.shape[0]
    originX = rasterOrigin[0]
    originY = rasterOrigin[1]

    driver = gdal.GetDriverByName(driver_name)
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Byte)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(epsg)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


def save(newRasterfn, rasterOrigin, pixelWidth, pixelHeight, array):
    reversed_arr = array[::-1]  # reverse array so the tif looks like the array
    array2raster(newRasterfn, rasterOrigin, pixelWidth, pixelHeight, reversed_arr)  # convert array to raster


if __name__ == "__main__":
    infname = r"E:\heitor.guerra\EVI\vegtype_2000_5880.tif"
    outfname = r"E:\heitor.guerra\EVI\output-b{}.tif"

    src_ds = gdal.Open(infname, GA_ReadOnly)

    rows = src_ds.RasterYSize
    cols = src_ds.RasterXSize
    geoTransform = src_ds.GetGeoTransform()
    pixelWidth = geoTransform[1]
    pixelHeight = -geoTransform[5]
    rasterOrigin = (geoTransform[0], geoTransform[3])

    rast_min = 0
    rast_max = 255
    step = (rast_max - rast_min) / (float(rows * cols) - 1)

    for band in range(1, src_ds.RasterCount + 1):
        # random_array = np.linspace(0, 255, num=rows * cols)
        # random_array = random_array.reshape(rows, cols)
        # save(outfname.format(band), rasterOrigin, pixelWidth, pixelHeight, random_array)

        srcband = src_ds.GetRasterBand(band)
        nodata = srcband.GetNoDataValue()
        rast_array = np.array(srcband.ReadAsArray())

        idx_col = 0
        result = []
        for row in rast_array:
            col = []
            for val in row:
                if val == nodata:
                    col.append(nodata)
                else:
                    col.append(idx_col)
                    idx_col += step
            result.append(col)
        del rast_array
        result = np.array(result)

        save(outfname.format(band), rasterOrigin, pixelWidth, pixelHeight, result)
