from models.user import User


class MainController:
    def __init__(self, view, main_window, user: User):
        self.view = view
        self.main_window = main_window
        self.view.profile_button.clicked.connect(lambda: self.main_window.show_profile_view())
        self.view.exit_button.clicked.connect(self.exit)

    def exit(self):
        self.main_window.set_current_user(None)
        self.main_window.show_initial_view()



