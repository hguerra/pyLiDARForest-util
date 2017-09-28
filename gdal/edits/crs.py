import pycrs
from osgeo import ogr

path = r"C:\Users\EBA\Documents\data\TRANSECTS\T-0145\POLIGONO_T-0145_SHP\POLIGONO_T-0145"

# PyCRS
fromcrs = pycrs.loader.from_file(path + ".prj")
print( fromcrs.to_proj4())
print(fromcrs.to_esri_wkt())

# GDAL
driver = ogr.GetDriverByName('ESRI Shapefile')
dataset = driver.Open(path + ".shp")
layer = dataset.GetLayer()
spatialRef = layer.GetSpatialRef()

#spatialRef.MorphToESRI()
#spatialRef.MorphFromESRI()

zone = spatialRef.GetUTMZone()
print("Zone: %d" %zone)

proj4 = spatialRef.ExportToProj4()
print("\nproj4: ")
print(proj4)

pci = spatialRef.ExportToPCI()
print("\npci: ")
print(pci)

usgs = spatialRef.ExportToUSGS()
print("\nusgs: ")
print(usgs)

mi = spatialRef.ExportToMICoordSys()
print("\nmi: ")
print(mi)

wkt = spatialRef.ExportToWkt()
print("\nwkt: ")
print(wkt)

wktPretty = spatialRef.ExportToPrettyWkt()
print("\nwktPretty: ")
print(wktPretty)

xml = spatialRef.ExportToXML()
print("\nxml: ")
print(xml)




