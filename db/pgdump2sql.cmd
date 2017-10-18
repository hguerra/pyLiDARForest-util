SET pg_bin=C:\Program Files\PostgreSQL\9.6\bin\
SET dump=pg_dump.exe
SET psql=psql.exe
SET PGPASSWORD=ebaeba18

:: Dump database
::"%pg_bin%%dump%" -U eba -F t eba > "E:\heitor.guerra\db_backup\db\eba-14-08-17.sql"

:: Dump table
::"%pg_bin%%dump%" -U eba -d eba -t "transects" > "E:\heitor.guerra\db_backup\transects.sql"
::"%pg_bin%%dump%" -U eba -d eba -t "metrics" > "E:\heitor.guerra\db_backup\metrics.sql"
::"%pg_bin%%dump%" -U eba -d eba -t "amazon" > "E:\heitor.guerra\db_backup\amazon_nofill.sql"
::"%pg_bin%%dump%" -U eba -d eba -t "amazon_evi_max_2" > "E:\heitor.guerra\db_backup\amazon_evi_max_2.sql"
::"%pg_bin%%dump%" -U eba -d eba -t "amazon_evi" > "E:\heitor.guerra\db_backup\amazon_evi.sql"
::"%pg_bin%%dump%" -U eba -d eba -t "amazon_ndvi" > "E:\heitor.guerra\db_backup\amazon_ndvi.sql"
::"%pg_bin%%dump%" -U eba -d eba -t "amazon_srtm" > "E:\heitor.guerra\db_backup\table\amazon_srtm.sql"

:: Dump table to another database
::"%pg_bin%%dump%" -U eba -d eba -t "amazon_trmm" | "%pg_bin%%psql%" -U eba -d eba_amazon_test