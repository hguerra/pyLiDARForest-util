import csv
import logging
import multiprocessing
import os.path as ospath
from os import listdir
from re import search

from stuff.dbutils import dbutils


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


def extract_number(transect):
    matcher = search("T*([0-9]+)", transect)
    if matcher:
        return matcher.group(1).rjust(4, "0")
    return transect


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


def lines_warp(bouding_box, raster_path):
    rasters = files(raster_path, ".tif")
    cmd = r'"C:\Anaconda\envs\geo\Library\bin\gdalwarp.exe" -q -cutline "{}" -crop_to_cutline -of GTiff "{}" "{}"'
    line = lambda raster: cmd.format(bouding_box, raster, new_filename(raster, prefix="clipped_"))
    return [line(raster) for raster in rasters]


def lines_merge(outputfile, raster_path, prefix=None, ext=".tif", batch=False, size=100, nodata=-9999):
    interpreter = r"C:\Anaconda\envs\geo\python.exe"
    script = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\gdal\scripts\gdal_merge.py"
    cmd = r'{0} "{1}" -a_nodata {2} -of GTiff -o "{3}" {4}'

    inputfiles = []
    for filename in listdir(raster_path):
        if prefix and not filename.startswith(prefix):
            continue
        filepath = ospath.join(raster_path, filename)
        if ospath.isfile(filepath) and ospath.splitext(filename)[1].lower() == ext:
            inputfiles.append('"{}"'.format(filepath))
    inputfiles.sort()

    lines = []
    if batch:
        lenght = len(inputfiles) / size
        for i in range(lenght):
            lines.append(cmd.format(interpreter, script, nodata, new_filename(outputfile, prefix="{}_".format(i)),
                                    " ".join(inputfiles[:size])))
            del inputfiles[:size]

        rest = len(inputfiles) % size
        if rest > 0:
            lines.append(cmd.format(interpreter, script, nodata, new_filename(outputfile, prefix="{}_".format(lenght)),
                                    " ".join(inputfiles[:rest])))
            del inputfiles[:rest]
    else:
        lines = [cmd.format(interpreter, script, nodata, outputfile, " ".join(inputfiles))]
    return lines


def lines_vrt(outputfile, raster_path, prefix=None, ext=".tif", batch=False, size=100):
    script = r"C:\Anaconda\envs\geo\Library\bin\gdalbuildvrt.exe"
    cmd = r'"{}" "{}" {}'

    inputfiles = []
    for filename in listdir(raster_path):
        if prefix and not filename.startswith(prefix):
            continue
        filepath = ospath.join(raster_path, filename)
        if ospath.isfile(filepath) and ospath.splitext(filename)[1].lower() == ext:
            inputfiles.append('"{}"'.format(filepath))
    inputfiles.sort()

    lines = []
    if batch:
        lenght = len(inputfiles) / size
        for i in range(lenght):
            lines.append(
                cmd.format(script, new_filename(outputfile, prefix="{}_".format(i)), " ".join(inputfiles[:size])))
            del inputfiles[:size]

        rest = len(inputfiles) % size
        if rest > 0:
            lines.append(
                cmd.format(script, new_filename(outputfile, prefix="{}_".format(lenght)), " ".join(inputfiles[:rest])))
            del inputfiles[:rest]
    else:
        lines = [cmd.format(script, outputfile, " ".join(inputfiles))]
    return lines


def lines_reproject(data_path, ext, epsg, vector=True):
    cmd = '"C:\\Anaconda\\envs\geo\\Library\\bin\\'
    if vector:
        cmd = cmd + 'ogr2ogr.exe" "{output}" -t_srs "EPSG:{epsg}" "{input}"'
    else:
        cmd = cmd + 'gdalwarp.exe" -t_srs "EPSG:{epsg}" "{input}" "{output}"'

    dataset = files(data_path, ext)
    line = lambda data, epsg: cmd.format(epsg=epsg, input=data, output=new_filename(data, prefix="{}_".format(epsg)))
    return [line(data, epsg) for data in dataset]


def lines_convert(data_path, input_ext, output_ext, format, epsg=5880, vector=True):
    cmd = '"C:\\Anaconda\\envs\geo\\Library\\bin\\'
    if vector:
        cmd = cmd + 'ogr2ogr.exe" -f "{format}" -t_srs "EPSG:{epsg}" "{output}" "{input}"'
    else:
        cmd = cmd + 'gdal_translate.exe" -of "{format}" -a_srs "EPSG:{epsg}" "{input}" "{output}"'

    dataset = files(data_path, input_ext)
    line = lambda data, epsg: cmd.format(format=format, epsg=epsg, input=data,
                                         output=new_filename(data, prefix="{}_".format(epsg), extension=output_ext))
    return [line(data, epsg) for data in dataset]


def lines_zonal_stats_grid(table, raster_path, log_path):
    rasters = files(raster_path, ".tif")
    cmd = 'C:\Anaconda\envs\geo\python.exe "E:\heitor.guerra\PycharmProjects\pyLiDARForest\metrics\zonal_stats_grid.py" -v "{}" -r "{}" -l "{}"'
    line = lambda raster: cmd.format(table, raster, ospath.join(log_path, ospath.basename(raster) + ".log"))
    return [line(raster) for raster in rasters]


def lines_zonal_stats_parcel(relation, vector, raster, log, vector_ext=".shp", raster_ext=".asc"):
    lines = []
    cmd = 'C:\Anaconda\envs\geo\python.exe "E:\heitor.guerra\PycharmProjects\pyLiDARForest\metrics\zonal_stats_parcel.py" -v "{}" -r "{}" -l "{}"'

    relation, fields = csv_as_list(relation)
    vectors = files(vector, vector_ext)
    rasters = files(raster, raster_ext)

    vector = fields[0]
    raster = fields[1]
    obs = fields[2]
    raster_count = "raster_count"
    vector_count = "vector_count"
    for info in relation:
        print(info)

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

        lines.append(cmd.format(info[vector], info[raster], ospath.join(log, ospath.basename(info[raster]) + ".log")))
    return lines


def lines_zonal_stats_parallel(boudingbox, table, raster_path, log_path, fid="ogc_fid", cores=8):
    db = dbutils("localhost", "eba", "ebaeba18", "eba", "pg_default")

    sql = "SELECT MIN({0}), MAX({0}), COUNT({0}) FROM {1};".format(fid, boudingbox)
    interpreter = r"C:\Anaconda\envs\geo\python.exe"
    script = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\stuff\zonal_stats_grid_parallel.py"
    cmd = '{} "{}" -b "{}" -t "{}" -r "{}" -s {} -e {} -l "{}"'

    result = db.getdata(sql)
    result = result[0]
    fid_min = result[0]
    fid_max = result[1]
    fid_count = result[2]

    fid_min -= 1
    step = fid_count / (cores - 1)
    startswith = fid_min
    lines = []
    for i in range(0, cores):
        endswith = startswith + step
        if endswith > fid_max:
            endswith = startswith + (fid_max - startswith) + 1
        log = ospath.join(log_path, "{}_{}_{}.log".format(table, startswith, endswith))
        lines.append(cmd.format(interpreter, script, boudingbox, table, raster_path, startswith, endswith, log))
        startswith = endswith
    return lines


def lines_extract_raster(table, mosaic, raster, output, log_path, attributes, table_fkey="mosaic_id", mosaic_fid="gid",
                         mosaic_geom="geom"):
    db = dbutils("localhost", "eba", "ebaeba18", "eba", "pg_default")

    interpreter = r"C:\Anaconda\envs\geo\python.exe"
    script = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\stuff\extract_raster.py"
    cmd = '{} "{}" -s "{}" -r "{}" -o "{}" -b "{}" -a {} -l "{}"'

    statement = "select {} from {}".format(",".join(attributes + [mosaic_geom]), table)
    condition = " where {} = {} "
    sql = "SELECT {} FROM {};".format(mosaic_fid, mosaic)
    arguments = ['"{}"'.format(attr) for attr in attributes]
    arguments = " ".join(arguments)

    lines = []
    fids = db.getdata(sql)
    for tup in fids:
        fid = tup[0]
        statement_line = statement + condition.format(table_fkey, fid)
        lines.append(statement_line)

    for i, statement_line in enumerate(lines):
        statement_line += "and " + " is not null and ".join(attributes) + " is not null"
        fid = str(i + 1)
        log = ospath.join(log_path, "{}_{}.log".format(mosaic, fid))
        lines[i] = cmd.format(interpreter, script, statement_line, raster, output, str(fid), arguments, log)
    return lines


def write_update_sql(bat_basename, sql_path, mode="w"):
    sqls = files(sql_path, ".sql")
    cmd = 'SET PGPASSWORD=ebaeba18\n"C:\\Program Files\\PostgreSQL\\9.6\\bin\\psql.exe" -U eba -d eba -f "{}"'
    count = 1
    for content in [cmd.format(sql) for sql in sqls]:
        bat_name = new_filename(bat_basename, sulfix="_{}".format(count))
        with open(bat_name, mode) as f:
            try:
                f.write(content)
                logging.info("Command appended with success")
                count += 1
            except Exception as writeErr:
                logging.error("Error to append '{}': {}".format(content, str(writeErr)))


def write_run_sql(bat_basename, table, fid="id", mode="w", command="SELECT fupdate_amazon_biomass({});"):
    db = dbutils("localhost", "eba", "ebaeba18", "eba", "pg_default")
    sql = "SELECT {0} FROM {1} ORDER BY {0};".format(fid, table)
    cmd = 'SET PGPASSWORD=ebaeba18\n"C:\\Program Files\\PostgreSQL\\9.6\\bin\\psql.exe" -U eba -d eba -c "{}"'.format(command)

    count = 1
    for row in db.getdata(sql):
        content = row[0]
        bat_name = new_filename(bat_basename, sulfix="_{}".format(count))
        with open(bat_name, mode) as f:
            try:
                f.write(cmd.format(content))
                logging.info("Command appended with success")
                count += 1
            except Exception as writeErr:
                logging.error("Error to append '{}': {}".format(content, str(writeErr)))

    write(bat_basename, files(ospath.dirname(ospath.abspath(bat_basename)), ".bat"))
    write_multi_thread(bat_basename, cores=multiprocessing.cpu_count())


def gdalmerge_tiles(prefix, outputfile, path, ext="", batch=True):
    outputfile = new_filename(outputfile, prefix="{}_".format(prefix))
    return lines_merge(outputfile, path, prefix=prefix, ext=ext, batch=batch)


def gdalmerge_grid(file):
    output = r"E:\heitor.guerra\db_backup\rasters\mosaic\{}.tif".format(file)
    raster_path = r"E:\heitor.guerra\db_backup\rasters\{}".format(file)
    return lines_merge(output, raster_path, ext=".tif", nodata=-340282346638528859811704183484516925440.000000,
                       batch=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bat_base = "E:\\heitor.guerra\\PycharmProjects\\pyLiDARForest\\app\\builder\exe\\"

    # # gdalwarp

    # bouding_box = r"E:\heitor.guerra\bouding_box_amazon\biome.shp"
    # raster_path = r"E:\heitor.guerra\tests"
    # bat = bat_base + "app_gdalwarp.bat"
    # write(bat, lines_warp(bouding_box, raster_path))
    # write_multi_thread(bat)

    # gdalmerge_tiles
    # merges = (
    #     # gdalmerge_grid("ndvi_mean") +
    #     # gdalmerge_grid("ndvi_max") +
    #     # gdalmerge_grid("ndvi_median") +
    #     # gdalmerge_grid("ndvi_min") +
    #     # gdalmerge_grid("ndvi_q1") +
    #     # gdalmerge_grid("ndvi_q3") +
    #     # gdalmerge_grid("evi_max")
    #     # gdalmerge_grid("evi_mean") +
    #     # gdalmerge_grid("evi_median") +
    #     # gdalmerge_grid("evi_min") +
    #     # gdalmerge_grid("evi_q1") +
    #     # gdalmerge_grid("evi_q3") +
    #     # gdalmerge_grid("evi_sd") +
    #     # gdalmerge_grid("palsar_hhrhv") +
    #     # gdalmerge_grid("palsar_hv") +
    #     # gdalmerge_grid("palsar_hh") +
    #     # gdalmerge_grid("trmm_median") +
    #     # gdalmerge_grid("trmm_max") +
    #     # gdalmerge_grid("trmm_min") +
    #     # gdalmerge_grid("trmm_q1") +
    #     # gdalmerge_grid("trmm_q3")
    # )
    #
    # bat = bat_base + "app_gdalmerge_random_forest.bat"
    # write(bat, gdalmerge_grid("random_forest"))

    # merges = (
    #     gdalmerge_tiles("N00", output, raster_path) +
    #     gdalmerge_tiles("N01", output, raster_path) +
    #     gdalmerge_tiles("N02", output, raster_path) +
    #     gdalmerge_tiles("N03", output, raster_path) +
    #     gdalmerge_tiles("N04", output, raster_path) +
    #     gdalmerge_tiles("N05", output, raster_path) +
    #     gdalmerge_tiles("N06", output, raster_path) +
    #     gdalmerge_tiles("N07", output, raster_path) +
    #     gdalmerge_tiles("N08", output, raster_path) +
    #     gdalmerge_tiles("N09", output, raster_path) +
    #     gdalmerge_tiles("N10", output, raster_path) +
    #     gdalmerge_tiles("S01", output, raster_path) +
    #     gdalmerge_tiles("S02", output, raster_path) +
    #     gdalmerge_tiles("S03", output, raster_path) +
    #     gdalmerge_tiles("S04", output, raster_path) +
    #     gdalmerge_tiles("S05", output, raster_path) +
    #     gdalmerge_tiles("S06", output, raster_path) +
    #     gdalmerge_tiles("S07", output, raster_path) +
    #     gdalmerge_tiles("S08", output, raster_path) +
    #     gdalmerge_tiles("S09", output, raster_path) +
    #     gdalmerge_tiles("S10", output, raster_path) +
    #     gdalmerge_tiles("S11", output, raster_path) +
    #     gdalmerge_tiles("S12", output, raster_path) +
    #     gdalmerge_tiles("S13", output, raster_path) +
    #     gdalmerge_tiles("S14", output, raster_path) +
    #     gdalmerge_tiles("S15", output, raster_path) +
    #     gdalmerge_tiles("S16", output, raster_path) +
    #     gdalmerge_tiles("S17", output, raster_path) +
    #     gdalmerge_tiles("S18", output, raster_path) +
    #     gdalmerge_tiles("S19", output, raster_path) +
    #     gdalmerge_tiles("S20", output, raster_path)
    # )
    #
    # write(bat, merges)
    # write_multi_thread(bat, cores=10)

    # simple merge
    # output_file = r"E:\heitor.guerra\db_backup\rasters\out.tif"
    # raster_path = r"E:\heitor.guerra\db_backup\rasters\test"
    # bat = bat_base + "simple_merge.bat"
    # write(bat, lines_merge(output_file, raster_path))

    # reproject

    # data_path = r"E:\heitor.guerra\DADOS_PARA_EXTRAPOLAR"
    # ext = ".tif"
    # epsg = 5880
    # bat = bat_base + "app_reproject.bat"
    # write(bat, lines_reproject(data_path, ext, epsg, vector=False))
    # write_multi_thread(bat)

    # zonal_stats_grid.py

    # table = r"vegtype_test"
    # raster_path = r"E:\heitor.guerra\tests\extrapolar"
    # log_path = r"E:\heitor.guerra\db_insert\zonal_stats\log\extrapolar"
    # bat = bat_base + "app_zonal_stats_grid.bat"
    # write(bat, lines_zonal_stats_grid(table, raster_path, log_path))
    # write_multi_thread(bat)

    # zonal_stats.py

    # relation_path = r"E:\heitor.guerra\CURSO_AMAPA\parcelas_shape.csv"
    # vector_path = r"E:\heitor.guerra\CURSO_AMAPA\shapes"
    # raster_path = r"E:\heitor.guerra\CURSO_AMAPA\asc"
    # log_path = r"E:\heitor.guerra\CURSO_AMAPA\log"
    # bat = bat_base + "zonal_stats_parcels.bat"
    # write(bat, lines_zonal_stats_parcel(relation_path, vector_path, raster_path, log_path))
    # write_multi_thread(bat)

    # zonal_stats_grid_parallel.py

    boudingbox = r"amazon"
    table = r"amazon_trmm_new"
    raster_path = r"E:\heitor.guerra\db_insert\zonal_stats\rasters\part_3"
    log_path = r"E:\heitor.guerra\db_insert\zonal_stats\log\extrapolar"
    cores = 10
    bat = bat_base + "zs_{}.bat".format(cores)

    write(bat, lines_zonal_stats_parallel(boudingbox, table, raster_path, log_path, fid="fid", cores=cores * 20))
    write_multi_thread(bat, cores=cores)

    # sql2pgdump

    # bat = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\biomass\exe\app_update_amazon.bat"
    # sql_path = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\biomass\sql"
    # write_update_sql(bat, sql_path)
    # write_multi_thread(bat)

    # SQL command
    # table = "transects"
    # bat = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\builder\exe\chm\fupdate_amazon_chm.bat"
    # write_run_sql(bat, table, command="SELECT fupdate_amazon_chm({});")

    # Extract raster
    # bat = bat_base + "extract_raster.bat"
    # log_path = r"E:\heitor.guerra\db_backup\rasters\log"
    # raster = r"E:\heitor.guerra\tests\extrapolar\EVI_max.tif"
    # output = r"E:\heitor.guerra\db_backup\rasters\test"
    # mosaic = "mosaic"
    # table = "amazon"
    # # attributes = ["evi_max", "evi_mean", "evi_median", "evi_min", "evi_q1", "evi_q3", "evi_sd",
    # #               "ndvi_max", "ndvi_mean", "ndvi_median", "ndvi_min", "ndvi_q1", "ndvi_q3",
    # #               "palsar_hh", "palsar_hhrhv1", "palsar_hv",
    # #               "trmm_max", "trmm_median", "trmm_min", "trmm_q1", "trmm_q3"]
    # # attributes = ["random_forest"]
    # attributes = ["row"]
    # write(bat, lines_extract_raster(table, mosaic, raster, output, log_path, attributes))
    # write_multi_thread(bat)

    # Convert
    # data_path = r"E:\heitor.guerra\db_backup\rasters\mosaic"
    # bat = bat_base + "app_translate.bat"
    # write(bat, lines_convert(data_path, ".tif", ".asc", "AAIGrid", vector=False))
