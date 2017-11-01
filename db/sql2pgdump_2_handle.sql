DROP FUNCTION fupdate_amazon_biomass();
CREATE OR REPLACE FUNCTION fupdate_amazon_biomass()
  RETURNS VOID AS $$
DECLARE
    amazon_transects CURSOR FOR SELECT polys.* FROM amazon_palsar polys INNER JOIN transects bb ON ST_Intersects(bb.polyflown, polys.geom);
BEGIN
  FOR amazon IN amazon_transects LOOP
    UPDATE amazon_palsar
    SET agblongo_als_total = metric.agblongo_als_total,
      agblongo_als_alive   = metric.agblongo_als_alive,
      agblongo_tch_total   = metric.agblongo_tch_total,
      agblongo_tch_alive   = metric.agblongo_tch_alive
    FROM (SELECT
            AVG(mt.agblongo_als_total) AS agblongo_als_total,
            AVG(mt.agblongo_als_alive) AS agblongo_als_alive,
            AVG(mt.agblongo_tch_total) AS agblongo_tch_total,
            AVG(mt.agblongo_tch_alive) AS agblongo_tch_alive
          FROM _metrics mt INNER JOIN amazon_palsar amz ON ST_Intersects(amz.geom, mt.geom)
          WHERE amz.fid = amazon.fid AND mt.all_ > 500) AS metric
    WHERE fid = amazon.fid;
  END LOOP;
END$$
LANGUAGE plpgsql;

SELECT fupdate_amazon_biomass();