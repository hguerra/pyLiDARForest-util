SET python_exe=C:\Anaconda\envs\geo\python.exe
SET script="E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\postgres_fishnet\postgres_fishnet_grid.py"

%python_exe% %script% -r "E:\heitor.guerra\tests\extrapolar\EVI_max.tif" -t "mosaic" -m "states" -mc "gid" -mv 2 -l "E:\heitor.guerra\amazon.log"
