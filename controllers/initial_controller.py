import traceback

from views.initial_view import InitialView


class InitialController:
    def __init__(self, view, main_window):
        self.view = view
        self.main_window = main_window
        self.view.login_button.clicked.connect(self.show_login)
        self.view.signup_button.clicked.connect(self.show_signup)

    def show_login(self):
        try:
            self.main_window.show_login_view()
        except Exception as e:
            traceback.print_exc()
            self.main_window.show_initial_view()

    def show_signup(self):
        try:
            self.main_window.show_signup_view()
        except Exception as e:
            traceback.print_exc()
            self.main_window.show_initial_view()

