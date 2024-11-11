from misc.config import *
import psycopg2


def connect():
    connection = psycopg2.connect(dbname=SQL_DATABASE, user=SQL_USER,
                                  password=SQL_PASSWORD, host=SQL_HOST, port=SQL_PORT)
    connection.cursor().execute("SET TIME ZONE 'UTC';")
    return connection