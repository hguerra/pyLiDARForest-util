import json
import logging
import os

from osgeo import ogr

from app.db.update.update_columns import UpdateTable


def geom_from_wkt(geom, epsg):
    return "ST_GeomFromText('{}', {})".format(geom, epsg)


def extract_geoms(data):
    ds = ogr.Open(data)
    bb = ds.GetLayer()
    assert bb

    geoms = {}
    duplicated = {}
    authority_code = 5880
    bb_defn = bb.GetLayerDefn()
    feat = bb.GetNextFeature()
    while feat:
        for i in range(0, bb_defn.GetFieldCount()):
            name_ref = bb_defn.GetFieldDefn(i).GetNameRef()
            if name_ref == "TRANSECT":
                field_value = feat.GetField(i)
                number = UpdateTable.extract_number(field_value)
                wkt = geom_from_wkt(feat.geometry().ExportToWkt(), authority_code)
                if number not in geoms:
                    geoms[number] = wkt
                else:
                    logging.error("Duplicate bouding box: {}".format(field_value))
                    duplicated[number] = wkt
        feat = bb.GetNextFeature()
    del ds
    return geoms, duplicated


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    boudingbox = r"E:\heitor.guerra\voados\transects_merged_5880.shp"
    geoms_json = "geoms.json"
    duplicated_json = "geoms_duplicated.json"
    projs_json = r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\db\geom\transects_epsg.json"

    transects_table = "transects"
    transects_select = ["id", "nome_trans", "renomeados", "transect"]
    insert_fields = ["nome_trans", "fuso", "transect", "polyflown"]
    zones = {
        "31968": "14N",
        "31969": "15N",
        "31970": "16N",
        "31971": "17N",
        "31972": "18N",
        "31973": "19N",
        "31974": "20N",
        "31975": "21N",
        "31976": "22N",
        "31977": "17S",
        "31978": "18S",
        "31979": "19S",
        "31980": "20S",
        "31981": "21S",
        "31982": "22S",
        "31983": "23S",
        "31984": "24S",
        "31985": "25S"
    }

    transects = {}
    transects_orm = UpdateTable(transects_table)

    logging.info("Loading geoms...")
    if os.path.isfile(geoms_json) and os.path.isfile(duplicated_json):
        with open(geoms_json, "r") as json_data:
            polyflown = json.load(json_data)
        with open(duplicated_json, "r") as json_data:
            geoms_duplicated = json.load(json_data)
    else:
        logging.info("Extracting geoms...")
        polyflown, geoms_duplicated = extract_geoms(boudingbox)

        logging.info("Writing geoms...")
        with open(geoms_json, "w") as f:
            json.dump(polyflown, f, indent=4, sort_keys=True)

        logging.info("Writing geoms duplicated...")
        with open(duplicated_json, "w") as f:
            json.dump(geoms_duplicated, f, indent=4, sort_keys=True)

    for col in transects_orm.select(transects_select, order_by="nome_trans"):
        pk_id = col[0]
        nome_trans = col[2] or col[1]
        number_transect = col[3]

        number = UpdateTable.extract_number(nome_trans)
        if int(number) == int(number_transect):
            transects[number] = pk_id
        else:
            logging.error("Duplicate transect number: '{}'".format(col))

    # for number, pk_id in transects.iteritems():
    #     if number in polyflown:
    #         geom = polyflown[number]
    #         try:
    #             transects_orm.update({"polyflown": geom}, ["id = {}".format(pk_id)], debug=False)
    #         except Exception as geom_err:
    #             logging.error("Error to process Transect {}: {}".format(number, str(geom_err)))
    #             transects_orm.rollback_transaction()
    #     else:
    #         logging.error("Transect {} not found in geoms".format(number))
    #
    # logging.info("Loading projs...")
    # data = []
    # if os.path.isfile(projs_json):
    #     with open(projs_json, "r") as json_data:
    #         projs = json.load(json_data)
    #
    #         sql_args = "INSERT INTO {}({})".format(transects_table, ",".join(insert_fields))
    #         for number in sorted(polyflown.keys()):
    #             if number not in transects:
    #                 logging.warning("Transect {} not in table '{}'".format(number, transects_table))
    #                 try:
    #                     transects_orm.begin_transaction()
    #                     sql_values = " VALUES({});".format(
    #                         ",".join(["'T_{}'".format(number),
    #                                   "'{}'".format(zones[projs[number]]),
    #                                   str(int(number)), polyflown[number]])
    #                     )
    #                     result = transects_orm.execute(sql_args + sql_values)
    #                     logging.info("Row {} added".format(result))
    #                     transects_orm.commit_transaction()
    #                 except Exception as insert_err:
    #                     logging.error("Error to insert record: {}".format(str(insert_err)))
    #                     transects_orm.rollback_transaction()
    # else:
    #     raise RuntimeError("File '{}' not found".format(projs_json))
    #
    # logging.info("Updating field 'nome_trans'")
    # for number, pk_id in transects.iteritems():
    #     transects_orm.update({"nome_trans": "'T_{}'".format(number)}, ["id = {}".format(pk_id)], debug=False)

    if os.path.isfile(projs_json):
        with open(projs_json, "r") as json_data:
            projs = json.load(json_data)

            logging.info("Updating field 'fuso'")
            for number, pk_id in transects.iteritems():
                if number in projs:
                    transects_orm.update({"fuso": "'{}'".format(zones[projs[number]])}, ["id = {}".format(pk_id)], debug=False)
    else:
        raise RuntimeError("File '{}' not found".format(projs_json))
