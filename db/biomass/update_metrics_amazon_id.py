import logging

from app.db.update.update_columns import UpdateTable


def geom_from_wkt(geom, epsg=5880):
    return "ST_GeomFromText('{}', {})".format(geom, epsg)


def update_metrics(up_transects, up_amazon, up_metrics):
    amazon_fields = ["fid", "ST_AsText(geom)"]
    amazon_intersects = ["INNER JOIN transects bb ON ST_Intersects(bb.polyflown, geom)"]
    for transect_id in up_transects.select(["id"]):
        transect_id = transect_id[0]
        result = up_amazon.select(amazon_fields, joins=amazon_intersects, conditions=["bb.id = {}".format(transect_id)])
        for rows in result:
            amazon_id = rows[0]
            geom = rows[1]
            up_metrics.update({"amazon_id": amazon_id},
                              conditions=["ST_Intersects({}, geom)".format(geom_from_wkt(geom))])
        else:
            logging.warning("No cell intersects with Transect {}".format(transect_id))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    distinct_ids_json = "distinct_ids.json"

    transects = UpdateTable("transects")
    amazon = UpdateTable("amazon_palsar_hh")
    metrics = UpdateTable("metrics")

    update_metrics(transects, amazon, metrics)
