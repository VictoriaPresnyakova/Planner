from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QPushButton, QLabel,
    QLineEdit, QHeaderView, QTabWidget, QHBoxLayout
)

class TaskListView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("All Tasks", self)
        layout.addWidget(self.title_label)

        # Горизонтальный layout для поля фильтрации и кнопки сброса
        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Filter tasks...")
        filter_layout.addWidget(self.filter_input)

        self.reset_filter_button = QPushButton("Reset Filter", self)
        filter_layout.addWidget(self.reset_filter_button)

        layout.addLayout(filter_layout)

        # Вкладки для разделения задач
        self.tabs = QTabWidget(self)

        # Таблица для задач, назначенных пользователю
        self.assigned_table = QTableWidget(self)
        self.assigned_table.setColumnCount(6)
        self.assigned_table.setHorizontalHeaderLabels(["Created At", "Title", "Description", "Status", "Assigned User", "Deadline"])
        self.assigned_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.assigned_table.setSortingEnabled(True)
        self.assigned_table.verticalHeader().setVisible(False)

        # Таблица для задач, созданных пользователем
        self.created_table = QTableWidget(self)
        self.created_table.setColumnCount(6)
        self.created_table.setHorizontalHeaderLabels(["Created At", "Title", "Description", "Status", "Assigned User", "Deadline"])
        self.created_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.created_table.setSortingEnabled(True)
        self.created_table.verticalHeader().setVisible(False)

        # Добавляем таблицы во вкладки
        self.tabs.addTab(self.assigned_table, "Assigned to Me")
        self.tabs.addTab(self.created_table, "Created by Me")
        layout.addWidget(self.tabs)

        # Кнопка для возврата назад
        self.back_button = QPushButton("Back", self)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.setWindowTitle("Task List")
