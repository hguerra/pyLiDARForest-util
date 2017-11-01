--DROP SEQUENCE public.amazon_palsar_seq;
CREATE SEQUENCE public.amazon_palsar_seq
INCREMENT 1
MINVALUE 1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER TABLE public.amazon_palsar_seq
  OWNER TO eba;

-- Table: public.amazon_palsar

--DROP TABLE public.amazon_palsar;
CREATE TABLE public.amazon_palsar
(
  fid         INTEGER NOT NULL DEFAULT nextval('amazon_palsar_seq' :: REGCLASS),
  "row"       INTEGER,
  col         INTEGER,
  states_id   INTEGER,
  mosaic_id   INTEGER,
  processed   BOOLEAN          DEFAULT FALSE,
  evi_max     DOUBLE PRECISION,
  evi_mean    DOUBLE PRECISION,
  evi_median  DOUBLE PRECISION,
  evi_min     DOUBLE PRECISION,
  evi_q1      DOUBLE PRECISION,
  evi_q3      DOUBLE PRECISION,
  evi_sd      DOUBLE PRECISION,
  ndvi_max    DOUBLE PRECISION,
  ndvi_mean   DOUBLE PRECISION,
  ndvi_median DOUBLE PRECISION,
  ndvi_min    DOUBLE PRECISION,
  ndvi_q1     DOUBLE PRECISION,
  ndvi_q3     DOUBLE PRECISION,
  ndvi_sd     DOUBLE PRECISION,
  srtm        DOUBLE PRECISION,
  trmm_max    DOUBLE PRECISION,
  trmm_mean   DOUBLE PRECISION,
  trmm_median DOUBLE PRECISION,
  trmm_min    DOUBLE PRECISION,
  trmm_q1     DOUBLE PRECISION,
  trmm_q3     DOUBLE PRECISION,
  trmm_sd     DOUBLE PRECISION,
  f_soil_qr   DOUBLE PRECISION,
  vegetation  DOUBLE PRECISION,
  palsar_hh  DOUBLE PRECISION,
  palsar_hhrhv1  DOUBLE PRECISION,
  palsar_hv  DOUBLE PRECISION,
  geom        GEOMETRY(Polygon, 5880),
  CONSTRAINT amazon_palsar_pkey PRIMARY KEY (fid),
  CONSTRAINT amazon_palsar_states_fkey FOREIGN KEY (states_id)
  REFERENCES public.states (gid) MATCH SIMPLE
  ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT amazon_palsar_mosaic_fkey FOREIGN KEY (mosaic_id)
  REFERENCES public.mosaic (gid) MATCH SIMPLE
  ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
OIDS = FALSE
);
ALTER TABLE public.amazon_palsar
  OWNER TO eba;
