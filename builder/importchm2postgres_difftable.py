# -*- coding: utf-8 -*-
import csv
import logging
import os
import os.path as ospath
from os import listdir
from re import search

from stuff.dbutils import dbutils


def extract_number(transect):
    matcher = search("T*([0-9]+)", transect)
    if matcher:
        return matcher.group(1).rjust(4, "0")
    return transect


def files(csv_path):
    csv_extension = ".csv"
    for filename in listdir(csv_path):
        if ospath.splitext(filename)[1] == csv_extension:
            yield ospath.join(csv_path, filename)


def chm(path, nullValue):
    index = "index"
    x = "x"
    y = "y"
    csvValue = "CHM_500"
    value = "chm"

    filename = "filename"
    filenameValue = "T-{}".format(extract_number(os.path.basename(path)))

    nlines = 0
    data = []
    logging.info("Loading CHM '{}' with null value '{}'".format(path, nullValue))
    with open(path, 'r') as f:
        reader = csv.DictReader(f, fieldnames=[index, x, y, csvValue])
        header = reader.next()
        # small bug in generated csv: index,x,y,csv0,731725.000,9677075.000,-
        header = header[None]
        if header[2] != nullValue:
            headerValues = {index: '0', x: header[0], y: header[1], value: header[2], filename: filenameValue}
            data.append(headerValues)
            nlines += 1

        for line in reader:
            if line[csvValue] != nullValue:
                line[value] = line[csvValue]
                line[filename] = filenameValue
                del line[csvValue]
                data.append(line)
                nlines += 1

    ndata = len(data)
    if nlines != ndata:
        logging.error("Number of lines read({}) is different of number of lines added({})",
                      format(str(nlines), str(ndata)))

    return [index, filename, x, y, value], data


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    filepath = r"E:\heitor.guerra\db_insert\CHM_50"
    server = "localhost"
    user = "eba"
    pwd = "ebaeba18"
    database = "eba"
    pgTemplate = "pg_default"

    nullvalue = "-"
    skipfields = 3
    tablename = "chm"

    for f in files(filepath):
        db = dbutils(server, user, pwd, database, pgTemplate)
        fieldnames, data = chm(f, nullvalue)
        db.initsqlvalidfieldnames(fieldnames)
        added = db.addrecs(tablename, fieldnames, data, skipfields, nullvalue)
        logging.info('File {0} imported, {1} lines processed, {2} recs added'.format(f, len(data), added))
