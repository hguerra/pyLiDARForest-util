from osgeo import gdal
from osgeo.gdalconst import *

# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()

if __name__ == "__main__":
    filename = r"E:\heitor.guerra\db_insert\zonal_stats\rasters\part_0\EVI_max.tif"
    src_ds = gdal.Open(filename, GA_ReadOnly)

    rows = src_ds.RasterYSize
    cols = src_ds.RasterXSize
    print ("[ Rows, Cols ]: {}, {} = {}".format(rows, cols, rows * cols))

    geoTransform = src_ds.GetGeoTransform()
    width = geoTransform[1]
    height = geoTransform[5]

    xmin = geoTransform[0]
    ymax = geoTransform[3]
    xmax = xmin + width * cols
    ymin = ymax + height * rows
    height = -height

    print("Extent: {}".format(str([xmin, xmax, ymin, ymax])))
    print("width: {}, height: {}\n".format(width, height))

    upper_left = (xmin, ymax)
    lower_left = (xmin, ymin)
    upper_right = (xmax, ymax)
    lower_right = (xmax, ymin)
    center = (xmin + ((width / 2) * cols), ymin + ((height / 2) * rows))

    print("Upper Left {}".format(str(upper_left)))
    print("Lower Left {}".format(str(lower_left)))
    print("Upper Right {}".format(str(upper_right)))
    print("Lower Right {}".format(str(lower_right)))
    print("Center {}".format(str(center)))

    print("\nTesting create grid parallel...\n")
    i = 1
    n = 4
    ydim = height / n
    xdim = width / n

    u_left = upper_left
    while i <= n:
        l_left = (u_left[0], u_left[1] + ydim)
        u_right = (u_left[0] + xdim, u_left[1])
        l_right = (u_left[0] + xdim, u_left[1] + ydim)

        print("Upper Left {}".format(str(u_left)))
        print("Lower Left {}".format(str(l_left)))
        print("Upper Right {}".format(str(u_right)))
        print("Lower Right {}\n".format(str(l_right)))

        i += 1
        if i < (n / 2):
            u_left = u_right
        else:
            u_left = l_left
