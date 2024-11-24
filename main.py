from threading import Thread

from PyQt5.QtWidgets import QApplication, QMessageBox

from controllers.auth_controller import AuthController
from controllers.initial_controller import InitialController
from controllers.main_controller import MainController
from controllers.profile_controller import ProfileController
from controllers.sign_up_auth_controller import SignUpAuthController
from controllers.signup_controller import SignUpController
from controllers.login_controller import LoginController
from models.user import User
from repositories.db.migrate import alembic_auto_migrate
from views.auth_view import AuthView
from views.initial_view import InitialView
from views.login_view import LoginView


from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from views.login_view import LoginView
from views.main_view import MainView
from views.profile_view import ProfileView
from views.sign_up_auth_view import SignUpAuthView
from views.signup_view import SignUpView

CURRENT_USER = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.setWindowTitle('Planner')

        # Initialize views
        self.initial_view = InitialView()
        self.login_view = LoginView()
        self.signup_view = SignUpView()
        self.signup_auth_view = SignUpAuthView()
        self.auth_view = AuthView()
        self.profile_view = ProfileView()
        self.main_view = MainView()

        # Initialize controllers
        self.initial_controller = InitialController(self.initial_view, self)
        self.login_controller = LoginController(self.login_view, self)
        self.signup_controller = SignUpController(self.signup_view, self)
        self.auth_controller = AuthController(self.auth_view, self)
        self.sign_up_auth_controller = SignUpAuthController(self.signup_auth_view, self)
        self.main_controller = None
        self.settings_controller = None
        self.profile_controller = None
        self.access_controller = None


        # Add views to stacked widget
        self.stacked_widget.addWidget(self.initial_view)
        self.stacked_widget.addWidget(self.login_view)
        self.stacked_widget.addWidget(self.signup_view)
        self.stacked_widget.addWidget(self.signup_auth_view)
        self.stacked_widget.addWidget(self.auth_view)
        self.stacked_widget.addWidget(self.profile_view)
        self.stacked_widget.addWidget(self.main_view)

        # Show initial view initially
        self.stacked_widget.setCurrentWidget(self.initial_view)

    def show_login_view(self):
        self.stacked_widget.setCurrentWidget(self.login_view)

    def show_auth_view(self):
        self.stacked_widget.setCurrentWidget(self.auth_view)

    def show_sign_up_auth_view(self):
        self.stacked_widget.setCurrentWidget(self.signup_auth_view)

    def show_signup_view(self):
        self.stacked_widget.setCurrentWidget(self.signup_view)

    def show_main_view(self):
        if CURRENT_USER:
            self.main_controller = MainController(self.main_view, self, CURRENT_USER)
            self.stacked_widget.setCurrentWidget(self.main_view)

    def show_initial_view(self):
        self.stacked_widget.setCurrentWidget(self.initial_view)

    def show_profile_view(self):
        if CURRENT_USER:
            self.profile_controller = ProfileController(self.profile_view, self, CURRENT_USER)
            self.stacked_widget.setCurrentWidget(self.profile_view)
        else:
            self.show_message_box('Please Log In', 'You should log in first',
                                                  lambda: self.show_main_view())

    def show_message_box(self, title, text, on_click=None):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        if on_click:
            msg.buttonClicked.connect(on_click)
            msg.destroyed.connect(on_click)
        x = msg.exec_()  # this will show our messagebox

    def set_current_user(self, user: User):
        global CURRENT_USER
        CURRENT_USER = user


if __name__ == '__main__':
    alembic_auto_migrate()

    app = QApplication([])
    main_window = MainWindow()
    main_window.showMaximized()
    main_window.show()

    app.exec_()