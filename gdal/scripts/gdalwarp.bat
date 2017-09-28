SET gdal_path=C:\Anaconda\envs\geo\Library\bin\
SET warp=gdalwarp.exe

::"%gdal_path%%warp%" -q -cutline E:/heitor.guerra/AMZ_BIOMA/bioma_Amazonia_WGS84.shp -crop_to_cutline -of GTiff G:/SUB07_DADOS_BASE/DADOS_PARA_EXTRAPOLAR/DADOS_all/EVI_max.tif E:/heitor.guerra/TESTES/output.tif
"%gdal_path%%warp%" -q -cutline E:/heitor.guerra/AMZ_BIOMA/bioma_ERASE_prodes_classe_4.shp -crop_to_cutline -of GTiff E:/heitor.guerra/TESTES/output.tif E:/heitor.guerra/TESTES/output2.tif