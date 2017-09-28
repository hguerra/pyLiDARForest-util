SET pg_bin=C:\Program Files\PostgreSQL\9.6\bin\
SET exec=psql.exe
SET PGPASSWORD=ebaeba18

::"%pg_bin%%exec%" -U eba -d eba -c "VACUUM ANALYZE public.transects;"
::"%pg_bin%%exec%" -U eba -d eba -c "CLUSTER public.transects USING transects_gix;"
::"%pg_bin%%exec%" -U eba -d eba -c "ANALYZE public.transects;"

::"%pg_bin%%exec%" -U eba -d eba -c "VACUUM ANALYZE public.agb_average;"
::"%pg_bin%%exec%" -U eba -d eba -c "CLUSTER public.agb_average USING agb_average_gix;"
::"%pg_bin%%exec%" -U eba -d eba -c "ANALYZE public.agb_average;"

"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as number from states;" > result.txt
