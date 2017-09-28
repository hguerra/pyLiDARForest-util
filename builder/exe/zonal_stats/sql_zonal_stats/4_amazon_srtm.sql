-- DROP SEQUENCE public.amazon_srtm_seq;
CREATE SEQUENCE public.amazon_srtm_seq
INCREMENT 1
MINVALUE 1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER TABLE public.amazon_srtm_seq
  OWNER TO eba;

-- Table: public.amazon_srtm

-- DROP TABLE public.amazon_srtm;
CREATE TABLE public.amazon_srtm
(
  ogc_fid     INTEGER NOT NULL DEFAULT nextval('amazon_srtm_seq' :: REGCLASS),
  states_id   INTEGER,
  "row"       INTEGER,
  col         INTEGER,
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
  trmm_max    DOUBLE PRECISION,
  trmm_mean   DOUBLE PRECISION,
  trmm_median DOUBLE PRECISION,
  trmm_min    DOUBLE PRECISION,
  trmm_q1     DOUBLE PRECISION,
  trmm_q3     DOUBLE PRECISION,
  trmm_sd     DOUBLE PRECISION,
  srtm        DOUBLE PRECISION,
  geom        GEOMETRY(Polygon, 5880),
  CONSTRAINT amazon_srtm_pkey PRIMARY KEY (ogc_fid),
  CONSTRAINT amazon_srtm_fkey FOREIGN KEY (states_id)
  REFERENCES public.states (gid) MATCH SIMPLE
  ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
OIDS = FALSE
);
ALTER TABLE public.amazon_srtm
  OWNER TO eba;

-- Index: public.amazon_srtm_idx

-- DROP INDEX public.amazon_srtm_idx;

CREATE INDEX amazon_srtm_gix
  ON public.amazon_srtm USING GIST (geom);
CREATE UNIQUE INDEX amazon_srtm_unique_index
  ON public.amazon_srtm (ogc_fid);
CREATE INDEX amazon_srtm_states_index
  ON public.amazon_srtm (states_id);
