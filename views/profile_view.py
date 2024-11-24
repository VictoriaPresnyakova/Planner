from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox


class ProfileView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.email_label = QLabel('Email', self)
        self.email_input = QLineEdit(self)
        self.email_input.setReadOnly(True)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.name_label = QLabel('Name', self)
        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_label)

        self.surname_label = QLabel('Surname', self)
        self.surname_input = QLineEdit(self)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_label)

        self.save_button = QPushButton('Save', self)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)

        self.message_label = QLabel('', self)
        layout.addWidget(self.message_label)

        self.setLayout(layout)
        self.setWindowTitle('Profile')
