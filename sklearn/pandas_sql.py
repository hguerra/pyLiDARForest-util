import logging
import os
from time import time

import pandas as pd
import pandas.io.sql as psql
import psycopg2 as pg
from sklearn import metrics
from sklearn import svm
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split


def _load_dataframe(pickle="amazon.pickle", host="localhost", user="eba", password="ebaeba18", database="eba"):
    log_msg = "Loading data frame from '{}'..."

    t0_load = time()
    if os.path.isfile(pickle):
        logging.info(log_msg.format("pickle"))
        df = pd.read_pickle(pickle)
    else:
        connection = pg.connect(host=host, user=user, password=password, database=database)
        sql_amazon = """
        SELECT
          st_x(st_centroid(polys.geom)) AS x,
          st_y(st_centroid(polys.geom)) AS y,
          polys.agblongo_tch_alive,
          polys.evi_max,
          polys.evi_mean,
          polys.evi_median,
          polys.evi_min,
          polys.evi_q1,
          polys.evi_q3,
          polys.evi_sd,
          polys.ndvi_max,
          polys.ndvi_mean,
          polys.ndvi_median,
          polys.ndvi_min,
          polys.ndvi_q1,
          polys.ndvi_q3,
          polys.palsar_hh,
          polys.palsar_hhrhv1,
          polys.palsar_hv,
          polys.trmm_max,
          polys.trmm_median,
          polys.trmm_min,
          polys.trmm_q1,
          polys.trmm_q3
        FROM 
          amazon_test polys INNER JOIN transects bb ON ST_Intersects(bb.polyflown, polys.geom)
        WHERE 
          polys.evi_max IS NOT NULL AND
          polys.evi_mean IS NOT NULL AND
          polys.evi_median IS NOT NULL AND
          polys.evi_min IS NOT NULL AND
          polys.evi_q1 IS NOT NULL AND
          polys.evi_q3 IS NOT NULL AND
          polys.evi_sd IS NOT NULL AND
          polys.ndvi_max IS NOT NULL AND
          polys.ndvi_mean IS NOT NULL AND
          polys.ndvi_median IS NOT NULL AND
          polys.ndvi_min IS NOT NULL AND
          polys.ndvi_q1 IS NOT NULL AND
          polys.ndvi_q3 IS NOT NULL AND
          polys.palsar_hh IS NOT NULL AND
          polys.palsar_hhrhv1 IS NOT NULL AND
          polys.palsar_hv IS NOT NULL AND
          polys.trmm_max IS NOT NULL AND
          polys.trmm_median IS NOT NULL AND
          polys.trmm_min IS NOT NULL AND
          polys.trmm_q1 IS NOT NULL AND
          polys.trmm_q3 IS NOT NULL;
        """

        logging.info(log_msg.format("PostgreSQL"))
        df = psql.read_sql(sql_amazon, connection)
        df.to_pickle(amazon_trmm_pickle)
    logging.info("Time elapsed to load data: %.2fs" % (time() - t0_load))
    return df


if __name__ == '__main__':
    #
    # Reference
    # https://thisdata.com/blog/unsupervised-machine-learning-with-one-class-support-vector-machines/
    #
    logging.basicConfig(level=logging.INFO)

    amazon_trmm_pickle = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\sklearn\amazon_transects.pickle"
    data = _load_dataframe(pickle=amazon_trmm_pickle)

    logging.info("EXTRACTING SPATIAL FEATURES...")
    backup_attrs = ["x", "y"]
    spatial = data[backup_attrs]
    data.drop(backup_attrs, axis=1, inplace=True)

    logging.info("MAKING OUR DATA ONE-CLASS...")
    data.loc[(data['agblongo_tch_alive'].isnull()) & (data['agblongo_tch_alive'] < 0), "biomass"] = -1
    data.loc[(data['agblongo_tch_alive'] >= 0) & (data['agblongo_tch_alive'] < 5), "biomass"] = 1
    data.loc[(data['agblongo_tch_alive'] >= 5) & (data['agblongo_tch_alive'] < 10), "biomass"] = 2
    data.loc[(data['agblongo_tch_alive'] >= 10) & (data['agblongo_tch_alive'] < 15), "biomass"] = 3
    data.loc[(data['agblongo_tch_alive'] >= 15) & (data['agblongo_tch_alive'] < 20), "biomass"] = 4
    data.loc[(data['agblongo_tch_alive'] >= 20) & (data['agblongo_tch_alive'] < 25), "biomass"] = 5
    data.loc[(data['agblongo_tch_alive'] >= 25) & (data['agblongo_tch_alive'] < 30), "biomass"] = 6
    data.loc[(data['agblongo_tch_alive'] >= 30) & (data['agblongo_tch_alive'] < 35), "biomass"] = 7
    data.loc[(data['agblongo_tch_alive'] >= 35) & (data['agblongo_tch_alive'] < 40), "biomass"] = 8
    data.loc[(data['agblongo_tch_alive'] >= 40) & (data['agblongo_tch_alive'] < 45), "biomass"] = 9
    data.loc[(data['agblongo_tch_alive'] >= 45) & (data['agblongo_tch_alive'] < 50), "biomass"] = 10
    data.loc[(data['agblongo_tch_alive'] >= 50) & (data['agblongo_tch_alive'] < 60), "biomass"] = 11
    data.loc[(data['agblongo_tch_alive'] >= 60) & (data['agblongo_tch_alive'] < 80), "biomass"] = 12
    data.loc[data['agblongo_tch_alive'] >= 80, "biomass"] = 13

    target = data["biomass"]
    data.drop(["agblongo_tch_alive", "biomass"], axis=1, inplace=True)

    logging.info("NORMALIZING FEATURES...")
    for col in data.columns:
        logging.info("Normalizing '{}'".format(col))
        df = data[col]
        data[col] = (df - df.min()) / (df.max() - df.min())

    outliers = target[target != -1]
    nu = float(outliers.shape[0]) / float(target.shape[0])
    logging.info("outliers.shape: {}, target.shape: {}".format(outliers.shape, target.shape))
    logging.info("outlier fraction: {}".format(nu))

    logging.info("SPLITTING DATA INTO TRAINING AND TEST SETS...")
    train_data, test_data, train_target, test_target = train_test_split(data, target, train_size=0.8)
    logging.info("train_data.shape: {}".format(train_data.shape))

    logging.info("TRAINING THE MODEL...")
    t0_training = time()
    model = svm.OneClassSVM(nu=nu, kernel='rbf', gamma=0.05)
    model.fit(train_data)
    logging.info("Time elapsed to training the model: %.2fs" % (time() - t0_training))

    logging.info("MAKING USE OF THE MODEL...")
    t0_dump = time()
    outputfile = "amazon_oneclass_{}.model".format(str(time()))
    joblib.dump(model, outputfile, compress=9)
    logging.info("Time elapsed to dumping the model: %.2fs" % (time() - t0_dump))

    logging.info("CHECKING ACCURACY OF THE MODEL...")
    t0_check = time()
    preds = model.predict(train_data)
    targs = train_target

    accuracy = metrics.accuracy_score(targs, preds)
    logging.info("accuracy: {}".format(accuracy))
    logging.info("precision: {}".format(metrics.precision_score(targs, preds)))
    # logging.info("recall: {}".format(metrics.recall_score(targs, preds)))
    # logging.info("f1: {}".format(metrics.f1_score(targs, preds)))
    # logging.info("area under curve (auc): {}".format(metrics.roc_auc_score(targs, preds)))
    logging.info("Time elapsed to checking the accuracy of the model: %.2fs" % (time() - t0_check))
