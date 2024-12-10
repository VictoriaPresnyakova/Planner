import unittest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QDateTime

from views.create_task_view import CreateTaskView
from controllers.create_task_controller import CreateTaskController
from models.user import User

class TestCreateTask(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем экземпляр QApplication
        cls.app = QApplication([])

    def setUp(self):
        # Создаем представление создания задачи
        self.view = CreateTaskView()

        # Мок для TaskService
        self.task_service = MagicMock()

        # Мок для UserService
        self.user_service = MagicMock()
        self.user_service.get_all_users.return_value = [
            User(id=1, name='Alice', surname='Smith'),
            User(id=2, name='Bob', surname='Johnson')
        ]

        # Мок для main_window
        self.main_window = MagicMock()
        self.main_window.show_main_view = MagicMock()

        # Тестовый пользователь
        self.user = User(id=3, name='Test', surname='User')

        # Инициализация контроллера
        self.controller = CreateTaskController(self.view, self.main_window, self.user, self.task_service, self.user_service)

        # Отображаем вид для тестов
        self.view.show()

    def test_successful_task_creation(self):
        # Ввод данных в поля
        QTest.keyClicks(self.view.title_input, 'Test Task')
        QTest.keyClicks(self.view.description_input, 'This is a test description')

        # Выбор пользователя из выпадающего списка
        self.view.assigned_user_id_input.setCurrentIndex(1)  # Выбираем первого пользователя из списка

        # Установка дедлайна
        self.view.deadline_input.setDateTime(QDateTime.fromString('2024-06-30 15:00', 'yyyy-MM-dd HH:mm'))

        # Нажатие на кнопку сохранения
        QTest.mouseClick(self.view.save_button, Qt.LeftButton)

        # Проверка вызова метода создания задачи
        self.task_service.create_task.assert_called_once_with({
            'title': 'Test Task',
            'description': 'This is a test description',
            'assigned_user_id': 1,
            'deadline': '2024-06-30 15:00:00',
            'created_at': unittest.mock.ANY,
            'user_id': 3
        })

        # Проверка сообщения об успешном создании
        self.assertEqual(self.view.message_label.text(), 'Task created successfully!')

    def test_task_creation_with_empty_title(self):
        # Ввод пустого заголовка
        QTest.keyClicks(self.view.title_input, '')

        # Нажатие на кнопку сохранения
        QTest.mouseClick(self.view.save_button, Qt.LeftButton)

        # Проверка сообщения об ошибке
        self.assertEqual(self.view.message_label.text(), 'Empty title')

        # Проверка, что метод создания задачи не был вызван
        self.task_service.create_task.assert_not_called()

    def test_task_creation_without_deadline(self):
        # Ввод данных в поля
        QTest.keyClicks(self.view.title_input, 'Task Without Deadline')
        QTest.keyClicks(self.view.description_input, 'No deadline for this task')

        # Установка чекбокса "No Deadline"
        self.view.hide_deadline_checkbox.setChecked(True)

        # Нажатие на кнопку сохранения
        QTest.mouseClick(self.view.save_button, Qt.LeftButton)

        # Проверка вызова метода создания задачи с дедлайном None
        self.task_service.create_task.assert_called_once_with({
            'title': 'Task Without Deadline',
            'description': 'No deadline for this task',
            'assigned_user_id': None,
            'deadline': None,
            'created_at': unittest.mock.ANY,
            'user_id': 3
        })

        # Проверка сообщения об успешном создании
        self.assertEqual(self.view.message_label.text(), 'Task created successfully!')

    def test_load_user_data(self):
        # Проверка, что список пользователей загружен корректно
        self.assertEqual(self.view.assigned_user_id_input.count(), 3)  # Пустой элемент + 2 пользователя
        self.assertEqual(self.view.assigned_user_id_input.itemText(1), 'Alice Smith')
        self.assertEqual(self.view.assigned_user_id_input.itemText(2), 'Bob Johnson')

    def test_back_button(self):
        # Нажатие на кнопку "Back"
        QTest.mouseClick(self.view.back_button, Qt.LeftButton)

        # Проверка, что вызван метод возврата на главный экран
        self.main_window.show_main_view.assert_called_once()

if __name__ == '__main__':
    unittest.main()
