-----------------------------------------------------------------------------------------------------------------
-- Create Function

DROP FUNCTION public.fselect_scientific_name(
IN common VARCHAR,
OUT family_id INTEGER,
OUT genus INTEGER,
OUT species INTEGER
);

CREATE OR REPLACE FUNCTION fselect_scientific_name(
  IN  common     VARCHAR,
  OUT family_id  INTEGER,
  OUT genus_id   INTEGER,
  OUT species_id INTEGER
) AS $$
BEGIN
  IF exists(SELECT 1
            FROM common_name
            WHERE common_name.name = common AND common_name.species_id IS NOT NULL)
  THEN
    SELECT
      common_name.family_id,
      common_name.genus_id,
      common_name.species_id
    INTO
      family_id, genus_id, species_id
    FROM
      common_name
    WHERE
      common_name.name = common
    GROUP BY
      common_name.family_id, common_name.genus_id, common_name.species_id
    ORDER BY count(common_name.species_id) DESC
    LIMIT 1;
  ELSEIF exists(SELECT 1
                FROM common_name
                WHERE common_name.name = common AND common_name.genus_id IS NOT NULL)
    THEN
      SELECT
        common_name.family_id,
        common_name.genus_id,
        common_name.species_id
      INTO
        family_id, genus_id, species_id
      FROM
        common_name
      WHERE
        common_name.name = common
      GROUP BY
        common_name.family_id, common_name.genus_id, common_name.species_id
      ORDER BY count(common_name.genus_id) DESC
      LIMIT 1;
  ELSE
    SELECT
      common_name.family_id,
      common_name.genus_id,
      common_name.species_id
    INTO
      family_id, genus_id, species_id
    FROM
      common_name
    WHERE
      common_name.name = common
    GROUP BY
      common_name.family_id, common_name.genus_id, common_name.species_id
    ORDER BY count(common_name.family_id) DESC
    LIMIT 1;
  END IF;
END; $$
LANGUAGE plpgsql;

SELECT *
FROM fselect_scientific_name('tapereba');
SELECT *
FROM fselect_scientific_name('molongo');
SELECT *
FROM fselect_scientific_name('faveira');
SELECT *
FROM fselect_scientific_name('null');

-----------------------------------------------------------------------------------------------------------------
-- Create Function

DROP FUNCTION public.fget_wood_density(
IN family_name VARCHAR,
IN genus_name VARCHAR,
IN species_name VARCHAR,
OUT meanwd DOUBLE PRECISION,
OUT sdwd DOUBLE PRECISION,
OUT levelwd VARCHAR
);

CREATE OR REPLACE FUNCTION fget_wood_density(
  IN  family_name  VARCHAR,
  IN  genus_name   VARCHAR,
  IN  species_name VARCHAR,
  OUT meanwd       DOUBLE PRECISION,
  OUT sdwd         DOUBLE PRECISION,
  OUT levelwd      VARCHAR
) AS $$
BEGIN
  IF exists(SELECT 1
            FROM species AS sp
            WHERE sp.name = species_name AND exists(SELECT 1
                                                    FROM taxonomy AS taxo
                                                    WHERE taxo.species_id = sp.id AND taxo.region IN
                                                                                      ('south america (tropical)', 'south america (extratropical)', 'central america (tropical)')))

  THEN
    SELECT
      AVG(taxo.density),
      0.07082326,
      'species'
    INTO meanwd, sdwd, levelwd
    FROM taxonomy AS taxo, (SELECT s.id AS species_id
                            FROM species AS s
                            WHERE s.name = species_name) AS sp
    WHERE taxo.species_id = sp.species_id AND
          taxo.region IN ('south america (tropical)', 'south america (extratropical)', 'central america (tropical)');
  ELSEIF exists(SELECT 1
                FROM genus AS gn
                WHERE gn.name = genus_name AND exists(SELECT 1
                                                      FROM taxonomy AS taxo
                                                      WHERE taxo.genus_id = gn.id AND taxo.region IN
                                                                                      ('south america (tropical)', 'south america (extratropical)', 'central america (tropical)')))
    THEN
      SELECT
        AVG(taxo.density),
        0.09413391,
        'genus'
      INTO meanwd, sdwd, levelwd
      FROM taxonomy AS taxo, (SELECT g.id AS genus_id
                              FROM genus AS g
                              WHERE g.name = genus_name) AS gen
      WHERE taxo.genus_id = gen.genus_id AND
            taxo.region IN ('south america (tropical)', 'south america (extratropical)', 'central america (tropical)');
  ELSEIF exists(SELECT 1
                FROM family AS fm
                WHERE fm.name = family_name AND exists(SELECT 1
                                                       FROM taxonomy AS taxo
                                                       WHERE taxo.family_id = fm.id AND taxo.region IN
                                                                                        ('south america (tropical)', 'south america (extratropical)', 'central america (tropical)')))
    THEN
      SELECT
        AVG(taxo.density),
        0.12340172,
        'family'
      INTO meanwd, sdwd, levelwd
      FROM taxonomy AS taxo, (SELECT f.id AS family_id
                              FROM family AS f
                              WHERE f.name = family_name) AS fam
      WHERE taxo.family_id = fam.family_id AND
            taxo.region IN ('south america (tropical)', 'south america (extratropical)', 'central america (tropical)');
  END IF;
END; $$
LANGUAGE plpgsql;

SELECT *
FROM fget_wood_density(NULL, NULL, 'eucalyptus melanoxylon');

SELECT *
FROM fget_wood_density(NULL, 'monotes', NULL);

SELECT *
FROM fget_wood_density('peridiscaceae', NULL, NULL);

-----------------------------------------------------------------------------------------------------------------
-- Create Function

DROP FUNCTION public.fget_plot_wood_density(
IN plot_name VARCHAR,
OUT meanwd DOUBLE PRECISION,
OUT levelwd VARCHAR
);

CREATE OR REPLACE FUNCTION fget_plot_wood_density(
  IN  plot_name VARCHAR,
  OUT meanwd    DOUBLE PRECISION,
  OUT levelwd   VARCHAR
) AS $$
BEGIN
  SELECT
    AVG(meas.density),
    'dataset'
  INTO
    meanwd,
    levelwd
  FROM measurements AS meas
  WHERE meas.plot = plot_name;
END; $$
LANGUAGE plpgsql;


SELECT *
FROM fget_plot_wood_density('jarau_p06');
-----------------------------------------------------------------------------------------------------------------
-- Create Function

-- DROP FUNCTION public.fupdate_measurements_density();
CREATE OR REPLACE FUNCTION public.fupdate_measurements_density()
  RETURNS TRIGGER AS $$
DECLARE
  family_name  VARCHAR;
  genus_name   VARCHAR;
  species_name VARCHAR;
  res_meanwd   DOUBLE PRECISION;
  res_sdwd     DOUBLE PRECISION;
  res_levelwd  VARCHAR;
BEGIN

  SELECT fam.name
  INTO family_name
  FROM family AS fam
  WHERE fam.id = NEW.family_id;
  SELECT gen.name
  INTO genus_name
  FROM genus AS gen
  WHERE gen.id = NEW.genus_id;
  SELECT sp.name
  INTO species_name
  FROM species AS sp
  WHERE sp.id = NEW.species_id;

  IF family_name IS NULL AND genus_name IS NULL AND species_name IS NULL AND NEW.common_name_id IS NOT NULL
  THEN
    SELECT fam.name
    INTO family_name
    FROM common_name AS common, family AS fam
    WHERE common.id = NEW.common_name_id AND common.family_id = fam.id;
    SELECT gen.name
    INTO genus_name
    FROM common_name AS common, genus AS gen
    WHERE common.id = NEW.common_name_id AND common.genus_id = gen.id;
    SELECT sp.name
    INTO species_name
    FROM common_name AS common, species AS sp
    WHERE common.id = NEW.common_name_id AND common.species_id = sp.id;
  END IF;

  SELECT
    meanwd,
    sdwd,
    levelwd
  INTO res_meanwd, res_sdwd, res_levelwd
  FROM fget_wood_density(family_name, genus_name, species_name);

  IF res_meanwd IS NULL
  THEN
    SELECT
      meanwd,
      NULL,
      levelwd
    INTO res_meanwd, res_sdwd, res_levelwd
    FROM fget_plot_wood_density(NEW.plot);
  END IF;

  NEW.density:=res_meanwd;
  NEW.density_sd:=res_sdwd;
  UPDATE information
  SET density = res_levelwd
  WHERE id = NEW.information_id;
  RETURN NEW;
END; $$
LANGUAGE plpgsql;

-- Create Trigger

-- DROP TRIGGER measurements_update_density ON public.measurements;
CREATE TRIGGER measurements_update_density
BEFORE INSERT OR UPDATE
  ON public.measurements
FOR EACH ROW
EXECUTE PROCEDURE public.fupdate_measurements_density();

-----------------------------------------------------------------------------------------------------------------
-- Create Function

-- DROP FUNCTION public.fheight_estimate();
CREATE OR REPLACE FUNCTION public.fheight_estimate()
  RETURNS TRIGGER AS
$BODY$
DECLARE
  var_height VARCHAR;
BEGIN
  IF NEW.dap IS NULL
  THEN
    NEW.height:= NULL;
    var_height:= NULL;
  ELSEIF NEW.height IS NOT NULL
    THEN
      var_height:='MEASURED';
  ELSE
    NEW.height:=48.131 * (1 - exp((-0.0375) * (NEW.dap ^ 0.8228)));
    var_height:='ESTIMATED';
  END IF;

  UPDATE public.information
  SET height = var_height
  WHERE id = new.information_id;

  RETURN NEW;
END$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;
ALTER FUNCTION public.fheight_estimate()
OWNER TO postgres;

-- Create Trigger

-- DROP TRIGGER measurements_height_estimate ON public.measurements;
CREATE TRIGGER measurements_height_estimate
BEFORE INSERT OR UPDATE
  ON public.measurements
FOR EACH ROW
EXECUTE PROCEDURE public.fheight_estimate();