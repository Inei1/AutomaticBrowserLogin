from kivy.app import App
from kivy.uix.modalview import ModalView

from automaticbrowserlogin.ui.menu import Menu
from automaticbrowserlogin.ui.popupio import PopupIO
from automaticbrowserlogin import user_info_directory


class ModifyPopup(ModalView):
    """
    Defines the logic for the modify popup.
    """
    def __init__(self, button_number):
        super().__init__()
        self.popup_io = PopupIO(button_number, user_info_directory)
        self.load_input()

    def load_input(self):
        self.ids.website_input.text, self.ids.user_input.text, self.ids.password_input.text = self.popup_io.load_login()

    def save_input(self):
        self.popup_io.delete_login()
        self.popup_io.save_login(self.ids.website_input.text, self.ids.user_input.text,
                                 self.ids.password_input.text.encode())
        Menu.refresh_screen(App.get_running_app().root)
        self.dismiss()
