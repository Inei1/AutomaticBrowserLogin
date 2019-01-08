from kivy.uix.modalview import ModalView
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
        self.ids.args_input.text = options.get("args")
        options_file.close()

    def save_options(self):
        options_file = open(options_directory, "w")
        args = self.ids.args_input.text
        options = {"args": args}
        json.dump(options, options_file)
        options_file.close()
        self.dismiss()
