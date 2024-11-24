from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel


class SignUpAuthView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.token_input = QLineEdit(self)
        self.token_input.setPlaceholderText('Enter authentication token')
        layout.addWidget(self.token_input)

        self.verify_button = QPushButton('Verify', self)
        layout.addWidget(self.verify_button)

        self.resend_token_button = QPushButton('Resend Token', self)
        layout.addWidget(self.resend_token_button)

        self.back_button = QPushButton('Back', self)
        layout.addWidget(self.back_button)

        self.message_label = QLabel('', self)
        layout.addWidget(self.message_label)

        self.setLayout(layout)
        self.setWindowTitle('Two-step Authentication')
