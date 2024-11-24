from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton


class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.profile_button = QPushButton('Profile', self)
        layout.addWidget(self.profile_button)

        self.exit_button = QPushButton('Exit', self)
        layout.addWidget(self.exit_button)

        self.welcome_label = QLabel('Welcome to the Main Application!', self)
        layout.addWidget(self.welcome_label)

        self.setLayout(layout)
        self.setWindowTitle('Main Application')