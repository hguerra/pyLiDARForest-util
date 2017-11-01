SET pgsql2shp="C:\Program Files\PostgreSQL\9.6\bin\pgsql2shp.exe"
SET output="E:\heitor.guerra\mosaic_metrics"

::%pgsql2shp% -f %output% -h localhost -u postgres -P postgres eba "SELECT filename, chm, x, y, ST_MakePolygon(ST_MakeLine(ARRAY[ST_MakePoint(x - 25, y - 25), ST_MakePoint(x + 25, y - 25), ST_MakePoint(x + 25, y + 25), ST_MakePoint(x - 25, y + 25), ST_MakePoint(x - 25, y - 25)])) as geom FROM metrics WHERE filename = 'NP_T-0002.CSV';"
::%pgsql2shp% -f %output% -h localhost -u eba -P ebaeba18 eba "SELECT filename, index_, x, y, chm, agblongo_als_total, agblongo_tch_total, agblongo_tch_alive, geom FROM metrics;"

::%pgsql2shp% -f "E:\heitor.guerra\db_select\NP_T-xxxx_amazon_palsar_hv_notnull" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM amazon_palsar_hv WHERE agblongo_als_alive IS NOT NULL OR agblongo_als_total IS NOT NULL OR agblongo_tch_alive IS NOT NULL OR agblongo_tch_total IS NOT NULL;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\NP_T-xxxx_amazon_trmm" -h localhost -u eba -P ebaeba18 eba "SELECT polys.* FROM amazon_trmm polys INNER JOIN transects bb ON ST_Intersects(bb.polyflown, polys.geom);"

::%pgsql2shp% -f "E:\heitor.guerra\db_select\CHM_NP_T-xxxx_amazon_trmm" -h localhost -u eba -P ebaeba18 eba "SELECT polys.* FROM amazon_trmm polys INNER JOIN transects bb ON ST_Intersects(bb.polyflown, polys.geom) WHERE chm IS NOT NULL;"

%pgsql2shp% -f "E:\heitor.guerra\db_backup\rasters\ipcc\chm_rf_train_below_60" -h localhost -u eba -P ebaeba18 eba "select amz.chm, amz.agblongo_tch_alive as train_a, amz.agblongo_tch_total as train_t, st_centroid(amz.geom) as geom from amazon_palsar as amz WHERE amz.agblongo_tch_alive is not null;"

::%pgsql2shp% -f "E:\heitor.guerra\db_select\uncertainty" -h localhost -u eba -P ebaeba18 eba "SELECT agblongo_als_total as agb_als_t, agblongo_als_alive as agb_als_a, agblongo_tch_total as agb_tch_t, agblongo_tch_alive as agb_tch_a, elev_max, agb, se_repr, se_pred, se_cal, se_total, eps, geom FROM amazon_palsar_17;"

::%pgsql2shp% -f "E:\heitor.guerra\db_select\chmEntre50e60" -h localhost -u eba -P ebaeba18 eba "SELECT * from chm where chm > 50 and chm < 60;"


::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_1" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 1;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_2" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 2;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_3" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 3;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_4" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 4;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_5" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 5;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_6" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 6;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_7" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 7;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_8" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 8;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_9" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 9;"

::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_10" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 10;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_11" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 11;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_12" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 12;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_13" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 13;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_14" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 14;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_15" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 15;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_16" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 16;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_17" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 17;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_18" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 18;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_19" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 19;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_20" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 20;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_21" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 21;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_22" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 22;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_23" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 23;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_24" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 24;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_25" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 25;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_26" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 26;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_27" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 27;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_28" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 28;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_29" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 29;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\mosaic_30" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM mosaic WHERE gid = 30;"
