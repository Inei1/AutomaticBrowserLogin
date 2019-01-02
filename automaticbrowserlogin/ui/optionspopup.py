from kivy.uix.modalview import ModalView
from kivy.uix.togglebutton import ToggleButton
from kivy.logger import Logger

from automaticbrowserlogin import options_directory

import json


class OptionsPopup(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_options()

    def load_options(self):
        try:
            options_file = open(options_directory, "r")
        except FileNotFoundError:
            Logger.warning("no options file found")
            return
        options = json.load(options_file)
        self.activate_browser_button(int(options.get("browser")))
        self.ids.args_input.text = options.get("args")
        options_file.close()

    def save_options(self):
        options_file = open(options_directory, "w")
        browser = -1
        for button in ToggleButton.get_widgets("browser_selection"):
            if button.state == "down":
                # workaround for how kivy doesn't seem to delete the old buttons when closing a popup, so
                # the old buttons are still there and the index goes over 3 and breaks everything
                if button.text == "Chrome":
                    browser = 0
                elif button.text == "Firefox":
                    browser = 1
                elif button.text == "Edge":
                    browser = 2
        args = self.ids.args_input.text
        options = {"args": args, "browser": browser}
        json.dump(options, options_file)
        options_file.close()
        self.dismiss()

    def activate_browser_button(self, browser):
        index = -1
        for child in self.children[0].children:
            if browser == -1:
                break
            if type(child) == ToggleButton and child.group == "browser_selection":
                index += 1
                if index == browser:
                    child.state = "down"
