DROP SEQUENCE public.roraima_seq;
CREATE SEQUENCE public.roraima_seq
INCREMENT 1
MINVALUE 1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER TABLE public.roraima_seq
  OWNER TO postgres;

DROP TABLE roraima;
CREATE TABLE roraima (
  id   INTEGER NOT NULL DEFAULT nextval('roraima_seq' :: REGCLASS),
  states_id INTEGER,
  row  INTEGER,
  col  INTEGER,
  processed BOOLEAN DEFAULT FALSE,
  geom GEOMETRY(Polygon, 5880),
  CONSTRAINT roraima_pkey PRIMARY KEY (id),
  CONSTRAINT roraima_fkey FOREIGN KEY (states_id) REFERENCES states (gid)
)
WITH (
OIDS = FALSE
);
ALTER TABLE public.roraima
  OWNER TO eba;

CREATE UNIQUE INDEX roraima_unique_index
  ON public.roraima (id);
CREATE INDEX roraima_gix
  ON public.roraima USING GIST (geom);

INSERT INTO roraima (states_id, row, col, geom)
  SELECT
    8,
    cells.row,
    cells.col,
    st_setsrid(cells.geom, 5880) AS geom
  FROM ST_CreateFishnet(9629, 13775, 248.817651102, 248.817651102, 2794214.56743, 8190752.29719) AS cells;

VACUUM ANALYZE roraima;
CLUSTER roraima USING roraima_gix;
ANALYZE roraima;

DELETE FROM roraima polys
USING states bb
WHERE bb.gid = 8 AND NOT ST_Intersects(polys.geom, bb.geom);

ALTER TABLE roraima ADD COLUMN states_id INTEGER;
ALTER TABLE roraima ADD CONSTRAINT roraima_fkey FOREIGN KEY (states_id) REFERENCES states (gid);
UPDATE roraima SET states_id = 8;