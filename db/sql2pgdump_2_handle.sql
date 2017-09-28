BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 1 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 2 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 3 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 4 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 5 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 6 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 7 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 8 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 9 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 10 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 11 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 12 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 13 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 14 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 15 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 16 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 17 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 18 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 19 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 20 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 21 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 22 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 23 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 24 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 25 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 26 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 27 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 28 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 29 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET mosaic_id = ms.gid
FROM mosaic ms
WHERE ms.gid = 30 AND st_intersects(amazon.geom, ms.geom);
COMMIT;

BEGIN;
ALTER TABLE amazon ADD CONSTRAINT amazon_mosaic_fkey FOREIGN KEY (mosaic_id) REFERENCES mosaic (gid);
CREATE INDEX amazon_mosaic_index ON amazon (mosaic_id);
COMMIT;
