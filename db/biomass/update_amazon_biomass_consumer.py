import argparse
import json
import logging
import os
import sys
import time

sys.path.append(r'E:\heitor.guerra\PycharmProjects\pyLiDARForest')

from app.db.update.update_columns import UpdateTable


def progress_bar(iteration, total, previous=0.0, prefix='Progress:', suffix='Complete', decimals=1, length=50,
                 fill='#'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        previous    - Optional  : previous progress (Float)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    progress = 100 * (iteration / float(total))
    if round(progress, 1) != round(previous, 1):
        percent = ("{0:." + str(decimals) + "f}").format(progress)
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)

        out = '%s |%s| %s%% %s' % (prefix, bar, percent, suffix)
        logging.info(out)
    return progress


def amazon_consumer(up_metrics, up_amazon, ids, startswith, endswith):
    avgs = ["AVG(agblongo_als_total)", "AVG(agblongo_als_alive)", "AVG(agblongo_tch_total)", "AVG(agblongo_tch_alive)"]
    metrics_fk = "amazon_id = {}"
    amazon_pk = "ogc_fid = {}"

    progress_cont = 0.0
    progress_total = endswith - startswith
    progress_previous = progress_bar(progress_cont, progress_total)
    while startswith < endswith:
        amz_id = ids[startswith]
        averages = up_metrics.select(avgs, conditions=[metrics_fk.format(amz_id)])
        averages = averages[0]

        up_amazon.update({
            "agblongo_als_total": averages[0],
            "agblongo_als_alive": averages[1],
            "agblongo_tch_total": averages[2],
            "agblongo_tch_alive": averages[3]
        }, conditions=[amazon_pk.format(amz_id)])

        progress_cont += 1
        progress_previous = progress_bar(progress_cont, progress_total, progress_previous)
        startswith += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--startswith", type=int, required=True, help="Initial feature identifier.")
    parser.add_argument("-e", "--endswith", type=int, required=True, help="Final feature identifier.")
    parser.add_argument("-j", "--json", type=str, default="distinct_ids.json")
    args = parser.parse_args()

    sqlfile = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\biomass\sql\update_amazon.sql"
    logfile = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\biomass\log\update_amazon_{}_{}.log"
    logging.basicConfig(
        filename=logfile.format(args.startswith, args.endswith),
        level=logging.INFO
    )
    ti = time.clock()

    amazon = UpdateTable("amazon_palsar_hh", filename=sqlfile)
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

    amazon_consumer(metrics, amazon, dist_amazon, args.startswith, args.endswith)
    amazon.close()

    tf_sec = int((time.clock() - ti) % 60)
    tf_min = int((tf_sec / 60) % 60)
    tf_h = int((tf_min / 60) % 24)
    logging.info(
        "{} executed with success in {} hours {} minutes {} seconds!".format(os.path.basename(__file__), tf_h, tf_min,
                                                                             tf_sec))
