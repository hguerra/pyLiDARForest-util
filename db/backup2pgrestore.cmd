SET pg_bin=C:\Program Files\PostgreSQL\9.6\bin\
SET restore=pg_restore.exe
SET PGPASSWORD=ebaeba18

:: Restore database
::"%pg_bin%%restore%" -h localhost -p 5432 -U eba -d eba -v "eba_23_08_2017_.backup"
"%pg_bin%%restore%" -h localhost -p 5432 -U eba -d simple_plotdata -v "E:\heitor.guerra\db_backup\db\simple_plotdata_12_11_2017.backup"

:: Restore table
::"%pg_bin%%restore%" -t amazon_trmm_new -h localhost -p 5432 -U eba -d eba -v "E:\heitor.guerra\db_backup\db\eba_05_10_2017.backup"
