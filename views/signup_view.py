# views/signup_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox

class SignUpView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Email')
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)


        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Name')
        layout.addWidget(self.name_input)

        self.surname_input = QLineEdit(self)
        self.surname_input.setPlaceholderText('Surname')
        layout.addWidget(self.surname_input)

        self.signup_button = QPushButton('Sign Up', self)
        layout.addWidget(self.signup_button)

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)

        self.message_label = QLabel('', self)
        layout.addWidget(self.message_label)

        self.setLayout(layout)
        self.setWindowTitle('Sign Up')
