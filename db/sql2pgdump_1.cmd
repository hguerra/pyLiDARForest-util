SET pg_bin=C:\Program Files\PostgreSQL\9.6\bin\
SET exec=psql.exe
SET PGPASSWORD=ebaeba18

echo %time%
"%pg_bin%%exec%" -U eba -d eba -f "E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\sql2pgdump_1_handle.sql"
::"%pg_bin%%exec%" -U eba -d amazon -f "E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\sql2pgdump_1_handle.sql"
echo %time%