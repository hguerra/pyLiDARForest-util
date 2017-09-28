import gdal
import ogr


def new_raster_from_base(base, outputURI, format, nodata=None, datatype=gdal.GDT_Byte):
    cols = base.RasterXSize
    rows = base.RasterYSize
    projection = base.GetProjection()
    geotransform = base.GetGeoTransform()
    bands = base.RasterCount

    driver = gdal.GetDriverByName(format)

    new_raster = driver.Create(str(outputURI), cols, rows, bands, datatype)
    new_raster.SetProjection(projection)
    new_raster.SetGeoTransform(geotransform)

    for i in range(bands):
        n = i + 1
        band = new_raster.GetRasterBand(n)
        nodata_value = nodata or base.GetRasterBand(n).GetNoDataValue()
        band.SetNoDataValue(nodata_value)
        band.Fill(nodata_value)
        band.FlushCache()
    return new_raster


if __name__ == '__main__':
    server = "localhost"
    dbname = "eba"
    user = "eba"
    password = "ebaeba18"

    vector_fn = "evi_max"
    raster_fn = r"E:\heitor.guerra\{}.tif".format(vector_fn)
    base_raster = r"E:\heitor.guerra\tests\extrapolar\EVI_max.tif"

    statement = "SELECT {}, geom FROM amazon_test".format(vector_fn)

    conn_str = "PG: host=%s dbname=%s user=%s password=%s" % (server, dbname, user, password)
    print("Trying to connect PostgresSQL database: {}".format(conn_str))
    conn = ogr.Open(conn_str)
    assert conn

    print("Querying data source and read in the extent ({})".format(statement))
    layer = conn.ExecuteSQL(statement)
    assert layer

    data = gdal.Open(base_raster, gdal.gdalconst.GA_ReadOnly)
    assert data

    print("Rasterizing...")
    raster_dataset = new_raster_from_base(data, raster_fn, 'GTiff', datatype=gdal.GDT_Float32)
    gdal.RasterizeLayer(raster_dataset, [1], layer, options=["ATTRIBUTE={}".format(vector_fn)])

    del raster_dataset
    del conn
    print("Done!")
