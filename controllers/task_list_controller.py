from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt


class TaskListController:
    def __init__(self, view, main_window, task_service, user_service):
        self.view = view
        self.main_window = main_window
        self.task_service = task_service
        self.user_service = user_service
        self.view.back_button.clicked.connect(self.back)
        self.view.table.cellDoubleClicked.connect(self.open_task_details)
        self.load_tasks()

    def back(self):
        self.main_window.show_main_view()

    def load_tasks(self):
        tasks = self.task_service.get_all_tasks()
        self.view.table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            #TODO
            item = QTableWidgetItem(str(task.id))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Только для чтения
            self.view.table.setItem(row, 0, item)
            self.view.table.setItem(row, 1, QTableWidgetItem(task.title))
            self.view.table.setItem(row, 2, QTableWidgetItem(task.description))
            self.view.table.setItem(row, 3, QTableWidgetItem(task.status))
            assigned_user = self.user_service.find_user_by_id(task.assigned_user_id)
            assigned_user_name = f"{assigned_user.name} {assigned_user.surname}" if assigned_user else "Unassigned"
            self.view.table.setItem(row, 4, QTableWidgetItem(assigned_user_name))
            self.view.table.setItem(row, 5, QTableWidgetItem(task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "No deadline"))

    def open_task_details(self, row, column):
        task_id = int(self.view.table.item(row, 0).text())
        task = self.task_service.find_task_by_id(task_id)
        self.main_window.show_task_edit_view(task)
