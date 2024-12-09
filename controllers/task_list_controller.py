from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
import openpyxl
from openpyxl.styles import Font
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os

class TaskListController:
    def __init__(self, view, main_window, user, task_service, user_service):
        self.view = view
        self.main_window = main_window
        self.user = user
        self.task_service = task_service
        self.user_service = user_service

        self.view.back_button.clicked.connect(self.back)
        self.view.filter_input.textChanged.connect(self.filter_tasks)
        self.view.reset_filter_button.clicked.connect(self.reset_filter)
        self.view.tabs.currentChanged.connect(self.load_tasks)

        self.view.assigned_table.cellDoubleClicked.connect(self.open_task_details)
        self.view.created_table.cellDoubleClicked.connect(self.open_task_details)

        self.view.export_excel_button.clicked.connect(self.export_to_excel)
        self.view.export_pdf_button.clicked.connect(self.export_to_pdf)

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
            self._add_readonly_item(table, row, 0, str(task.id))
            self._add_readonly_item(table, row, 1, task.created_at.strftime("%Y-%m-%d %H:%M") )
            self._add_readonly_item(table, row, 2, task.title)
            self._add_readonly_item(table, row, 3, task.description)
            self._add_readonly_item(table, row, 4, task.status)
            assigned_user = self.user_service.find_user_by_id(task.assigned_user_id)
            assigned_user_name = f"{assigned_user.name} {assigned_user.surname}" if assigned_user else "Unassigned"
            self._add_readonly_item(table, row, 5, assigned_user_name)
            self._add_readonly_item(table, row, 6,
                                    task.deadline.strftime("%Y-%m-%d %H:%M") if task.deadline else "No deadline")

        self.filter_tasks(self.view.filter_input.text())

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

    def reset_filter(self):
        """Сбрасывает фильтр и очищает поле ввода."""
        self.view.filter_input.clear()
        self.filter_tasks("")  # Сбрасываем фильтр, чтобы показать все строки

    def open_task_details(self, row, column):
        """Открывает детальную информацию о задаче для редактирования."""
        current_tab_index = self.view.tabs.currentIndex()

        if current_tab_index == 0:
            table = self.view.assigned_table
        else:
            table = self.view.created_table

        task_id = int(table.item(row, 0).text())
        task = self.task_service.find_task_by_id(task_id)
        self.main_window.show_task_edit_view(task)

    def _get_current_table(self):
        current_tab_index = self.view.tabs.currentIndex()
        return self.view.assigned_table if current_tab_index == 0 else self.view.created_table

    def export_to_excel(self):
        # Открываем диалог выбора папки
        folder_path = QFileDialog.getExistingDirectory(self.view, "Select Folder to Save Excel Report")
        if not folder_path:
            return  # Если пользователь отменил выбор

        file_path = os.path.join(folder_path, "tasks_report.xlsx")

        table = self._get_current_table()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Tasks"

        # Получаем видимые заголовки
        visible_columns = [col for col in range(table.columnCount()) if not table.isColumnHidden(col)]
        headers = [table.horizontalHeaderItem(col).text() for col in visible_columns]
        sheet.append(headers)

        # Стиль для заголовков
        for col_num, header in enumerate(headers, start=1):
            sheet.cell(row=1, column=col_num, value=header).font = Font(bold=True)

        # Добавляем видимые строки
        row_index = 2
        for row in range(table.rowCount()):
            if table.isRowHidden(row):
                continue
            row_data = [table.item(row, col).text() if table.item(row, col) else "" for col in visible_columns]
            sheet.append(row_data)
            row_index += 1

        # Сохранение файла
        workbook.save(file_path)
        QMessageBox.information(self.view, "Success", f"Report saved as {file_path}")

    def export_to_pdf(self):
        # Открываем диалог выбора папки
        folder_path = QFileDialog.getExistingDirectory(self.view, "Select Folder to Save PDF Report")
        if not folder_path:
            return  # Если пользователь отменил выбор

        file_path = os.path.join(folder_path, "tasks_report.pdf")

        table = self._get_current_table()
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        # Начальные координаты
        x_offset = 50
        y_offset = height - 50
        line_height = 20

        # Получаем видимые заголовки
        visible_columns = [col for col in range(table.columnCount()) if not table.isColumnHidden(col)]
        headers = [table.horizontalHeaderItem(col).text() for col in visible_columns]

        # Рисуем заголовки
        c.setFont("Helvetica-Bold", 12)
        for col_num, header in enumerate(headers):
            c.drawString(x_offset + col_num * 100, y_offset, header)
        y_offset -= line_height

        # Рисуем видимые строки
        c.setFont("Helvetica", 10)
        for row in range(table.rowCount()):
            if table.isRowHidden(row):
                continue
            for col_num, col in enumerate(visible_columns):
                item = table.item(row, col)
                text = item.text() if item else ""
                c.drawString(x_offset + col_num * 100, y_offset, text)
            y_offset -= line_height

            # Добавляем новую страницу при необходимости
            if y_offset < 50:
                c.showPage()
                y_offset = height - 50

        c.save()
        QMessageBox.information(self.view, "Success", f"Report saved as {file_path}")



