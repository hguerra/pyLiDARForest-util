SET pg_bin=C:\Program Files\PostgreSQL\9.6\bin\
SET restore=pg_restore.exe
SET PGPASSWORD=ebaeba18

:: Restore database
"%pg_bin%%restore%" -h localhost -p 5432 -U eba -d eba -v "E:/heitor.guerra/db_backup/db/eba_23_08_2017_.backup"
