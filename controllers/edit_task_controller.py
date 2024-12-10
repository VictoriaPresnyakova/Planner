import traceback
from PyQt5.QtWidgets import QMessageBox

class EditTaskController:
    def __init__(self, view, main_window, task, task_service, user_service):
        self.view = view
        self.main_window = main_window
        self.task = task
        self.task_service = task_service
        self.user_service = user_service

        self.view.save_button.clicked.connect(self.save_task)
        self.view.delete_button.clicked.connect(self.delete_task)  # Подключаем обработчик удаления
        self.view.back_button.clicked.connect(self.back)
        self.load_task_details()

    def load_task_details(self):
        try:
            self.view.title_input.setText(self.task.title)
            self.view.description_input.setText(self.task.description)
            self.view.status_input.setCurrentText(self.task.status)

            users = self.user_service.get_all_users()
            user_map = {user.id: f"{user.name} {user.surname}" for user in users}
            self.view.assigned_user_input.addItems(user_map.values())
            assigned_user_name = user_map.get(self.task.assigned_user_id, "Unassigned")
            self.view.assigned_user_input.setCurrentText(assigned_user_name)

            if self.task.deadline:
                self.view.deadline_input.setDateTime(self.task.deadline)
        except Exception as e:
            traceback.print_exc()
            self.back()

    def save_task(self):
        try:
            if self.view.title_input.text() == '':
                self.view.message_label.setText('Empty title')
                return

            self.task.title = self.view.title_input.text()
            self.task.description = self.view.description_input.text()
            self.task.status = self.view.status_input.currentText()

            assigned_user_name = self.view.assigned_user_input.currentText()
            user = next((u for u in self.user_service.get_all_users() if f"{u.name} {u.surname}" == assigned_user_name), None)
            self.task.assigned_user_id = user.id if user else None

            self.task.deadline = self.view.deadline_input.dateTime().toPyDateTime() if self.view.deadline_input.text() else None

            self.task_service.update_task(self.task)
            self.main_window.task_list_controller.load_tasks()  # Обновляем список задач
            self.back()  # Возвращаемся на страницу списка задач
        except Exception as e:
            traceback.print_exc()
            self.back()

    def delete_task(self):
        try:
            confirmation = self.confirm_delete()
            if confirmation:
                self.task_service.delete_task_by_id(self.task.id)  # Удаляем задачу
                self.main_window.task_list_controller.load_tasks()  # Обновляем список задач
                self.back()  # Возвращаемся на страницу списка задач
        except Exception as e:
            traceback.print_exc()
            self.back()

    def confirm_delete(self):
        try:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Confirm Deletion")
            msg_box.setText("Are you sure you want to delete this task?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            response = msg_box.exec()
            return response == QMessageBox.Yes
        except Exception as e:
            traceback.print_exc()
            self.back()

    def back(self):
        try:
            self.main_window.show_task_list_view()
        except Exception as e:
            traceback.print_exc()
            self.main_window.show_initial_view()
