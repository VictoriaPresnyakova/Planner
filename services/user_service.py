from copy import deepcopy

from misc.utils import clear_rest_input_parameters
from models.user import User
from repositories.user_repo import UserRepo
import random
import string


class UserService:
    def __init__(self):
        self.repository = UserRepo()

    def get_all_users(self, limit=500, offset=0):
        user_list = self.repository.get_all_users(limit, offset)
        result = []
        for user in user_list:
            try:
                result.append(User(**user))
            except Exception as e:
                print(e)
        return result

    def get_user_by_email(self, emal: str):
        user = self.repository.get_user_by_email(emal)
        if user:
            return User(**user)
        return None

    def create_user(self, kwargs):
        user = self.repository.create_user(clear_rest_input_parameters(kwargs))
        if user:
            return User(**user)
        return False

    def find_user_by_id(self, id: int):
        user = self.repository.find_user_by_id(id)
        if user:
            return User(**user)
        return None

    def update_user(self, user: User):
        kwargs = deepcopy(user.__dict__)
        id = kwargs.pop('id', -1)
        user = self.repository.update_user_by_id(id, clear_rest_input_parameters(kwargs))
        if user:
            return User(**user)
        return False

    def delete_user_by_id(self, id: int):
        return self.repository.delete_user_by_id(id)

    def generate_token(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
