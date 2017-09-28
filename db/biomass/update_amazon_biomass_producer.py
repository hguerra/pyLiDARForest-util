import argparse
import json
import logging
import multiprocessing
import os
import sys
import time

sys.path.append(r'E:\heitor.guerra\PycharmProjects\pyLiDARForest')
from app.db.update.update_columns import UpdateTable


def multi_thread_header():
    return '''SET python_exe=C:\Anaconda\envs\geo\python.exe
SET script="E:\heitor.guerra\PycharmProjects\pyLiDARForest\stuff\procScriptMultithread.py"'''


def multi_thread_line(processorcores, verbose, inputfname):
    return '%python_exe% %script% -c "{}" -v "{}" "{}"'.format(processorcores, verbose, inputfname)


def new_filename(filename, prefix="", sulfix=""):
    path = os.path.dirname(filename)
    filename = os.path.basename(filename)
    filename, ext = os.path.splitext(filename)
    multi_bat = "{}{}{}{}".format(prefix, filename, sulfix, ext)
    return os.path.join(path, multi_bat)


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


def get_steps(values, n=8):
    steps = []
    fid_count = len(values)
    if fid_count > 0:
        fid_min = 0
        fid_max = fid_count - 1
        step = fid_count / (n - 1)

        startswith = fid_min
        for i in range(0, n):
            endswith = startswith + step
            if endswith > fid_max:
                endswith = startswith + (fid_max - startswith) + 1
            steps.append((startswith, endswith))
            startswith = endswith
    return steps


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json", type=str, default="distinct_ids.json")
    parser.add_argument("-bat", "--bat", type=str, default="update_amazon.bat")
    parser.add_argument("-c", "--cores", type=int, default=multiprocessing.cpu_count())
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    interpreter = r"C:\Anaconda\envs\geo\python.exe"
    script = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\biomass\update_amazon_biomass_consumer.py"
    cmd = '{} "{}" -s {} -e {}'

    ti = time.clock()

    metrics = UpdateTable("metrics")

    logging.info("Loading distinct ids...")
    if os.path.isfile(args.json):
        with open(args.json, "r") as json_data:
            dist_amazon = json.load(json_data)
    else:
        dist_amazon = metrics.select_distinct("amazon_id", conditions=["amazon_id IS NOT NULL"],
                                              order_by="amazon_id")
        with open(args.json, "w") as f:
            json.dump(dist_amazon, f, indent=4, sort_keys=True)

    lines = []
    for step in get_steps(dist_amazon, n=args.cores):
        lines.append(cmd.format(interpreter, script, step[0], step[1]))

    write(args.bat, lines)
    write_multi_thread(args.bat, cores=args.cores)

    tf_sec = int((time.clock() - ti) % 60)
    tf_min = int((tf_sec / 60) % 60)
    tf_h = int((tf_min / 60) % 24)
    logging.info("{} executed with success in {} hours {} minutes {} seconds!".format(os.path.basename(__file__),
                                                                                      tf_h, tf_min, tf_sec))
