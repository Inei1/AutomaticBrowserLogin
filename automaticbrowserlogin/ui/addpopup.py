from kivy.app import App
from kivy.uix.modalview import ModalView

from automaticbrowserlogin.ui.menu import Menu
from automaticbrowserlogin.ui.popupio import PopupIO


class AddPopup(ModalView):
    def __init__(self):
        super().__init__()
        self.popup_io = PopupIO(None)

    def save_input(self):
        self.popup_io.save_input(self.ids.website_input.text, self.ids.user_input.text,
                                 self.ids.password_input.text.encode())
        Menu.refresh_screen(App.get_running_app().root)
        self.dismiss()
