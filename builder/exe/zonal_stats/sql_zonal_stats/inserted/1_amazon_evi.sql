-- DROP SEQUENCE public.amazon_evi_seq;
CREATE SEQUENCE public.amazon_evi_seq
INCREMENT 1
MINVALUE 1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER TABLE public.amazon_evi_seq
  OWNER TO eba;

-- Table: public.amazon_evi

-- DROP TABLE public.amazon_evi;
CREATE TABLE public.amazon_evi
(
  fid        INTEGER NOT NULL DEFAULT nextval('amazon_evi_seq' :: REGCLASS),
  "row"      INTEGER,
  col        INTEGER,
  states_id  INTEGER,
  mosaic_id  INTEGER,
  processed  BOOLEAN          DEFAULT FALSE,
  evi_max    DOUBLE PRECISION,
  evi_mean   DOUBLE PRECISION,
  evi_median DOUBLE PRECISION,
  evi_min    DOUBLE PRECISION,
  evi_q1     DOUBLE PRECISION,
  evi_q3     DOUBLE PRECISION,
  evi_sd     DOUBLE PRECISION,
  geom       GEOMETRY(Polygon, 5880),
  CONSTRAINT amazon_evi_pkey PRIMARY KEY (fid),
  CONSTRAINT amazon_evi_fkey FOREIGN KEY (states_id)
  REFERENCES public.states (gid) MATCH SIMPLE
  ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT amazon_evi_mosaic_fkey FOREIGN KEY (mosaic_id)
  REFERENCES public.mosaic (gid) MATCH SIMPLE
  ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
OIDS = FALSE
);
ALTER TABLE public.amazon_evi
  OWNER TO eba;
