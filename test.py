import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

con = psycopg2.connect(
      user='postgres', host=  '127.0.0.1',
      password='postgres')

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

cur = con.cursor()

# Use the psycopg2.sql module instead of string concatenation
# in order to avoid sql injection attacks.
cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier("symperaDB"))
    )
