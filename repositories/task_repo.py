from repositories.abc.task_repo_abc import TaskRepoABC
from repositories.db.common import insert_new_record, change_record_by_id, delete_record_by_id
from repositories.db.connect import connect
from contextlib import closing
from psycopg2.extras import NamedTupleCursor


class TaskRepo(TaskRepoABC):

    def get_all_tasks(self, limit, offset):
        try:
            res = []
            with closing(connect()) as conn:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    cursor.execute('SELECT * FROM {} LIMIT %s offset %s'.format('public.task'), (limit, offset))
                    for row in cursor:
                        res.append({x: getattr(row, x) for x in row._fields})
                    return res
        except Exception as e:
            return {}

    def get_tasks_by_user_id(self, user_id, limit, offset):
        try:
            res = []
            with closing(connect()) as conn:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    cursor.execute('SELECT * FROM {} WHERE user_id = %s OR assigned_user_id = %s LIMIT %s offset %s'.format('public.task'), (user_id, user_id, limit, offset))
                    for row in cursor:
                        res.append({x: getattr(row, x) for x in row._fields})
                    return res
        except Exception as e:
            return {}

    def get_tasks_by_filter(self, filter_query: str, limit, offset):
        try:
            res = []
            with closing(connect()) as conn:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    cursor.execute(
                        'SELECT * FROM {} WHERE {} LIMIT %s offset %s'.format(
                            'public.task', filter_query), (limit, offset))
                    for row in cursor:
                        res.append({x: getattr(row, x) for x in row._fields})
                    return res
        except Exception as e:
            return {}

    def create_task(self, kwargs):
        return insert_new_record('public.task', kwargs)

    def find_task_by_id(self, id: int):
        try:
            with closing(connect()) as conn:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    cursor.execute('SELECT * FROM {} where id = %s'.format('public.task'), (id,))
                    res = cursor.fetchone()
                    return {x: getattr(res, x) for x in res._fields}
        except Exception as e:
            return {}

    def update_task_by_id(self, id: int, kwargs):
        return change_record_by_id('public.task', id, kwargs)

    def delete_task_by_id(self, id: int):
        return delete_record_by_id('public.task', id)
