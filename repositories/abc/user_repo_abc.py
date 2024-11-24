from abc import ABC, abstractmethod


class UserRepoABC(ABC):

    @abstractmethod
    def get_all_users(self, limit, offset):
        pass

    @abstractmethod
    def get_user_by_email(self, emal: str):
        pass

    @abstractmethod
    def create_user(self, kwargs):
        pass

    @abstractmethod
    def find_user_by_id(self, id: int):
        pass

    @abstractmethod
    def update_user_by_id(self, id: int, kwargs):
        pass

    @abstractmethod
    def delete_user_by_id(self, id: int):
        pass
