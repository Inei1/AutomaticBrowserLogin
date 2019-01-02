from kivy.logger import Logger
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.label import Label

from automaticbrowserlogin.startup.startapp import run_autologin
from automaticbrowserlogin import user_info_directory

import os
import json


class Menu(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.refresh_screen()

    @staticmethod
    def run():
        run_autologin()

    def refresh_screen(self):
        while self.children[0].id is not None:
            self.remove_widget(self.children[0])
        Logger.debug("refreshing screen")
        try:
            user_info = open(user_info_directory, "rb")
        except FileNotFoundError:
            self.add_widget(self.get_standard_button("Add", 0.05, 0.8, "add_button", Factory.AddPopup().open))
            Logger.warning("no logins found")
            return

        Logger.debug("user_info:", user_info.read())
        user_info.seek(0)
        if os.stat(user_info.name).st_size == 0:
            add_button = self.get_standard_button("Add", 0.05, 0.8, "add_button", Factory.AddPopup().open)
            self.add_widget(add_button)
        else:
            for i, line in enumerate(user_info):
                Logger.debug("user info:", line[:-2].decode())
                login = json.loads(line[:-2].decode())
                delete_button = self.get_standard_button("Delete", 0.2, 0.8 - (0.1 * i), "delete_button" + str(i),
                                                         self.delete_button_function, i)
                self.add_widget(delete_button)

                modify_button = self.get_standard_button("Modify", 0.05, 0.8 - (0.1 * i), "modify_button" +
                                                         str(i), self.modify_button_function, i)
                self.add_widget(modify_button)

                website = login.get("website")
                website_label_text = "/".join(website.split("/", 3)[:3])
                website_label = Label(text="Website: " + website_label_text, size_hint=(0.5, 0.13),
                                      pos_hint={"x": 0.4, "y": 0.77 - (0.1 * i)}, font_size=24, color=(0, 0, 0, 1),
                                      id="Label" + str(i))
                self.add_widget(website_label)

                add_button = self.get_standard_button("Add", 0.05, 0.7 - (0.1 * i),
                                                      "add_button", Factory.AddPopup().open)
                self.add_widget(add_button)

    @staticmethod
    def delete_button_function(button_number):
        Logger.debug("opening the delete popup for number:", button_number)
        Factory.DeletePopup(button_number).open()
        return

    @staticmethod
    def modify_button_function(button_number):
        Logger.debug("loading a login to modify:", button_number)
        Factory.ModifyPopup(button_number).open()
        return

    @staticmethod
    def get_standard_button(txt, x, y, btnid, release, *args):
        return Button(text=txt, color=(0, 0, 0, 1), size_hint=(0.13, 0.06), pos_hint={"x": x, "y": y},
                      font_size=16, on_release=lambda z: release(*args), id=btnid)
