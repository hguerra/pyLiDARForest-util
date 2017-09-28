DROP SEQUENCE public.amazon_roraima_seq;
CREATE SEQUENCE public.amazon_roraima_seq
INCREMENT 1
MINVALUE 1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER TABLE public.amazon_roraima_seq
  OWNER TO postgres;

DROP TABLE amazon_roraima;
CREATE TABLE amazon_roraima (
  id                 INTEGER NOT NULL DEFAULT nextval('amazon_roraima_seq' :: REGCLASS),
  class              VARCHAR(10),
  agblongo_als_total DOUBLE PRECISION,
  agblongo_als_alive DOUBLE PRECISION,
  agblongo_tch_total DOUBLE PRECISION,
  agblongo_tch_alive DOUBLE PRECISION,
  evi_max            DOUBLE PRECISION,
  evi_mean           DOUBLE PRECISION,
  evi_median         DOUBLE PRECISION,
  evi_min            DOUBLE PRECISION,
  evi_q1             DOUBLE PRECISION,
  evi_q3             DOUBLE PRECISION,
  evi_sd             DOUBLE PRECISION,
  ndvi_max           DOUBLE PRECISION,
  ndvi_mean          DOUBLE PRECISION,
  ndvi_median        DOUBLE PRECISION,
  ndvi_min           DOUBLE PRECISION,
  ndvi_q1            DOUBLE PRECISION,
  ndvi_q3            DOUBLE PRECISION,
  palsar_hh          DOUBLE PRECISION,
  palsar_hhrhv1      DOUBLE PRECISION,
  palsar_hv          DOUBLE PRECISION,
  trmm_max           DOUBLE PRECISION,
  trmm_median        DOUBLE PRECISION,
  trmm_min           DOUBLE PRECISION,
  trmm_q1            DOUBLE PRECISION,
  trmm_q3            DOUBLE PRECISION,
  geom               GEOMETRY(Polygon, 5880),
  CONSTRAINT amazon_roraima_pkey PRIMARY KEY (id)
)
WITH (
OIDS = FALSE
);
ALTER TABLE public.amazon_roraima
  OWNER TO eba;

CREATE UNIQUE INDEX amazon_roraima_unique_index
  ON public.amazon_roraima (id);
CREATE INDEX amazon_roraima_gix
  ON public.amazon_roraima USING GIST (geom);

INSERT INTO amazon_roraima (class, agblongo_als_total, agblongo_als_alive, agblongo_tch_total, agblongo_tch_alive, evi_max, evi_mean, evi_median, evi_min, evi_q1, evi_q3, evi_sd, ndvi_max, ndvi_mean, ndvi_median, ndvi_min, ndvi_q1, ndvi_q3, palsar_hh, palsar_hhrhv1, palsar_hv, trmm_max, trmm_median, trmm_min, trmm_q1, trmm_q3, geom)
  SELECT
    fbiomass_classes(polys.agblongo_tch_alive) AS class,
    polys.agblongo_als_total,
    polys.agblongo_als_alive,
    polys.agblongo_tch_total,
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
    polys.trmm_q3,
    polys.geom
  FROM amazon_trmm polys INNER JOIN states bb ON ST_Intersects(bb.geom, polys.geom)
  WHERE bb.gid = 8;