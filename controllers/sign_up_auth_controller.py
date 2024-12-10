import traceback

from models.user import User
from services.mail_sender import MailSender
from services.user_service import UserService


class SignUpAuthController:
    def __init__(self, view, main_window, user_service, mail_sender):
        self.view = view
        self.main_window = main_window
        self.user_kwargs = None
        self.user_service = user_service
        self.mail_sender = mail_sender
        self.view.verify_button.clicked.connect(self.verify_token)
        self.view.resend_token_button.clicked.connect(self.resend_token)
        self.view.back_button.clicked.connect(self.back)

    def back(self):
        try:
            self.view.message_label.setText('')
            self.main_window.show_signup_view()
        except Exception as e:
            traceback.print_exc()
            self.main_window.show_initial_view()

    def resend_token(self):
        try:
            if self.user_kwargs:
                token = self.user_service.generate_token()
                self.user_kwargs['auth_token'] = token
                self.mail_sender.send_email(self.user_kwargs['email'], subject="Your Authentication Token",
                                            body=f"Your authentication token is: {token}")
                self.view.message_label.setText('Token was resend')
        except Exception as e:
            traceback.print_exc()
            self.back()

    def verify_token(self):
        try:
            token = self.view.token_input.text()
            try:
                if self.user_kwargs and self.user_kwargs['auth_token'] == token:
                    self.user_kwargs['auth_token'] = None
                    user = self.user_service.create_user(self.user_kwargs)
                    if not user:
                        raise Exception('Error while save user')
                    self.main_window.show_login_view()
                else:
                    self.view.message_label.setText('Invalid token')
            except Exception as e:
                self.view.message_label.setText(f'Sign up failed: {str(e)}')
        except Exception as e:
            traceback.print_exc()
            self.back()

    def set_user(self, kwargs):
        try:
            self.user_kwargs = kwargs
        except Exception as e:
            traceback.print_exc()
            self.back()
