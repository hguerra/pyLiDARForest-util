BEGIN;
UPDATE amazon
SET states_id = st.gid
FROM states st
WHERE st.gid = 4 AND st_intersects(amazon.geom, st.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET states_id = st.gid
FROM states st
WHERE st.gid = 9 AND st_intersects(amazon.geom, st.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET states_id = st.gid
FROM states st
WHERE st.gid = 7 AND st_intersects(amazon.geom, st.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET states_id = st.gid
FROM states st
WHERE st.gid = 1 AND st_intersects(amazon.geom, st.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET states_id = st.gid
FROM states st
WHERE st.gid = 2 AND st_intersects(amazon.geom, st.geom);

COMMIT;
BEGIN;
UPDATE amazon
SET states_id = st.gid
FROM states st
WHERE st.gid = 3 AND st_intersects(amazon.geom, st.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET states_id = st.gid
FROM states st
WHERE st.gid = 5 AND st_intersects(amazon.geom, st.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET states_id = st.gid
FROM states st
WHERE st.gid = 6 AND st_intersects(amazon.geom, st.geom);
COMMIT;

BEGIN;
UPDATE amazon
SET states_id = st.gid
FROM states st
WHERE st.gid = 8 AND st_intersects(amazon.geom, st.geom);
COMMIT;
