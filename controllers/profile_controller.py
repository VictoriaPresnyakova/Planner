from models.user import User
from services.user_service import UserService


class ProfileController:
    def __init__(self, view, main_window, user):
        self.view = view
        self.main_window = main_window
        self.user = user
        self.load_user_data()
        self.view.save_button.clicked.connect(self.save_user_data)
        self.view.back_button.clicked.connect(self.back)
        self.user_service = UserService()

    def back(self):
        self.view.message_label.setText('')
        self.main_window.show_main_view()

    def load_user_data(self):
        self.view.email_input.setText(self.user.email)
        self.view.name_input.setText(self.user.name)
        self.view.surname_input.setText(self.user.surname)

    def save_user_data(self):
        if self.view.name_input.text() == '':
            self.view.message_label.setText('Empty name')
            return
        if self.view.surname_input.text() == '':
            self.view.message_label.setText('Empty surname')
            return
        self.user.name = self.view.name_input.text()
        self.user.surname = self.view.surname_input.text()
        try:
            self.user = self.user_service.update_user(self.user)
            if self.user:
                self.view.message_label.setText('Profile updated successfully')
            else:
                raise Exception('Error while saving')
        except Exception as e:
            self.view.message_label.setText(f'Error updating profile: {str(e)}')
