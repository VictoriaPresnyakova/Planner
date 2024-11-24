

class User:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name} {self.surname})>"
