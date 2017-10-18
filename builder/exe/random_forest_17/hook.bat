SET pg_bin=C:\Program Files\PostgreSQL\9.6\bin\
SET exec=psql.exe
SET PGPASSWORD=ebaeba18

echo %time%

"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_soil from amazon_soil_17 where f_soil_qr is not null;" >> result.txt
::"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_max from amazon_trmm_bilinear_17 where trmm_max is not null;" >> result.txt
::"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_median from amazon_trmm_bilinear_17 where trmm_median is not null;" >> result.txt
::"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_min from amazon_trmm_bilinear_17 where trmm_min is not null;" >> result.txt
::"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_q1 from amazon_trmm_bilinear_17 where trmm_q1 is not null;" >> result.txt
::"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_q3 from amazon_trmm_bilinear_17 where trmm_q3 is not null;" >> result.txt
::"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_sd from amazon_trmm_bilinear_17 where trmm_sd is not null;" >> result.txt
::"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_soil from amazon_trmm_bilinear_17 where f_soil_qr is not null;" >> result.txt

::"%pg_bin%%exec%" -U eba -d eba -c "VACUUM ANALYZE public.vegetation_ibge;"
::"%pg_bin%%exec%" -U eba -d eba -c "CLUSTER public.vegetation_ibge USING vegetation_ibge_geom_idx;"
::"%pg_bin%%exec%" -U eba -d eba -c "ANALYZE public.vegetation_ibge;"

::"%pg_bin%%exec%" -U eba -d eba -c "VACUUM ANALYZE public.amazon_trmm_17;"
::"%pg_bin%%exec%" -U eba -d eba -c "CLUSTER public.amazon_trmm_17 USING amazon_trmm_17_gix;"
::"%pg_bin%%exec%" -U eba -d eba -c "ANALYZE public.amazon_trmm_17;"

::C:\Anaconda\envs\geo\python.exe "E:\heitor.guerra\PycharmProjects\pyLiDARForest\stuff\extract_raster.py" -s "select trmm_max,trmm_mean,trmm_median,trmm_min,trmm_q1,trmm_q3,trmm_sd,f_soil_qr,geom from amazon_trmm_bilinear_17" -r "E:\heitor.guerra\tests\extrapolar\EVI_max.tif" -o "E:\heitor.guerra\db_backup\rasters\test\trmm\bilinear\zs" -b "1" -a "trmm_max" "trmm_mean" "trmm_median" "trmm_min" "trmm_q1" "trmm_q3" "trmm_sd" "f_soil_qr" -l "E:\heitor.guerra\db_backup\rasters\test\trmm\bilinear\zs\extract_amazon_trmm_bilinear_17.log"
C:\Anaconda\envs\geo\python.exe "E:\heitor.guerra\PycharmProjects\pyLiDARForest\stuff\extract_raster.py" -s "select f_soil_qr,geom from amazon_soil_17" -r "E:\heitor.guerra\tests\extrapolar\EVI_max.tif" -o "E:\heitor.guerra\db_backup\rasters\test\vegetation\zs" -b "17" -a "f_soil_qr" -l "E:\heitor.guerra\db_backup\rasters\test\vegetation\zs\extract_veg_17.log"
