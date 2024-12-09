import datetime

from models.user import User
from services.task_service import TaskService
from services.user_service import UserService


class CreateTaskController:
    def __init__(self, view, main_window, user):
        self.view = view
        self.main_window = main_window
        self.user = user
        self.task_service = TaskService()
        self.user_service = UserService()
        self.load_user_data()
        self.view.save_button.clicked.connect(self.save_task_data)
        self.view.back_button.clicked.connect(self.back)
        self.view.hide_deadline_checkbox.stateChanged.connect(self.toggle_deadline_visibility)  # Обработка чекбокса

    def toggle_deadline_visibility(self, state):
        is_hidden = state == 2  # 2 означает, что чекбокс установлен
        self.view.deadline_label.setVisible(not is_hidden)
        self.view.deadline_input.setVisible(not is_hidden)

    def back(self):
        self.view.message_label.setText('')
        self.main_window.show_main_view()

    def clear_deadline(self):
        self.view.deadline_input.clear()

    def load_user_data(self):
        users = self.user_service.get_all_users()
        self.view.assigned_user_id_input.addItem('', None)
        for user in users:
            full_name = f"{user.name} {user.surname}"
            self.view.assigned_user_id_input.addItem(full_name,
                                                     user.id)  # Добавляем отображаемый текст и id в QComboBox

    def save_task_data(self):
        if self.view.title_input.text() == '':
            self.view.message_label.setText('Empty title')
            return

        try:
            # Если галочка установлена, deadline = None
            deadline = None if self.view.hide_deadline_checkbox.isChecked() else self.view.deadline_input.dateTime().toString(
                "yyyy-MM-dd HH:mm:ss")

            self.task_service.create_task({
                'title': self.view.title_input.text(),  # Получаем id выбранного пользователя
                'description': self.view.description_input.text(),
                'assigned_user_id': self.view.assigned_user_id_input.currentData(),
                'deadline': deadline,
                'created_at': datetime.datetime.now(),
                'user_id': self.user.id
            })
            self.view.message_label.setText("Task created successfully!")
        except Exception as e:
            self.view.message_label.setText(f"Error creating task: {e}")
