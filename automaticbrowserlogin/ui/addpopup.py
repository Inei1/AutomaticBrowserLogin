from kivy.app import App
from kivy.uix.modalview import ModalView

from automaticbrowserlogin.ui.menu import Menu
from automaticbrowserlogin.ui.popupio import PopupIO
from automaticbrowserlogin import user_info_directory


class AddPopup(ModalView):
    """
    This class contains the logic for the add popup.
    """
    def __init__(self):
        super().__init__()
        self.popup_io = PopupIO(None, user_info_directory)

    def save_input(self):
        self.popup_io.save_login(self.ids.website_input.text, self.ids.user_input.text,
                                 self.ids.password_input.text.encode())
        Menu.refresh_screen(App.get_running_app().root)
        self.dismiss()
