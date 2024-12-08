from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

from models.user import User


class TaskListController:
    def __init__(self, view, main_window, user: User, task_service, user_service):
        self.view = view
        self.main_window = main_window
        self.user = user
        self.task_service = task_service
        self.user_service = user_service
        self.view.back_button.clicked.connect(self.back)
        self.view.table.cellDoubleClicked.connect(self.open_task_details)
        self.load_tasks()

    def back(self):
        self.main_window.show_main_view()

    def load_tasks(self):
        tasks = self.task_service.get_tasks_by_user_id(self.user.id)

        self.view.table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            self._add_readonly_item(row, 0, str(task.id))
            self._add_readonly_item(row, 1, task.title)
            self._add_readonly_item(row, 2, task.description)
            self._add_readonly_item(row, 3, task.status)
            assigned_user = self.user_service.find_user_by_id(task.assigned_user_id)
            assigned_user_name = f"{assigned_user.name} {assigned_user.surname}" if assigned_user else "Unassigned"
            self._add_readonly_item(row, 4, assigned_user_name)
            self._add_readonly_item(row, 5,
                task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "No deadline")

    def _add_readonly_item(self, row, column, text):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Только для чтения
        self.view.table.setItem(row, column, item)

    def open_task_details(self, row, column):
        task_id = int(self.view.table.item(row, 0).text())
        task = self.task_service.find_task_by_id(task_id)
        self.main_window.show_task_edit_view(task)
