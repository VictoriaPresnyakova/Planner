import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from views.signup_view import SignUpView
from controllers.signup_controller import SignUpController
from services.user_service import UserService
from services.mail_sender import MailSender
from unittest.mock import MagicMock

app = QApplication([])  # Инициализация QApplication для тестов

class TestSignUp(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр представления
        self.view = SignUpView()

        # Создаем мок-сервисы для пользователя и отправки почты
        self.user_service = MagicMock(spec=UserService)
        self.mail_sender = MagicMock(spec=MailSender)

        # Создаем мок для main_window
        self.main_window = MagicMock()
        self.main_window.sign_up_auth_controller = MagicMock()
        self.main_window.show_sign_up_auth_view = MagicMock()

        # Инициализируем контроллер с моками
        self.controller = SignUpController(self.view, self.main_window, self.user_service, self.mail_sender)
        self.view.show()

    def tearDown(self):
        self.view.close()

    def test_successful_signup(self):
        # Настройка поведения мока для создания пользователя
        self.user_service.get_user_by_email.return_value = None

        # Ввод данных в поля
        QTest.keyClicks(self.view.email_input, 'test@example.com')
        QTest.keyClicks(self.view.password_input, 'password123')
        QTest.keyClicks(self.view.name_input, 'John')
        QTest.keyClicks(self.view.surname_input, 'Doe')

        # Нажатие на кнопку регистрации
        QTest.mouseClick(self.view.signup_button, Qt.LeftButton)

        # Проверка, что был вызван метод перехода на аутентификацию токеном
        self.main_window.show_sign_up_auth_view.assert_called_once()

    def test_signup_with_existing_email(self):
        # Настройка поведения мока для существующего пользователя
        self.user_service.get_user_by_email.return_value = True

        # Ввод данных в поля
        QTest.keyClicks(self.view.email_input, 'admin@mail.ru')
        QTest.keyClicks(self.view.password_input, 'password123')
        QTest.keyClicks(self.view.name_input, 'Jane')
        QTest.keyClicks(self.view.surname_input, 'Doe')

        # Нажатие на кнопку регистрации
        QTest.mouseClick(self.view.signup_button, Qt.LeftButton)

        # Проверка сообщения об ошибке
        a = self.view.message_label.text()
        self.assertEqual(self.view.message_label.text(), 'User with such email already exists')

    def test_signup_with_empty_fields(self):
        # Нажатие на кнопку регистрации без ввода данных
        QTest.mouseClick(self.view.signup_button, Qt.LeftButton)

        # Проверка сообщения об ошибке
        print(self.view.message_label.text())
        self.assertEqual(self.view.message_label.text(), 'Empty email')

if __name__ == '__main__':
    unittest.main()
