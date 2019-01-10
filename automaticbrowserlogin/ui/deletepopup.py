from kivy.app import App
from kivy.uix.modalview import ModalView

from automaticbrowserlogin.ui.menu import Menu
from automaticbrowserlogin.ui.popupio import PopupIO
from automaticbrowserlogin import user_info_directory


class DeletePopup(ModalView):
    """
    This class contains the logic for the delete popup.
    """
    def __init__(self, button_number):
        super().__init__()
        self.popup_io = PopupIO(button_number, user_info_directory)

    def delete_info_btn(self):
        self.popup_io.delete_login()
        Menu.refresh_screen(App.get_running_app().root)
        self.dismiss()
