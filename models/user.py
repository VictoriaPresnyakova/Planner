from repositories.db.enums import UserRole, UserNotification


class User:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<User(email={self.email})>'
