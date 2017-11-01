import logging
import os.path as ospath
from os import listdir
from re import search


def multi_header_template():
    return '''SET python_exe=C:\Anaconda\envs\geo\python.exe
SET script="E:\heitor.guerra\PycharmProjects\pyLiDARForest\stuff\procScriptMultithread.py"
'''


def multi_line_template(processorcores, verbose, inputfname):
    return '%python_exe% %script% -c "{}" -v "{}" "{}"' \
        .format(processorcores, verbose, inputfname)


def line_template(metric_path, chm_path, log_path, metric_file, chm_file):
    return 'C:\Anaconda\envs\geo\python.exe "E:\heitor.guerra\PycharmProjects\pyLiDARForest\stuff\importchm2postgres.py" ' \
           '"{metric_path}\{metric_file}" "{chm_path}\{chm_file}" ' \
           '-s "localhost" -u "eba" -p "ebaeba18" -t "metrics" -d "eba" -sf 3 -nv "-" ' \
           '-l "{log_path}\{metric_file}.log"'.format(metric_path=metric_path, chm_path=chm_path, log_path=log_path,
                                                      metric_file=metric_file, chm_file=chm_file)


def extract_number(transect):
    matcher = search("T*([0-9]+)", transect)
    if matcher:
        return matcher.group(1).rjust(4, "0")
    return transect


def files(csv_path):
    csv_extension = ".csv"
    return {
        extract_number(filename): filename
        for filename in listdir(csv_path)
        if ospath.isfile(ospath.join(csv_path, filename)) and ospath.splitext(filename)[1] == csv_extension
    }


def new_filename(filename, prefix="", sulfix=""):
    path = ospath.dirname(filename)
    filename = ospath.basename(filename)
    filename, ext = ospath.splitext(filename)
    multi_bat = "{}{}{}{}".format(prefix, filename, sulfix, ext)
    return ospath.join(path, multi_bat)


def write(bat, metric_path, chm_path, log_path, processorcores=14, verbose=1):
    multi_bat = new_filename(bat, prefix="multi_thread_")
    metric_files = files(metric_path)
    chm_files = files(chm_path)

    with open(bat, "w") as f:
        keys = sorted(metric_files.keys())
        for transect in keys:
            mpath = metric_files[transect]
            if transect in chm_files:
                cpath = chm_files[transect]
                try:
                    f.write(line_template(metric_path, chm_path, log_path, mpath, cpath) + "\n")
                    logging.info("Command appended with success")
                except Exception as writeErr:
                    logging.error("Error to append transect '{}': {}".format(transect, str(writeErr)))
            else:
                logging.error("CHM {} not found.".format(transect))

    with open(multi_bat, "w") as f:
        f.write(multi_header_template() + "\n")
        try:
            f.write(multi_line_template(processorcores, verbose, bat) + "\n")
            logging.info("Command appended with success")
        except Exception as writeErr:
            logging.error("Error to append : {}".format(str(writeErr)))


if __name__ == "__main__":
    metric_path = r"E:\heitor.guerra\db_insert\metrics"
    chm_path = r"E:\heitor.guerra\db_insert\chm"
    log_path = r"E:\heitor.guerra\db_insert\metrics"
    bat = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\builder\exe\app_importchmcsv.bat"

    logging.basicConfig(level=logging.INFO)
    write(bat, metric_path, chm_path, log_path)
