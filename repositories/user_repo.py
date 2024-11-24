from repositories.abc.user_repo_abc import UserRepoABC
from repositories.db.common import insert_new_record, change_record_by_id, delete_record_by_id
from repositories.db.connect import connect
from contextlib import closing
from psycopg2.extras import NamedTupleCursor


class UserRepo(UserRepoABC):

    def get_all_users(self, limit, offset):
        try:
            res = []
            with closing(connect()) as conn:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    cursor.execute('SELECT * FROM {} LIMIT %s offset %s'.format('public.user'), (limit, offset))
                    for row in cursor:
                        res.append({x: getattr(row, x) for x in row._fields})
                    return res
        except Exception as e:
            return {}

    def get_user_by_email(self, email: str):
        try:
            with closing(connect()) as conn:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    cursor.execute('SELECT * FROM {} where email = %s'.format('public.user'), (email,))
                    res = cursor.fetchone()
                    return {x: getattr(res, x) for x in res._fields}
        except Exception as e:
            return {}

    def create_user(self, kwargs):
        return insert_new_record('public.user', kwargs)

    def find_user_by_id(self, id: int):
        try:
            with closing(connect()) as conn:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    cursor.execute('SELECT * FROM {} where id = %s'.format('public.user'), (id,))
                    res = cursor.fetchone()
                    return {x: getattr(res, x) for x in res._fields}
        except Exception as e:
            return {}

    def update_user_by_id(self, id: int, kwargs):
        return change_record_by_id('public.user', id, kwargs)

    def delete_user_by_id(self, id: int):
        return delete_record_by_id('public.user', id)
