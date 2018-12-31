from kivy.app import App
from kivy.uix.modalview import ModalView

from automaticbrowserlogin.ui.menu import Menu
from automaticbrowserlogin.ui.popupio import PopupIO


class ModifyPopup(ModalView):
    def __init__(self, button_number):
        super().__init__()
        self.popup_io = PopupIO(button_number)
        self.load_input()

    def load_input(self):
        self.ids.website_input.text, self.ids.user_input.text, self.ids.password_input.text = self.popup_io.load_input()
        pass

    def save_input(self):
        self.popup_io.delete_login()
        self.popup_io.save_input(self.ids.website_input.text, self.ids.user_input.text,
                                 self.ids.password_input.text.encode())
        Menu.refresh_screen(App.get_running_app().root)
        self.dismiss()
