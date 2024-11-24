from repositories.db.enums import TaskStatus


class Task:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'status':
                value = TaskStatus(value)
            setattr(self, key, value)

    def __repr__(self):
        return f'<Task(id={self.id})>'
