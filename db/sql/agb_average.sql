--DROP SEQUENCE public.agb_average_seq;
CREATE SEQUENCE public.agb_average_seq
INCREMENT 1
MINVALUE 1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER TABLE public.agb_average_seq
  OWNER TO postgres;

-- DROP TABLE agb_average;
CREATE TABLE agb_average (
  id                 INTEGER NOT NULL DEFAULT nextval('agb_average_seq' :: REGCLASS),
  transect_id        INTEGER,
  filename           CHARACTER VARYING(32),
  agblongo_als_total DOUBLE PRECISION,
  agblongo_als_alive DOUBLE PRECISION,
  agblongo_tch_total DOUBLE PRECISION,
  agblongo_tch_alive DOUBLE PRECISION,
  CONSTRAINT agb_average_pkey PRIMARY KEY (id)
);

SELECT AddGeometryColumn('public', 'agb_average', 'geom', 5880, 'POINT', 2);

CREATE UNIQUE INDEX agb_average_unique_index
  ON public.agb_average (id);
CREATE INDEX agb_average_gix
  ON public.agb_average USING GIST (geom);

INSERT INTO agb_average (transect_id, filename, agblongo_als_total, agblongo_als_alive, agblongo_tch_total, agblongo_tch_alive, geom)
  SELECT
    metric.transect_id,
    metric.filename,
    AVG(metric.agblongo_als_total) AS agblongo_als_total,
    AVG(metric.agblongo_als_alive) AS agblongo_als_alive,
    AVG(metric.agblongo_tch_total) AS agblongo_tch_total,
    AVG(metric.agblongo_tch_alive) AS agblongo_tch_alive,
    ST_SetSRID(st_centroid(transect.polyflown), 5880)
  FROM metrics metric INNER JOIN transects transect ON metric.transect_id = transect.id
  GROUP BY metric.transect_id, metric.filename, transect.polyflown
  ORDER BY metric.filename;
