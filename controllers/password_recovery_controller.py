import hashlib
import random
import string
from services.user_service import UserService
from services.mail_sender import MailSender

class PasswordRecoveryController:
    def __init__(self, view, main_window, user_service, mail_sender):
        self.view = view
        self.main_window = main_window
        self.user_service = user_service
        self.mail_sender =mail_sender
        self.user = None

        self.view.send_code_button.clicked.connect(self.send_recovery_code)
        self.view.recover_button.clicked.connect(self.recover_password)
        self.view.back_button.clicked.connect(self.back_to_login)

    def send_recovery_code(self):
        email = self.view.email_input.text()
        self.user = self.user_service.get_user_by_email(email)

        if self.user:
            code = self.user_service.generate_token()
            self.user.reset_code = code
            self.user_service.update_user(self.user)

            self.mail_sender.send_email(
                self.user.email,
                subject="Password Recovery Code",
                body=f"Your password recovery code is: {code}"
            )
            self.view.message_label.setText('Recovery code sent to your email.')
        else:
            self.view.message_label.setText('Email not found.')

    def recover_password(self):
        email = self.view.email_input.text()
        self.user = self.user_service.get_user_by_email(email)

        if self.user is None:
            self.view.message_label.setText('Please enter email')
            return

        if self.user.reset_code is None:
            self.view.message_label.setText('Please request a recovery code first.')
            return

        code = self.view.code_input.text()
        new_password = self.view.new_password_input.text()

        if self.user.reset_code == code:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            self.user.password = hashed_password
            self.user.reset_code = None
            self.user_service.update_user(self.user)
            self.view.message_label.setText('Password successfully updated.')
        else:
            self.view.message_label.setText('Invalid code.')

    def back_to_login(self):
        self.view.message_label.setText('')
        self.main_window.show_login_view()
