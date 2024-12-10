import unittest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import hashlib

from views.login_view import LoginView
from controllers.login_controller import LoginController
from models.user import User


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем экземпляр QApplication
        cls.app = QApplication([])

    def setUp(self):
        # Создаем представление логина
        self.view = LoginView()

        # Создаем мок для UserService
        self.user_service = MagicMock()

        # Создаем мок для MailSender
        self.mail_sender = MagicMock()

        # Создаем мок для main_window
        self.main_window = MagicMock()
        self.main_window.auth_controller = MagicMock()
        self.main_window.show_auth_view = MagicMock()
        self.main_window.show_initial_view = MagicMock()
        self.main_window.show_password_recovery_view = MagicMock()

        # Инициализируем контроллер с моками
        self.controller = LoginController(self.view, self.main_window, self.user_service, self.mail_sender)
        self.view.show()

    def test_successful_login_without_token(self):
        # Настройка пользователя без токена
        user = User(id=1, email='admin@mail.ru', password=hashlib.sha256('12345'.encode()).hexdigest(), auth_token=None)
        self.user_service.get_user_by_email.return_value = user

        # Ввод данных в поля
        QTest.keyClicks(self.view.username_input, 'admin@mail.ru')
        QTest.keyClicks(self.view.password_input, '12345')

        # Нажатие на кнопку логина
        QTest.mouseClick(self.view.login_button, Qt.LeftButton)

        # Проверка отправки токена по почте
        self.mail_sender.send_email.assert_called_once_with(
            'admin@mail.ru',
            subject="Your Authentication Token",
            body=unittest.mock.ANY  # Токен может быть разным, поэтому используем ANY
        )

        # Проверка, что вызван метод показа аутентификации
        self.main_window.show_auth_view.assert_called_once()

    def test_successful_login_with_token(self):
        # Настройка пользователя с существующим токеном
        user = User(id=1, email='admin@mail.ru', password=hashlib.sha256('12345'.encode()).hexdigest(),
                    auth_token='TOKEN123')
        self.user_service.get_user_by_email.return_value = user

        # Ввод данных в поля
        QTest.keyClicks(self.view.username_input, 'admin@mail.ru')
        QTest.keyClicks(self.view.password_input, '12345')

        # Нажатие на кнопку логина
        QTest.mouseClick(self.view.login_button, Qt.LeftButton)

        # Проверка, что письмо не отправлялось
        self.mail_sender.send_email.assert_not_called()

        # Проверка, что вызван метод показа аутентификации
        self.main_window.show_auth_view.assert_called_once()

    def test_login_with_invalid_credentials(self):
        # Настройка отсутствующего пользователя
        self.user_service.get_user_by_email.return_value = None

        # Ввод неверных данных
        QTest.keyClicks(self.view.username_input, 'invalid@mail.ru')
        QTest.keyClicks(self.view.password_input, 'wrongpassword')

        # Нажатие на кнопку логина
        QTest.mouseClick(self.view.login_button, Qt.LeftButton)

        # Проверка сообщения об ошибке
        self.assertEqual(self.view.message_label.text(), 'Invalid credentials')

    def test_login_back_button(self):
        # Нажатие на кнопку "Back"
        QTest.mouseClick(self.view.back_button, Qt.LeftButton)

        # Проверка, что вызван метод возврата на начальный экран
        self.main_window.show_initial_view.assert_called_once()

    def test_forgot_password_button(self):
        # Нажатие на кнопку "Forgot Password?"
        QTest.mouseClick(self.view.forgot_password_button, Qt.LeftButton)

        # Проверка, что вызван метод восстановления пароля
        self.main_window.show_password_recovery_view.assert_called_once()


if __name__ == '__main__':
    unittest.main()
