from kivy.app import App
from kivy.uix.modalview import ModalView

from automaticbrowserlogin.ui.menu import Menu
from automaticbrowserlogin.ui.popupio import PopupIO


class DeletePopup(ModalView):
    def __init__(self, button_number):
        super().__init__()
        self.popup_io = PopupIO(button_number)

    def delete_info_btn(self):
        self.popup_io.delete_login()
        Menu.refresh_screen(App.get_running_app().root)
        self.dismiss()
