SET pgsql2shp="C:\Program Files\PostgreSQL\9.6\bin\pgsql2shp.exe"
SET output="E:\heitor.guerra\grid_metrics"

::%pgsql2shp% -f %output% -h localhost -u postgres -P postgres eba "SELECT filename, chm, x, y, ST_MakePolygon(ST_MakeLine(ARRAY[ST_MakePoint(x - 25, y - 25), ST_MakePoint(x + 25, y - 25), ST_MakePoint(x + 25, y + 25), ST_MakePoint(x - 25, y + 25), ST_MakePoint(x - 25, y - 25)])) as geom FROM metrics WHERE filename = 'NP_T-0002.CSV';"
::%pgsql2shp% -f %output% -h localhost -u eba -P ebaeba18 eba "SELECT filename, index_, x, y, chm, agblongo_als_total, agblongo_tch_total, agblongo_tch_alive, geom FROM metrics;"

::%pgsql2shp% -f "E:\heitor.guerra\db_select\NP_T-xxxx_amazon_palsar_hv_notnull" -h localhost -u eba -P ebaeba18 eba "SELECT * FROM amazon_palsar_hv WHERE agblongo_als_alive IS NOT NULL OR agblongo_als_total IS NOT NULL OR agblongo_tch_alive IS NOT NULL OR agblongo_tch_total IS NOT NULL;"
::%pgsql2shp% -f "E:\heitor.guerra\db_select\NP_T-xxxx_amazon_trmm" -h localhost -u eba -P ebaeba18 eba "SELECT polys.* FROM amazon_trmm polys INNER JOIN transects bb ON ST_Intersects(bb.polyflown, polys.geom);"

%pgsql2shp% -f "E:\heitor.guerra\db_select\CHM_NP_T-xxxx_amazon_trmm" -h localhost -u eba -P ebaeba18 eba "SELECT polys.* FROM amazon_trmm polys INNER JOIN transects bb ON ST_Intersects(bb.polyflown, polys.geom) WHERE chm IS NOT NULL;"
