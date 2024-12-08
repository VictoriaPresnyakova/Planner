from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


class TaskListController:
    def __init__(self, view, main_window, user, task_service, user_service):
        self.view = view
        self.main_window = main_window
        self.user = user
        self.task_service = task_service
        self.user_service = user_service

        self.view.back_button.clicked.connect(self.back)
        self.view.filter_input.textChanged.connect(self.filter_tasks)
        self.view.tabs.currentChanged.connect(self.load_tasks)

        self.load_tasks()

    def back(self):
        self.main_window.show_main_view()

    def load_tasks(self):
        current_tab_index = self.view.tabs.currentIndex()

        if current_tab_index == 0:
            tasks = self.task_service.get_tasks_by_assigned_user_id(self.user.id)
            table = self.view.assigned_table
        else:
            tasks = self.task_service.get_tasks_created_by_user_id(self.user.id)
            table = self.view.created_table

        table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            self._add_readonly_item(table, row, 0, task.created_at.strftime("%Y-%m-%d %H:%M") )
            self._add_readonly_item(table, row, 1, task.title)
            self._add_readonly_item(table, row, 2, task.description)
            self._add_readonly_item(table, row, 3, task.status)
            assigned_user = self.user_service.find_user_by_id(task.assigned_user_id)
            assigned_user_name = f"{assigned_user.name} {assigned_user.surname}" if assigned_user else "Unassigned"
            self._add_readonly_item(table, row, 4, assigned_user_name)
            self._add_readonly_item(table, row, 5,
                                    task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "No deadline")

    def _add_readonly_item(self, table, row, column, text):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Только для чтения
        table.setItem(row, column, item)

    def filter_tasks(self, text):
        """Фильтрует таблицу по введённому тексту."""
        table = self.view.tabs.currentWidget()
        for row in range(table.rowCount()):
            row_hidden = True
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and text.lower() in item.text().lower():
                    row_hidden = False
                    break
            table.setRowHidden(row, row_hidden)
