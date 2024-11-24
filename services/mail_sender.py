import smtplib
from misc.config import *
from email.mime.text import MIMEText


class MailSender:
    def __init__(self):
        self.from_email = EMAIL
        self.from_password = EMAIL_PASSWORD

    def send_email(self, to_email, subject, body):
        print(to_email, subject, body)
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.from_email, self.from_password)
            server.sendmail(self.from_email, to_email, msg.as_string())