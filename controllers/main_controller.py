import traceback

from models.user import User


class MainController:
    def __init__(self, view, main_window, user: User):
        self.view = view
        self.main_window = main_window
        self.view.profile_button.clicked.connect(lambda: self.main_window.show_profile_view())
        self.view.create_task_button.clicked.connect(lambda: self.main_window.show_create_task_view())
        self.view.view_tasks_button.clicked.connect(lambda: self.main_window.show_task_list_view())
        self.view.exit_button.clicked.connect(self.exit)

    def exit(self):
        try:
            self.main_window.set_current_user(None)
            self.main_window.show_initial_view()
        except Exception as e:
            traceback.print_exc()
            self.main_window.show_initial_view()



