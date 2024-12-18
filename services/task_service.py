from copy import deepcopy

from misc.utils import clear_rest_input_parameters
from models.task import Task
import random
import string

from repositories.task_repo import TaskRepo


class TaskService:
    def __init__(self):
        self.repository = TaskRepo()

    def get_all_tasks(self, limit=500, offset=0):
        task_list = self.repository.get_all_tasks(limit, offset)
        result = []
        for task in task_list:
            try:
                result.append(Task(**task))
            except Exception as e:
                print(e)
        return result

    def get_tasks_by_user_id(self, user_id: int, limit=500, offset=0):
        task_list = self.repository.get_tasks_by_user_id(user_id, limit, offset)
        result = []
        for task in task_list:
            try:
                result.append(Task(**task))
            except Exception as e:
                print(e)
        return result

    def get_tasks_by_assigned_user_id(self, user_id, limit=500, offset=0):
        task_list = self.repository.get_tasks_by_filter(f'assigned_user_id = {user_id}', limit, offset)
        result = []
        for task in task_list:
            try:
                result.append(Task(**task))
            except Exception as e:
                print(e)
        return result

    def get_tasks_created_by_user_id(self, user_id, limit=500, offset=0):
        task_list = self.repository.get_tasks_by_filter(f'user_id = {user_id}', limit, offset)
        result = []
        for task in task_list:
            try:
                result.append(Task(**task))
            except Exception as e:
                print(e)
        return result

    def create_task(self, kwargs):
        task = self.repository.create_task(clear_rest_input_parameters(kwargs))
        if task:
            return Task(**task)
        return False

    def find_task_by_id(self, id: int):
        task = self.repository.find_task_by_id(id)
        if task:
            return Task(**task)
        return None

    def update_task(self, task: Task):
        kwargs = deepcopy(task.__dict__)
        id = kwargs.pop('id', -1)
        task = self.repository.update_task_by_id(id, clear_rest_input_parameters(kwargs))
        if task:
            return Task(**task)
        return False

    def delete_task_by_id(self, id: int):
        return self.repository.delete_task_by_id(id)
