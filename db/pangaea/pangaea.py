import logging
import os
from time import time

import pandas as pd
import pandas.io.sql as psql
import psycopg2 as pg


def as_data_frame(sql, pickle="df.pickle", host="localhost", user="eba", password="ebaeba18", database="eba"):
    log_msg = "Loading data frame from '{}'..."

    t0_load = time()
    if os.path.isfile(pickle):
        logging.info(log_msg.format("pickle"))
        df = pd.read_pickle(pickle)
    else:
        connection = pg.connect(host=host, user=user, password=password, database=database)

        logging.info(log_msg.format("PostgreSQL"))
        df = psql.read_sql(sql, connection)
        df.to_pickle(pickle)
    logging.info("Time elapsed to load data: %.2fs" % (time() - t0_load))
    return df


def write_tab(df, filename):
    df.to_csv(filename, sep='\t', index=False, encoding='utf-8')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    select = "filename"
    distinct_pickle = "distinct.pickle"
    pickle_dir = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\pangaea\pickle"
    output_dir = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\pangaea\tab"

    attributes = [
        "filename",
        "x AS longitude",
        "y AS latitude",
        "index_",
        "all_",
        "min",
        "max",
        "avg",
        "qav",
        "std",
        "ske",
        "kur",
        "p01",
        "p05",
        "p10",
        "p20",
        "p25",
        "p30",
        "p40",
        "p50",
        "p60",
        "p70",
        "p75",
        "p80",
        "p90",
        "p95",
        "p99",
        "b05",
        "b10",
        "b20",
        "b30",
        "b40",
        "b50",
        "b60",
        "b70",
        "b80",
        "b90",
        "c00",
        "c01",
        "c02",
        "c03",
        "c04",
        "c05",
        "c06",
        "c07",
        "c08",
        "d00",
        "d01",
        "d02",
        "d03",
        "d04",
        "d05",
        "d06",
        "d07",
        "d08",
        "cov_gap",
        "dns_gap",
        "chm"
    ]

    distinct_sql = "SELECT DISTINCT({0}) AS {0} FROM metrics_new ORDER BY {0};".format(select)
    distinct = as_data_frame(distinct_sql, os.path.join(pickle_dir, distinct_pickle))

    metrics_template_init = "SELECT {} FROM metrics_new WHERE {} = ".format(",".join(attributes), select)
    metrics_template_end = "'{}';"
    for idx, row in distinct.iterrows():
        filename = row[select]
        metric_pickle = os.path.join(pickle_dir, filename + ".pickle")
        output_file = os.path.join(output_dir, filename + ".tab")

        metrics_sql = metrics_template_init + metrics_template_end.format(filename)
        metric = as_data_frame(metrics_sql, metric_pickle)

        logging.info("Writing tab '{}'...".format(filename))
        write_tab(metric, output_file)

    logging.info("Done.")
