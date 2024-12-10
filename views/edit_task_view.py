from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel, QDateTimeEdit
from PyQt5.QtCore import QDateTime

from repositories.db.enums import TaskStatus


class EditTaskView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Title", self)
        self.title_input = QLineEdit(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)

        self.description_label = QLabel("Description", self)
        self.description_input = QLineEdit(self)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)

        self.status_label = QLabel("Status", self)
        self.status_input = QComboBox(self)
        self.status_input.addItems([e for e in TaskStatus])
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)

        self.assigned_user_label = QLabel("Assigned User", self)
        self.assigned_user_input = QComboBox(self)
        layout.addWidget(self.assigned_user_label)
        layout.addWidget(self.assigned_user_input)

        self.deadline_label = QLabel("Deadline", self)
        self.deadline_input = QDateTimeEdit(self)
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.deadline_label)
        layout.addWidget(self.deadline_input)

        self.message_label = QLabel('', self)
        layout.addWidget(self.message_label)

        self.save_button = QPushButton("Save", self)
        layout.addWidget(self.save_button)

        self.delete_button = QPushButton("Delete Task", self)  # Новая кнопка
        layout.addWidget(self.delete_button)

        self.back_button = QPushButton("Back", self)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.setWindowTitle("Edit Task")
