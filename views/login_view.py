# views/login_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        #self.username_input.setText('admin@mail.ru')
        self.username_input.setPlaceholderText('Email')
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        #self.password_input.setText('12345')
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login', self)
        layout.addWidget(self.login_button)

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)

        self.forgot_password_button = QPushButton('Forgot Password?', self)
        layout.addWidget(self.forgot_password_button)

        self.message_label = QLabel('', self)
        layout.addWidget(self.message_label)

        self.setLayout(layout)
        self.setWindowTitle('Login')
