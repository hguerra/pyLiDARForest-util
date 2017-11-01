import logging
import os.path as ospath
from os import listdir, mkdir

from osgeo import ogr


def new_filename(filename, prefix="", sulfix="", extension=None):
    path = ospath.dirname(filename)
    filename = ospath.basename(filename)
    filename, ext = ospath.splitext(filename)
    ext = extension or ext
    multi_bat = "{}{}{}{}".format(prefix, filename, sulfix, ext)
    return ospath.join(path, multi_bat)


def multi_thread_header():
    return '''SET python_exe=C:\Anaconda\envs\geo\python.exe
SET script="E:\heitor.guerra\PycharmProjects\pyLiDARForest\stuff\procScriptMultithread.py"'''


def multi_thread_line(processorcores, verbose, inputfname):
    return '%python_exe% %script% -c "{}" -v "{}" "{}"'.format(processorcores, verbose, inputfname)


def write_multi_thread(bat, mode="w", cores=8, verbose=1):
    multi_bat = new_filename(bat, prefix="multi_thread_")

    with open(multi_bat, mode) as f:
        f.write(multi_thread_header() + "\n")
        try:
            f.write(multi_thread_line(cores, verbose, bat) + "\n")
            logging.info("Command appended with success")
        except Exception as writeErr:
            logging.error("Error to append : {}".format(str(writeErr)))


def write(bat, lines, mode="w"):
    with open(bat, mode) as f:
        for line in lines:
            try:
                f.write(line + "\n")
                logging.info("Command appended with success")
            except Exception as writeErr:
                logging.error("Error to append '{}': {}".format(line, str(writeErr)))


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


class EPSG(object):
    SIRGAS = 1
    WGS = 2


class Reproject(object):
    def __init__(self, filepath, fromEPSG, extension=".shp"):
        self._files = self.files(filepath, ext=extension)
        self._from = fromEPSG
        self._driver = ogr.GetDriverByName("ESRI Shapefile")
        self._lines = []
        self._input = filepath
        self._output = ospath.join(filepath, "reproject")

        if not ospath.isdir(self._output):
            mkdir(self._output)

    def commands(self):
        for f in self._files:
            inputdir = ospath.join(self._input, f)
            outputdir = ospath.join(self._output, f)

            srs = self.__getSpatialRef(inputdir)
            zone = srs.GetUTMZone()
            if EPSG.SIRGAS == self._from:
                epsg = self.sirgasEPSG(zone)
                origin = self.WGSEPSG(zone)
            else:
                epsg = self.WGSEPSG(zone)
                origin = self.sirgasEPSG(zone)

            logging.info("Reprojecting {} to {}".format(origin, epsg))
            cmd = '"C:\\Anaconda\\envs\geo\\Library\\bin\\'
            cmd = cmd + 'ogr2ogr.exe" "{output}" -t_srs "EPSG:{epsg}" "{input}"'
            self._lines.append(cmd.format(epsg=epsg, input=inputdir, output=outputdir))

        return self._lines

    def __getSpatialRef(self, file):
        dataset = self._driver.Open(file)
        layer = dataset.GetLayer()
        srs = layer.GetSpatialRef()
        dataset.Destroy()
        return srs

    @staticmethod
    def files(filepath, ext):
        hasExtension = lambda filename: ospath.splitext(filename)[1].lower() == ext
        isFile = lambda filename: ospath.isfile(ospath.join(filepath, filename)) and hasExtension(filename)
        return [filename for filename in listdir(filepath) if isFile(filename)]

    @staticmethod
    def sirgasEPSG(zone):
        sirgas = {
            14: "31968",
            15: "31969",
            16: "31970",
            17: "31971",
            18: "31972",
            19: "31973",
            20: "31974",
            21: "31975",
            22: "31976",
            -17: "31977",
            -18: "31978",
            -19: "31979",
            -20: "31980",
            -21: "31981",
            -22: "31982",
            -23: "31983",
            -24: "31984",
            -25: "31985"
        }

        return sirgas[zone]

    @staticmethod
    def WGSEPSG(zone):
        wgs = {
            14: "32614",
            15: "32615",
            16: "32616",
            17: "32617",
            18: "32618",
            19: "32619",
            20: "32620",
            21: "32621",
            22: "32622",
            -17: "32717",
            -18: "32718",
            -19: "32719",
            -20: "32720",
            -21: "32721",
            -22: "32722",
            -23: "32723",
            -24: "32724",
            -25: "32725"
        }

        return wgs[zone]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    reproject = Reproject(r"G:\Analise_HIPERESPECTRAL\Dados\parcelas_campo", EPSG.WGS)

    bat_base = "E:\\heitor.guerra\\PycharmProjects\\pyLiDARForest\\app\\builder\exe\\"
    bat = bat_base + "app_reproject.bat"

    write(bat, reproject.commands())
    write_multi_thread(bat)

