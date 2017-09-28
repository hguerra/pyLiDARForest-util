import os
import subprocess
import tempfile


def execute(command, verbose=False):
    print("Running '{}'".format(command))
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = p.communicate()
    if ((out is not None) and ("ERROR" in out)) or ((err is not None) and ("ERROR" in err)):
        print("Error in command: {0} Message: {1}{2}".format(command, out, err))
        raise
    if verbose > 0:
        print(out)
    return out, err


def bat(command, suffix=".bat", directory="."):
    with tempfile.NamedTemporaryFile(suffix=suffix, dir=directory, delete=False) as tmp_file:
        tmp_name = tmp_file.name
        tmp_file.write(command)
        tmp_file.close()

        stdout, stderr = execute(tmp_name)
        os.remove(tmp_name)
        return stdout, stderr


if __name__ == '__main__':
    # stdout, stderr = execute(r"E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\builder\measure_time.cmd")
    # print(stdout)
    # print(stderr)
    # print(bat("echo %time%"))

    table = "amazon_roraima"
    intersects = "states"
    intersects_fid_col = "gid"
    intersects_fid_value = "8"
    psqlbin = r"C:\Program Files\PostgreSQL\9.6\bin\psql.exe"
    user = "eba"
    password = "ebaeba18"
    dbname = "amazon"

    sql = ("VACUUM ANALYZE {0};".format(table),
           "CLUSTER {0} USING {0}_wkb_geometry_geom_idx;".format(table),
           "ANALYZE {0};".format(table),
           "DELETE FROM {0} polys USING {1} bb WHERE bb.{2} = {3} AND "
           "NOT ST_Intersects(polys.wkb_geometry, bb.geom);"
           .format(table, intersects, intersects_fid_col, intersects_fid_value))

    sql = ("SELECT COUNT(*) FROM states;",)

    cmd = 'SET PGPASSWORD={}\n"{}" -U {} -d {} -c "{}"'.format(password, psqlbin, user, dbname, "".join(sql))
    print(bat(cmd))
