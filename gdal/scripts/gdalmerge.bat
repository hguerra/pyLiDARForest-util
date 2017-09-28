SET python_exe=C:\Anaconda\envs\geo\python.exe
SET script=E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\gdal\scripts\gdal_merge.py

%python_exe% %script% -of "GTiff" -o "output.tif" "input_1.tif" "input_2.tif"