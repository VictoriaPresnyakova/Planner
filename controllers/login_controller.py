import hashlib
import traceback

from PyQt5.QtWidgets import QApplication

from models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from services.mail_sender import MailSender
from services.user_service import UserService
from views.login_view import LoginView


class LoginController:
    def __init__(self, view, main_window, user_service, mail_sender):
        self.view = view
        self.main_window = main_window
        self.view.login_button.clicked.connect(self.handle_login)
        self.view.back_button.clicked.connect(self.back)
        self.view.forgot_password_button.clicked.connect(lambda: self.main_window.show_password_recovery_view())
        self.user_service = user_service
        self.mail_sender = mail_sender

    def back(self):
        try:
            self.view.message_label.setText('')
            self.main_window.show_initial_view()
        except Exception as e:
            traceback.print_exc()
            self.main_window.show_initial_view()

    def handle_login(self):
        try:
            username = self.view.username_input.text()
            user = self.user_service.get_user_by_email(username)

            if user and user.password == hashlib.sha256(self.view.password_input.text().encode()).hexdigest():
                if not user.auth_token:
                    token = self.user_service.generate_token()
                    user.auth_token = token
                    self.user_service.update_user(user)
                    self.mail_sender.send_email(user.email, subject="Your Authentication Token",
                                                body=f"Your authentication token is: {token}")
                    self.main_window.auth_controller.set_user(user)
                    self.main_window.show_auth_view()
                else:
                    self.main_window.auth_controller.set_user(user)
                    self.main_window.show_auth_view()

            else:
                self.view.message_label.setText('Invalid credentials')
        except Exception as e:
            traceback.print_exc()
            self.back()
