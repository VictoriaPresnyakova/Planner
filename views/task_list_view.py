from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QLabel, QLineEdit, QHeaderView, QTableView
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp

class TaskListView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("All Tasks", self)
        layout.addWidget(self.title_label)

        # Поле для фильтрации
        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Filter tasks...")
        layout.addWidget(self.filter_input)

        # Таблица для отображения задач
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Created At", "Title", "Description", "Status", "Assigned User", "Deadline"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)  # Включаем сортировку
        layout.addWidget(self.table)

        # Кнопка для возврата назад
        self.back_button = QPushButton("Back", self)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.setWindowTitle("Task List")
