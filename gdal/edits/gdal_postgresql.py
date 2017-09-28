# http://initd.org/psycopg/docs/usage.html
import psycopg2

# Connect to an existing database
conn = psycopg2.connect(dbname="eba", port="5432", user="postgres", password="postgres", host="localhost")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command
cur.execute("select * from metrics limit 100;")
result = cur.fetchall()

print(result)