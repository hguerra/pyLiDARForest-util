@echo off
for /f "tokens=1-4 delims=/ " %%i in ("%date%") do (
    set day=%%i
    set month=%%j
    set year=%%k
)
set datestr=%day%_%month%_%year%
echo datestr is %datestr%

set BACKUP_FILE=eba_%datestr%.backup
echo backup file name is %BACKUP_FILE%

SET pg_bin=C:\Program Files\PostgreSQL\9.6\bin\
SET dump=pg_dump.exe
SET PGPASSWORD=ebaeba18
echo on

:: Dump database
"%pg_bin%%dump%" -h localhost -p 5432 -U eba -F c -b -v -f "E:/heitor.guerra/db_backup/db/%BACKUP_FILE%" eba
"%pg_bin%%dump%" -h localhost -p 5432 -U eba -F c -b -v -f "E:/heitor.guerra/db_backup/db/palsar/%BACKUP_FILE%" palsar