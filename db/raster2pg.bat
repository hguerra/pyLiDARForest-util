SET pg_bin=C:\Program Files\PostgreSQL\9.6\bin\
SET exec=raster2pgsql.exe
SET files_path=E:\heitor.guerra\DADOS_PARA_EXTRAPOLAR\EVI_NDVI_reprojected\DB\

"%pg_bin%%exec%" -I -C -s 5880 -M "%files_path%*.tif" -F -t 250x250 > "evi_ndvi.sql"
"%pg_bin%psql.exe" -U eba -d eba -f "evi_ndvi.sql"