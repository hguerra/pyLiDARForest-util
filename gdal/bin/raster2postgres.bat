SET python_exe=C:\Anaconda\envs\geo\python.exe
SET script=E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\gdal\gdal_polygonize.py

::gdal_polygonize.py myraster.tif -f "ESRI Shapefile" mylayer.shp
::gdal_polygonize.py myraster.tif -f PostgreSQL PG:"dbname='eba' user='eba' password='ebaeba18'" mylayer
::gdal_polygonize.py "E:\heitor.guerra\DADOS_PARA_EXTRAPOLAR\EVI_NDVI_reprojected\DB\EVI_QUANTILE_AMZ_Legal_sh4.tif" -f PostgreSQL PG:"dbname='eba' user='eba' password='ebaeba18'" evi
%python_exe% %script% "E:\heitor.guerra\EVI\output-b1.tif" -f "ESRI Shapefile" E:\heitor.guerra\EVI\data.shp