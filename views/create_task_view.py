# views/create_task_view.py
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QDateEdit, QDateTimeEdit, \
    QHBoxLayout, QCheckBox


class CreateTaskView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel('Title', self)
        self.title_input = QLineEdit(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)

        self.description_label = QLabel('Description', self)
        self.description_input = QLineEdit(self)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)

        self.assigned_user_id_label = QLabel('User', self)
        self.assigned_user_id_input = QComboBox(self)
        layout.addWidget(self.assigned_user_id_label)
        layout.addWidget(self.assigned_user_id_input)

        self.deadline_label = QLabel('Deadline', self)
        self.deadline_input = QDateTimeEdit(self)
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDateTime(QDateTime.currentDateTime())
        self.deadline_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        layout.addWidget(self.deadline_label)
        layout.addWidget(self.deadline_input)

        self.hide_deadline_checkbox = QCheckBox("No Deadline", self)
        layout.addWidget(self.hide_deadline_checkbox)

        layout.addWidget(self.deadline_label)
        layout.addWidget(self.deadline_input)

        self.save_button = QPushButton('Save', self)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)

        self.message_label = QLabel('', self)
        layout.addWidget(self.message_label)

        self.setLayout(layout)
        self.setWindowTitle('Profile')
