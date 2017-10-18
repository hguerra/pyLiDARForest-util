SET pg_bin=C:\Program Files\PostgreSQL\9.6\bin\
SET PGPASSWORD=ebaeba18

SET shp2pgsql="%pg_bin%shp2pgsql.exe"
SET psql="%pg_bin%psql.exe"

::%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_1.shp" tile_1 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_2.shp" tile_2 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_3.shp" tile_3 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_4.shp" tile_4 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_5.shp" tile_5 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_6.shp" tile_6 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_7.shp" tile_7 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_8.shp" tile_8 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_9.shp" tile_9 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_10.shp" tile_10 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_11.shp" tile_11 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_12.shp" tile_12 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_13.shp" tile_13 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_14.shp" tile_14 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_15.shp" tile_15 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_16.shp" tile_16 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_17.shp" tile_17 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_18.shp" tile_18 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_19.shp" tile_19 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_20.shp" tile_20 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_21.shp" tile_21 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_22.shp" tile_22 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_23.shp" tile_23 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_24.shp" tile_24 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_25.shp" tile_25 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_26.shp" tile_26 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_27.shp" tile_27 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_28.shp" tile_28 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_29.shp" tile_29 | %psql% -U postgres -d palsar
%shp2pgsql% -I -s 5880 "E:\heitor.guerra\db_select\grid\grid_30.shp" tile_30 | %psql% -U postgres -d palsar
