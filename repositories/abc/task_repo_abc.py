from abc import ABC, abstractmethod


class TaskRepoABC(ABC):

    @abstractmethod
    def get_all_tasks(self, limit, offset):
        pass

    @abstractmethod
    def create_task(self, kwargs):
        pass

    @abstractmethod
    def find_task_by_id(self, id: int):
        pass

    @abstractmethod
    def update_task_by_id(self, id: int, kwargs):
        pass

    @abstractmethod
    def delete_task_by_id(self, id: int):
        pass
