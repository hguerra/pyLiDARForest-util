CREATE SEQUENCE public.family_id_seq
INCREMENT 1
START 1
MINVALUE 1
MAXVALUE 9223372036854775807
CACHE 1;

CREATE SEQUENCE public.genus_id_seq
INCREMENT 1
START 1
MINVALUE 1
MAXVALUE 9223372036854775807
CACHE 1;

CREATE SEQUENCE public.species_id_seq
INCREMENT 1
START 1
MINVALUE 1
MAXVALUE 9223372036854775807
CACHE 1;

CREATE SEQUENCE public.taxonomy_id_seq
INCREMENT 1
START 1
MINVALUE 1
MAXVALUE 9223372036854775807
CACHE 1;

CREATE SEQUENCE public.common_name_id_seq
INCREMENT 1
START 1
MINVALUE 1
MAXVALUE 9223372036854775807
CACHE 1;

CREATE SEQUENCE public.measurements_id_seq
INCREMENT 1
START 1
MINVALUE 1
MAXVALUE 9223372036854775807
CACHE 1;

CREATE SEQUENCE public.information_id_seq
INCREMENT 1
START 1
MINVALUE 1
MAXVALUE 9223372036854775807
CACHE 1;

CREATE SEQUENCE public.geo_reference_id_seq
INCREMENT 1
START 1
MINVALUE 1
MAXVALUE 9223372036854775807
CACHE 1;

CREATE SEQUENCE public.owner_id_seq
INCREMENT 1
START 1
MINVALUE 1
MAXVALUE 9223372036854775807
CACHE 1;


CREATE TABLE public.family (
  id   INTEGER NOT NULL DEFAULT nextval('family_id_seq' :: REGCLASS),
  name VARCHAR NOT NULL,
  PRIMARY KEY (id)
);


CREATE TABLE public.genus (
  id   INTEGER NOT NULL DEFAULT nextval('genus_id_seq' :: REGCLASS),
  name VARCHAR NOT NULL,
  PRIMARY KEY (id)
);


CREATE TABLE public.species (
  id   INTEGER NOT NULL DEFAULT nextval('species_id_seq' :: REGCLASS),
  name VARCHAR NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE public.taxonomy (
  id                INTEGER          NOT NULL DEFAULT nextval('taxonomy_id_seq' :: REGCLASS),
  family_id         INTEGER          NOT NULL,
  genus_id          INTEGER          NOT NULL,
  species_id        INTEGER          NOT NULL,
  density           DOUBLE PRECISION NOT NULL,
  region            VARCHAR,
  article_reference INTEGER,
  PRIMARY KEY (id)
);

CREATE INDEX ON public.taxonomy
(family_id);
CREATE INDEX ON public.taxonomy
(genus_id);
CREATE INDEX ON public.taxonomy
(species_id);


CREATE TABLE public.common_name (
  id         INTEGER NOT NULL DEFAULT nextval('common_name_id_seq' :: REGCLASS),
  family_id  INTEGER,
  genus_id   INTEGER,
  species_id INTEGER,
  name       VARCHAR NOT NULL,
  PRIMARY KEY (id)
);

CREATE INDEX ON public.common_name
(family_id);
CREATE INDEX ON public.common_name
(genus_id);
CREATE INDEX ON public.common_name
(species_id);


CREATE TABLE public.measurements (
  id               INTEGER          NOT NULL DEFAULT nextval('measurements_id_seq' :: REGCLASS),
  owner_id         INTEGER          NOT NULL,
  information_id   INTEGER          NOT NULL,
  geo_reference_id INTEGER,
  taxonomy_id      INTEGER,
  common_name_id   INTEGER,
  tree_id          INTEGER,
  plot             VARCHAR          NOT NULL,
  year             SMALLINT         NOT NULL,
  dap              DOUBLE PRECISION NOT NULL,
  height           REAL             NOT NULL,
  density          DOUBLE PRECISION,
  PRIMARY KEY (id)
);

CREATE INDEX ON public.measurements
(owner_id);
CREATE INDEX ON public.measurements
(geo_reference_id);
CREATE INDEX ON public.measurements
(information_id);
CREATE INDEX ON public.measurements
(taxonomy_id);
CREATE INDEX ON public.measurements
(common_name_id);

CREATE TABLE public.information (
  id     INTEGER NOT NULL DEFAULT nextval('information_id_seq' :: REGCLASS),
  plot   VARCHAR,
  height VARCHAR,
  dead   BOOLEAN,
  type   VARCHAR,
  PRIMARY KEY (id)
);

CREATE TABLE public.owner (
  id   INTEGER NOT NULL DEFAULT nextval('owner_id_seq' :: REGCLASS),
  name VARCHAR NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE public.geo_reference (
  id      INTEGER NOT NULL DEFAULT nextval('geo_reference_id_seq' :: REGCLASS),
  x       DOUBLE PRECISION,
  y       DOUBLE PRECISION,
  az      DOUBLE PRECISION,
  azimuth FLOAT,
  geom    GEOMETRY(Point, 5880),
  PRIMARY KEY (id)
);

ALTER TABLE public.taxonomy
  ADD CONSTRAINT FK_taxonomy__family_id FOREIGN KEY (family_id) REFERENCES public.family (id);
ALTER TABLE public.taxonomy
  ADD CONSTRAINT FK_taxonomy__genus_id FOREIGN KEY (genus_id) REFERENCES public.genus (id);
ALTER TABLE public.taxonomy
  ADD CONSTRAINT FK_taxonomy__species_id FOREIGN KEY (species_id) REFERENCES public.species (id);

ALTER TABLE public.common_name
  ADD CONSTRAINT FK_common_name__family_id FOREIGN KEY (family_id) REFERENCES public.family (id);
ALTER TABLE public.common_name
  ADD CONSTRAINT FK_common_name__genus_id FOREIGN KEY (genus_id) REFERENCES public.genus (id);
ALTER TABLE public.common_name
  ADD CONSTRAINT FK_common_name__species_id FOREIGN KEY (species_id) REFERENCES public.species (id);

ALTER TABLE public.measurements
  ADD CONSTRAINT FK_measurements__taxonomy_id FOREIGN KEY (taxonomy_id) REFERENCES public.taxonomy (id);
ALTER TABLE public.measurements
  ADD CONSTRAINT FK_measurements__common_name_id FOREIGN KEY (common_name_id) REFERENCES public.common_name (id);
ALTER TABLE public.measurements
  ADD CONSTRAINT FK_measurements__owner_id FOREIGN KEY (owner_id) REFERENCES public.owner (id);
ALTER TABLE public.measurements
  ADD CONSTRAINT FK_measurements__information_id FOREIGN KEY (information_id) REFERENCES public.information (id);
ALTER TABLE public.measurements
  ADD CONSTRAINT FK_measurements__geo_reference_id FOREIGN KEY (geo_reference_id) REFERENCES public.geo_reference (id);