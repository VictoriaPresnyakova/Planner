import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QMessageBox


from repositories.db.enums import TaskStatus
from views.edit_task_view import EditTaskView
from controllers.edit_task_controller import EditTaskController
from models.task import Task
from models.user import User


class TestEditTask(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        # Создаем представление редактирования задачи
        self.view = EditTaskView()

        # Моки для сервисов
        self.task_service = MagicMock()
        self.user_service = MagicMock()
        self.user_service.get_all_users.return_value = [
            User(id=1, name='Alice', surname='Smith'),
            User(id=2, name='Bob', surname='Johnson')
        ]

        # Мок для main_window
        self.main_window = MagicMock()
        self.main_window.task_list_controller.load_tasks = MagicMock()
        self.main_window.show_task_list_view = MagicMock()

        # Тестовая задача
        self.task = Task(
            id=101,
            title='Test Task',
            description='Test Description',
            status=TaskStatus.IN_PROCESS,
            assigned_user_id=1,
            deadline=QDateTime.fromString('2024-06-30 15:00', 'yyyy-MM-dd HH:mm').toPyDateTime()
        )

        # Инициализация контроллера
        self.controller = EditTaskController(self.view, self.main_window, self.task, self.task_service, self.user_service)

    def test_load_task_details(self):
        # Проверка загрузки данных задачи в форму
        self.assertEqual(self.view.title_input.text(), 'Test Task')
        self.assertEqual(self.view.description_input.text(), 'Test Description')
        self.assertEqual(self.view.status_input.currentText(), TaskStatus.IN_PROCESS)
        self.assertEqual(self.view.assigned_user_input.currentText(), 'Alice Smith')
        self.assertEqual(self.view.deadline_input.dateTime().toString('yyyy-MM-dd HH:mm'), '2024-06-30 15:00')

    def test_successful_task_save(self):
        # Изменяем данные в форме
        QTest.keyClicks(self.view.title_input, ' Updated')
        QTest.keyClicks(self.view.description_input, ' Updated')
        self.view.status_input.setCurrentText(TaskStatus.DONE)
        self.view.assigned_user_input.setCurrentText('Bob Johnson')
        self.view.deadline_input.setDateTime(QDateTime.fromString('2024-07-01 12:00', 'yyyy-MM-dd HH:mm'))

        # Нажатие на кнопку сохранения
        QTest.mouseClick(self.view.save_button, Qt.LeftButton)

        # Проверка вызова метода обновления задачи
        self.task_service.update_task.assert_called_once()
        updated_task = self.task_service.update_task.call_args[0][0]

        self.assertEqual(updated_task.title, 'Test Task Updated')
        self.assertEqual(updated_task.description, 'Test Description Updated')
        self.assertEqual(updated_task.status, TaskStatus.DONE)
        self.assertEqual(updated_task.assigned_user_id, 2)
        self.assertEqual(updated_task.deadline.strftime('%Y-%m-%d %H:%M'), '2024-07-01 12:00')

        # Проверка возврата к списку задач
        self.main_window.task_list_controller.load_tasks.assert_called_once()
        self.main_window.show_task_list_view.assert_called_once()

    def test_task_save_with_empty_title(self):
        # Очищаем поле заголовка
        self.view.title_input.clear()

        # Нажатие на кнопку сохранения
        QTest.mouseClick(self.view.save_button, Qt.LeftButton)

        # Проверка, что задача не была сохранена
        self.task_service.update_task.assert_not_called()

    def test_back_button(self):
        # Нажатие на кнопку "Back"
        QTest.mouseClick(self.view.back_button, Qt.LeftButton)

        # Проверка вызова метода возврата на список задач
        self.main_window.show_task_list_view.assert_called_once()


if __name__ == '__main__':
    unittest.main()
