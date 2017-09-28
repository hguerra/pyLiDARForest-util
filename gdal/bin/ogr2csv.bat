SET python_exe=C:\Anaconda\envs\geo\python.exe
SET script=E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\gdal\edits\ogr2csv.py

::%python_exe% %script% -v "G:\CAMPOS_DGPS\PARCELAS_SEPARADAS" -f "zonal_stats.csv" -l "E:\heitor.guerra\ZonalStats\ogr2csv.log"
::%python_exe% %script% -v "E:\heitor.guerra\ZonalStats\SHP" -f "E:\heitor.guerra\ZonalStats\zonal_stats_missing.csv" -l "E:\heitor.guerra\ZonalStats\ogr2csv_missing.log"
%python_exe% %script% -v "E:\heitor.guerra\CURSO_AMAPA\zonal_stats" -f "E:\heitor.guerra\CURSO_AMAPA\zonal_stats.csv" -l "E:\heitor.guerra\CURSO_AMAPA\log\ogr2csv.log"