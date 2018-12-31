import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder

from automaticbrowserlogin.ui.menu import Menu
from automaticbrowserlogin.ui.addpopup import AddPopup
from automaticbrowserlogin.ui.deletepopup import DeletePopup
from automaticbrowserlogin.ui.modifypopup import ModifyPopup
from automaticbrowserlogin.ui.optionspopup import OptionsPopup
from automaticbrowserlogin import root_directory


kivy.require("1.10.0")

Window.clearcolor = (1, 1, 1, 1)


class AutomaticBrowserLogin(App):
    def build(self):
        self.icon = root_directory + "/Icon.png"
        self.register_classes()
        Builder.load_file(root_directory + "/automaticbrowserlogin/automaticbrowserlogin.kv")
        return Menu()

    @staticmethod
    def register_classes():
        Factory.register("AddPopup", cls=AddPopup)
        Factory.register("DeletePopup", cls=DeletePopup)
        Factory.register("ModifyPopup", cls=ModifyPopup)
        Factory.register("OptionsPopup", cls=OptionsPopup)


if __name__ == "__main__":
    AutomaticBrowserLogin().run()
