import csv
import logging
import os.path as ospath
from os import listdir
from re import search


def multi_thread_header():
    return '''SET python_exe=C:\Anaconda\envs\geo\python.exe
SET script="E:\heitor.guerra\PycharmProjects\pyLiDARForest\stuff\procScriptMultithread.py"'''


def multi_thread_line(processorcores, verbose, inputfname):
    return '%python_exe% %script% -c "{}" -v "{}" "{}"'.format(processorcores, verbose, inputfname)


def new_filename(filename, prefix="", sulfix="", extension=None):
    path = ospath.dirname(filename)
    filename = ospath.basename(filename)
    filename, ext = ospath.splitext(filename)
    ext = extension or ext
    multi_bat = "{}{}{}{}".format(prefix, filename, sulfix, ext)
    return ospath.join(path, multi_bat)


def format_number(number):
    return number.rjust(4, "0")


def extract_number(transect):
    matcher = search("T*([0-9]+)_", transect)
    if matcher:
        return format_number(matcher.group(1))
    elif transect.isalnum():
        return format_number(transect)
    return transect


def files(filepath, ext):
    has_extension = lambda filename: ospath.splitext(filename)[1].lower() == ext
    is_file = lambda filename: ospath.isfile(ospath.join(filepath, filename)) and has_extension(filename)
    return [ospath.join(filepath, filename) for filename in listdir(filepath) if is_file(filename)]


def csv_as_list(path):
    data = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            data.append(line)
    return data, reader.fieldnames


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


def lines_zonal_stats_parcel(relation, vector, raster, log, nodata, vector_ext=".shp", raster_ext=".asc"):
    lines = []
    cmd = 'C:\Anaconda\envs\geo\python.exe "E:\heitor.guerra\PycharmProjects\pyLiDARForest\metrics\zonal_stats_parcel.py" -v "{}" -r "{}" -n {} -l "{}"'

    relation, fields = csv_as_list(relation)
    vectors = files(vector, vector_ext)
    rasters = files(raster, raster_ext)

    vector = fields[0]
    raster = fields[1]
    obs = fields[2]
    raster_count = "raster_count"
    vector_count = "vector_count"
    for info in relation:
        if info[obs]:
            logging.error("Removing info ({}) based on observation '{}'".format(str(info), info[obs]))
            continue

        info[raster_count] = 0
        info[vector_count] = 0
        transect = extract_number(info[raster])
        for r in rasters:
            if transect == extract_number(r):
                info[raster] = r
                info[raster_count] = info[raster_count] + 1

        for v in vectors:
            if v.lower().find(info[vector].lower()) > 0:
                info[vector] = v
                info[vector_count] = info[vector_count] + 1

        if info[raster_count] == 0 or info[vector_count] == 0:
            logging.error("Removing info ({}) based on counters".format(str(info), info[obs]))
            continue

        lines.append(
            cmd.format(info[vector], info[raster], nodata, ospath.join(log, ospath.basename(info[raster]) + ".log")))
    return lines


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    relation_path = r"G:\Analise_HIPERESPECTRAL\Dados\shape_Lidar_csv.csv"
    vector_path = r"G:\Analise_HIPERESPECTRAL\Dados\parcelas_campo\sirgas"
    raster_path = r"G:\Analise_HIPERESPECTRAL\Dados\Lidar\CHM_1m"
    log_path = r"G:\Analise_HIPERESPECTRAL\scripts"
    bat_path = r"zonal_stats_parcels.bat"

    raster_nodata_value = -9999
    vector_file_extension = ".shp"
    raster_file_extension = ".asc"

    write(bat_path, lines_zonal_stats_parcel(
        relation_path,
        vector_path,
        raster_path,
        log_path,
        raster_nodata_value,
        vector_file_extension,
        raster_file_extension))

    write_multi_thread(bat_path)
