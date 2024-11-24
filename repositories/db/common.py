import traceback

from repositories.db.connect import connect
from contextlib import closing
from psycopg2.extras import NamedTupleCursor


def get_record_by_id(table_name, record_id):
    try:
        with closing(connect()) as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute('SELECT * FROM {} where id = %s'.format(table_name), (record_id,))
                res = cursor.fetchone()
                return {x: getattr(res, x) for x in res._fields}
    except Exception as e:
        return {}


def change_record_by_id(table_name, record_id, new_values):
    try:
        with closing(connect()) as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute("UPDATE {} set ({}) = row%s where id={} RETURNING *".format(table_name, ', '.join(new_values.keys()), record_id), (tuple(new_values.values()),))
                res = cursor.fetchone()
            conn.commit()
        return {x: getattr(res, x) for x in res._fields}
    except Exception as e:
        return False


def delete_record_by_id(table_name, record_id):
    try:
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM {} where id={}".format(table_name, record_id))
            conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        return False


def insert_new_record(table_name, values):
    try:
        with closing(connect()) as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute("INSERT INTO {} ({}) VALUES%s RETURNING *".format(table_name, ', '.join(values.keys())), (tuple(values.values()),))
                res = cursor.fetchone()
            conn.commit()
        return {x: getattr(res, x) for x in res._fields}
    except Exception as e:
        traceback.print_exc()
        return False
