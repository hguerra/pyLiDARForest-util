import logging
from os import path, getpid
from re import search

from stuff.dbutils import dbutils


class UpdateTable(object):
    def __init__(self, table, server="localhost", dbname="eba", user="eba", password="ebaeba18",
                 tablespace="pg_default", filename=None):
        db = dbutils(server, user, password, dbname, tablespace)
        assert db

        self._db = db
        self._table = table

        if filename:
            self._sql = open(UpdateTable.new_filename(filename, sulfix=str(getpid())), "a")

    def select_distinct(self, field, conditions=None, order_by=None, debug=False):
        sql = "SELECT DISTINCT({}) FROM {}"
        if conditions:
            where = " WHERE {}".format(" AND ".join(conditions))
            sql += where
        if order_by:
            order_by = " ORDER BY {}".format(order_by)
            sql += order_by
        sql += ";"
        sql = sql.format(field, self._table)
        if debug:
            logging.info(sql)
        else:
            return [row[0] for row in self._db.getdata(sql)]

    def select(self, fields, joins=None, conditions=None, order_by=None, limit=None, debug=False):
        sql = "SELECT {} FROM {}".format(",".join(fields), self._table)
        if joins:
            sql += " {}".format(" ".join(joins))
        if conditions:
            where = " WHERE {}".format(" AND ".join(conditions))
            sql += where
        if order_by:
            order_by = " ORDER BY {}".format(order_by)
            sql += order_by
        if limit:
            limit = " LIMIT {}".format(limit)
            sql += limit
        sql += ";"
        if debug:
            logging.info(sql)
        else:
            return self._db.getdata(sql)

    def update(self, data, conditions, debug=False):
        columns = []
        for field, value in data.iteritems():
            if not value:
                value = "NULL"
            columns.append("{} = {}".format(field, value))
        sql = "UPDATE {} SET {} WHERE {};".format(self._table, ",".join(columns), " AND ".join(conditions))
        if debug:
            logging.info(sql)
        elif hasattr(self, "_sql"):
            self._sql.write(sql + "\n")
        else:
            self.begin_transaction()
            edits = self.execute(sql)
            self.commit_transaction()
            return edits

    def addrec(self, fields, data):
        if not self._db.sqlvalidfieldnames:
            self._db.initsqlvalidfieldnames(fields)
        return self._db.addrecs(self._table, fields, data)

    def execute(self, sql, autocommit=False, ignoreexcept=False):
        return self._db.execute(sql, autocommit, ignoreexcept)

    def begin_transaction(self):
        self.execute("BEGIN")

    def commit_transaction(self):
        self.execute("COMMIT")

    def rollback_transaction(self):
        self.execute("ROLLBACK")

    def close(self):
        if hasattr(self, "_sql"):
            self._sql.close()

    @staticmethod
    def extract_number(transect):
        matcher = search("T*([0-9]+)", transect)
        if matcher:
            return matcher.group(1).rjust(4, "0")
        return transect

    @staticmethod
    def new_filename(filename, prefix="", sulfix=""):
        filepath = path.dirname(filename)
        filename = path.basename(filename)
        filename, ext = path.splitext(filename)
        newfilename = "{}{}{}{}".format(prefix, filename, sulfix, ext)
        return path.join(filepath, newfilename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    metrics_table = "metrics"
    transects_table = "transects"

    metrics_select = "filename"
    transects_select = ["id", "nome_trans", "renomeados"]

    metrics = UpdateTable(metrics_table)
    transects = UpdateTable(transects_table)

    logging.info("Getting distinct '{}' from '{}'".format(metrics_select, metrics_table))
    metr_dist = {UpdateTable.extract_number(transect): transect for transect in metrics.select_distinct(metrics_select)}

    logging.info("Getting '{}' from '{}'".format(transects_select, transects_table))
    trans_dist = {}
    for cols in transects.select(transects_select):
        pk_id = cols[0]
        transect = cols[2] or cols[1]
        trans_dist[UpdateTable.extract_number(transect)] = pk_id

    for number, pk_id in trans_dist.iteritems():
        if number not in metr_dist:
            logging.error("Transect {} not found in metrics table".format(number))
            continue
        metrics.update({"transect_id": pk_id}, ["filename = '{}'".format(metr_dist[number])])
