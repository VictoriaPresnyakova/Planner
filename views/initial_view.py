from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class InitialView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.login_button = QPushButton('Login', self)
        layout.addWidget(self.login_button)

        self.signup_button = QPushButton('Sign Up', self)
        layout.addWidget(self.signup_button)

        self.setLayout(layout)
        self.setWindowTitle('Welcome')
