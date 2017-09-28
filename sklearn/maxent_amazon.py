import logging
import os
import sys
from time import time

import pandas as pd
import pandas.io.sql as psql
import psycopg2 as pg
from sklearn import metrics
from sklearn import svm
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split


def load_dataframe(pickle="amazon.pickle", host="localhost", user="eba", password="ebaeba18", database="eba"):
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
        df.to_pickle(pickle)
    logging.info("Time elapsed to load data: %.2fs" % (time() - t0_load))
    return df


def extract_spatial_features(df, features=["x", "y"]):
    logging.info("Extracting spatial features...")

    spatial = df[features]
    df.drop(features, axis=1, inplace=True)
    return spatial


def making_one_class(df, column, newcolumn, class_min, class_max):
    logging.info("Making data one class...")

    df.loc[(df[column].isnull()) | (df[column] < class_min) | (df[column] >= class_max), newcolumn] = 1.0
    df.loc[(df[column] >= class_min) & (df[column] < class_max), newcolumn] = -1.0

    df_target = df[newcolumn]
    df.drop([column, newcolumn], axis=1, inplace=True)
    return df_target


def normalize(df):
    logging.info("Normalizing features...")

    for col in df.columns:
        logging.info("Normalizing '{}'".format(col))
        norm = df[col]
        df[col] = (norm - norm.min()) / (norm.max() - norm.min())


def get_outliers(target):
    return target[target == -1.0]


def split_data(df, outliers, target, train_size=0.8):
    logging.info("Calculating outlier fraction(nu)...")

    nu = float(outliers.shape[0]) / float(target.shape[0])
    logging.info("outliers.shape: {}, target.shape: {}".format(outliers.shape, target.shape))
    logging.info("outlier fraction: {}".format(nu))

    logging.info("Splitting data into training and tests sets...")
    train_data, test_data, train_target, test_target = train_test_split(df, target, train_size=train_size)

    logging.info("train_data.shape: {}".format(train_data.shape))

    return nu, train_data, test_data, train_target, test_target


def standardize_features(train):
    logging.info("Standardize features...")

    mean = train.mean(axis=0)
    std = train.std(axis=0)
    return (train - mean) / std


def training(train_std, outlier_fraction, kernel="rbf", gamma=0.00005):
    model_svm = svm.OneClassSVM(nu=outlier_fraction, kernel=kernel, gamma=gamma)
    model_svm.fit(train_std)

    return model_svm


def accuracy_score(model, pred_data, targets):
    preds = model.predict(pred_data)
    accuracy = metrics.accuracy_score(targets, preds)
    precision = metrics.precision_score(targets, preds)
    recall = metrics.recall_score(targets, preds)
    f1 = metrics.f1_score(targets, preds)
    auc = metrics.roc_auc_score(targets, preds)

    return accuracy, precision, recall, f1, auc


def dump_model(model, outputfile):
    joblib.dump(model, outputfile, compress=9)


def calibration(train_std, train_data, train_target, outlier_fraction, cicles=10):
    best_accuracy = (-sys.maxint, 0)
    worst_accuracy = (sys.maxint, 0)

    count = 0
    increment = 0.00001
    gamma = increment
    progress_previous = progress_bar(count, cicles)

    while count < cicles:
        model = training(train_std=train_std, outlier_fraction=outlier_fraction, gamma=gamma)
        accuracy = accuracy_score(model=model, pred_data=train_data, targets=train_target)[0]

        if accuracy > best_accuracy[0]:
            best_accuracy = (accuracy, gamma)
        elif accuracy < worst_accuracy[0]:
            worst_accuracy = (accuracy, gamma)
        gamma += increment
        count += 1
        progress_previous = progress_bar(count, cicles, progress_previous)
    return best_accuracy, worst_accuracy


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


if __name__ == '__main__':
    #
    # Reference
    # https://thisdata.com/blog/unsupervised-machine-learning-with-one-class-support-vector-machines/
    #
    logging.basicConfig(level=logging.INFO)

    amazon_trmm_pickle = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\sklearn\amazon_transects.pickle"
    column_subject = "agblongo_tch_alive"
    column_target = "biomass"
    outputfile = "amazon_oneclass_{}.model".format(str(time()))

    data = load_dataframe(pickle=amazon_trmm_pickle)
    # sp = extract_spatial_features(data)

    target = making_one_class(data, column=column_subject, newcolumn=column_target, class_min=15, class_max=20)
    outliers = get_outliers(target)

    normalize(data)

    nu, train_data, test_data, train_target, test_target = split_data(df=data, outliers=outliers, target=target)
    train_data_std = standardize_features(train=train_data)

    # logging.info("Training the model...")
    # t0_training = time()
    # model = training(train_std=train_data_std, outlier_fraction=nu)
    # logging.info("Time elapsed to training the model: %.2fs" % (time() - t0_training))
    #
    # score = accuracy_score(model=model, pred_data=train_data, targets=train_target)
    # logging.info("Checking accuracy of test set: {}".format(score))
    #
    # score = accuracy_score(model=model, pred_data=test_data, targets=test_target)
    # logging.info("Checking accuracy of test set: {}".format(score))

    logging.info("Training the model...")
    t0_training = time()

    b, w = calibration(train_std=train_data_std, train_data=train_data, train_target=train_target, outlier_fraction=nu, cicles=5)
    logging.info("Best: {}".format(b))
    logging.info("Worst: {}".format(w))

    logging.info("Time elapsed to training the model: %.2fs" % (time() - t0_training))
