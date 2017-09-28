-- DROP SEQUENCE public.amazon_palsar_hh_seq;
CREATE SEQUENCE public.amazon_palsar_hh_seq
INCREMENT 1
MINVALUE 1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER TABLE public.amazon_palsar_hh_seq
  OWNER TO eba;

-- Table: public.amazon_palsar_hh

-- DROP TABLE public.amazon_palsar_hh;
CREATE TABLE public.amazon_palsar_hh
(
  ogc_fid            INTEGER NOT NULL DEFAULT nextval('amazon_palsar_hh_seq' :: REGCLASS),
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
  ndvi_sd            DOUBLE PRECISION,
  palsar_hh          DOUBLE PRECISION,
  palsar_hhrhv1      DOUBLE PRECISION,
  palsar_hv          DOUBLE PRECISION,
  geom               GEOMETRY(Polygon, 5880),
  CONSTRAINT amazon_palsar_hh_pkey PRIMARY KEY (ogc_fid)
)
WITH (
OIDS = FALSE
);
ALTER TABLE public.amazon_palsar_hh
  OWNER TO eba;

-- Index: public.amazon_palsar_hh_idx

-- DROP INDEX public.amazon_palsar_hh_idx;

CREATE INDEX amazon_palsar_hh_gix
  ON public.amazon_palsar_hh USING GIST (geom);
