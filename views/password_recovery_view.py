from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class PasswordRecoveryView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Enter your email')
        self.layout.addWidget(self.email_input)

        self.send_code_button = QPushButton('Send Recovery Code')
        self.layout.addWidget(self.send_code_button)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText('Enter the code sent to your email')
        self.layout.addWidget(self.code_input)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText('Enter your new password')
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.new_password_input)

        self.recover_button = QPushButton('Recover Password')
        self.layout.addWidget(self.recover_button)

        self.message_label = QLabel()
        self.layout.addWidget(self.message_label)

        self.back_button = QPushButton('Back to Login')
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)
