import time

from osgeo import ogr

from stuff.dbutils import dbutils


def geom_from_wkb(geom, epsg):
    return "ST_GeomFromWKB('{}', {})".format(geom, epsg)


def geom_from_wkt(geom, epsg):
    return "ST_GeomFromText('{}', {})".format(geom, epsg)


def names_reference(defn, fid_column="ogc_fid", geom_column="wkb_geometry"):
    names = [fid_column]
    for i in range(0, defn.GetFieldCount()):
        names.append(defn.GetFieldDefn(i).GetNameRef())
    names.append(geom_column)
    return names


def begin_transaction(db):
    db.execute("BEGIN")


def commit_transaction(db):
    db.execute("COMMIT")


def rollback_transaction(db):
    db.execute("ROLLBACK")


def update_row(db, table, data, fid_column, fid_value):
    columns = []
    for field, value in data.iteritems():
        if not value:
            value = "NULL"
        columns.append("{} = {}".format(field, value))
    sql = "UPDATE {} SET {} WHERE {} = {};".format(table, ",".join(columns), fid_column, fid_value)
    return db.execute(sql)


def insert_row(db, table, fields, data):
    data = ["NULL" if v is None else str(v) for v in data[1:]]
    sql = "INSERT INTO {}({}) VALUES({});".format(table, ",".join(fields[1:]), ",".join(data))
    return db.execute(sql)


def steps(db, table, n, fid="ogc_fid"):
    sql = "SELECT MIN({0}), MAX({0}), COUNT({0}) FROM {1};".format(fid, table)

    result = db.getdata(sql)
    result = result[0]
    fid_min = result[0]
    fid_max = result[1]
    step = (fid_max - fid_min) / (n - 1)

    tuples = []
    startswith = fid_min
    for i in range(0, n):
        endswith = startswith + step
        if endswith > fid_max:
            endswith = startswith + (fid_max - startswith) + 1
        tuples.append((startswith, endswith))
        startswith = endswith
    return tuples


if __name__ == '__main__':
    db = dbutils("localhost", "eba", "ebaeba18", "eba", "pg_default")

    conn_str = "PG: host=%s dbname=%s user=%s password=%s" % ("localhost", "eba", "eba", "ebaeba18")
    bouding_box = "vegtype_20170724_132101"

    conn = ogr.Open(conn_str)
    assert conn

    bb = conn.GetLayer(bouding_box)
    assert bb

    srs = bb.GetSpatialRef()
    srs.AutoIdentifyEPSG()
    partial_node = "PROJCS"
    authority_name = srs.GetAuthorityName(partial_node)
    authority_code = srs.GetAuthorityCode(partial_node)

    name = bb.GetName()
    fid_column = bb.GetFIDColumn()
    geom_column = bb.GetGeometryColumn()

    print("Layer name: {}".format(name))
    print("FID column: {}".format(fid_column))
    print("Name of the geometry column: {}".format(geom_column))
    print("Authority name: {}".format(authority_name))
    print("Authority code: {}".format(authority_code))
    print("SpatialRef: {}".format(srs.ExportToWkt()))

    bb_defn = bb.GetLayerDefn()
    fields = names_reference(bb_defn, fid_column, geom_column)

    print("Fields: {}".format(fields))

    #
    # INSERT ROW
    #
    ti = time.clock()

    transaction_cont = 0
    feat = bb.GetNextFeature()
    while feat:
        geometry = feat.geometry()
        fid_value = feat.GetFID()
        wkt = geom_from_wkt(geometry.ExportToWkt(), authority_code)

        if transaction_cont == 0:
            begin_transaction(db)

        data = [fid_value]
        for i in range(0, bb_defn.GetFieldCount()):
            data.append(feat.GetField(i))
        data.append(wkt)
        print(insert_row(db, "vegtype_20170724_155158", fields, data))

        if transaction_cont == 1000:
            commit_transaction(db)
            transaction_cont = 0

        transaction_cont += 1
        feat = bb.GetNextFeature()

    if transaction_cont > 0:
        print("Closing transaction with {} records".format(transaction_cont))
        commit_transaction(db)

    tf_sec = int((time.clock() - ti) % 60)
    tf_min = int((tf_sec / 60) % 60)
    tf_h = int((tf_min / 60) % 24)
    print("Table created with success in {} hours {} minutes {} seconds!".format(tf_h, tf_min, tf_sec))
    print("Total of features read: {}".format(bb.GetFeaturesRead()))

    #
    # UPDATE ROW
    #

    # print("Reset feature reading")
    # bb.ResetReading()

    # print("Reading using step")
    # ti = time.clock()
    #
    # st = steps(db, bouding_box, 8, fid_column)
    # print(st)
    #
    startswith, endswith = 0, bb.GetFeatureCount()
    bb.SetNextByIndex(startswith)

    newtable = "vegtype_20170724_155158"

    transaction_cont = 0
    feat = bb.GetNextFeature()
    while startswith < endswith:
        if transaction_cont == 0:
            begin_transaction(db)

        data = {}
        fid_value = feat.GetFID()
        for i in range(0, bb_defn.GetFieldCount()):
            data[bb_defn.GetFieldDefn(i).GetNameRef()] = feat.GetField(i)

        update_row(db, newtable, data, fid_column, fid_value)

        if transaction_cont == 1000:
            commit_transaction(db)
            transaction_cont = 0

        startswith += 1
        transaction_cont += 1
        feat = bb.GetNextFeature()

    if transaction_cont > 0:
        print("Closing transaction with {} records".format(transaction_cont))
        commit_transaction(db)

    tf_sec = int((time.clock() - ti) % 60)
    tf_min = int((tf_sec / 60) % 60)
    tf_h = int((tf_min / 60) % 24)
    print("Table created with success in {} hours {} minutes {} seconds!".format(tf_h, tf_min, tf_sec))
