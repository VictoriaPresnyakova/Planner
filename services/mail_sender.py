import smtplib
import time
import traceback
from threading import Thread

from misc.config import *
from email.mime.text import MIMEText


class MailSender:
    def __init__(self):
        self.from_email = EMAIL
        self.from_password = EMAIL_PASSWORD
        self.messages = []
        Thread(target=self._work, daemon=True).start()

    def _send_email(self, to_email, subject, body):
        print(to_email, subject, body)
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.from_email, self.from_password)
            server.sendmail(self.from_email, to_email, msg.as_string())

    def _send_email_async(self, message):
        self.messages.append(message)

    def send_email(self, to_email, subject, body):
        thread = Thread(target=self._send_email_async, args=({'to_email': to_email, 'subject': subject, 'body': body},), daemon=True)
        thread.start()
        return thread

    def _work(self):
        while True:
            if self.messages:
                for x in self.messages:
                    message = self.messages.pop(0)
                    try:
                        self._send_email(message.get('to_email', ''), message.get('subject', ''), message.get('body', ''))
                    except:
                        traceback.print_exc()
            else:
                time.sleep(1)