from enum import IntEnum, Enum


class TaskStatus(str, Enum):
    NEW = "New"
    IN_PROCESS = "In process"
    DONE = "Done"