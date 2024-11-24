from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel


class TaskListView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("All Tasks", self)
        layout.addWidget(self.title_label)

        # Таблица для отображения задач
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Description", "Status", "Assigned User", "Deadline"])
        layout.addWidget(self.table)

        # Кнопка для возврата назад
        self.back_button = QPushButton("Back", self)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.setWindowTitle("Task List")
