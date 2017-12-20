import kivy
import os
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from Crypto.Cipher import AES
# noinspection PyUnresolvedReferences
from secret import private_key

kivy.require("1.10.0")

Window.clearcolor = (1, 1, 1, 1)

"""UI:
button that opens a popup for adding a website config
browser website username password additional-options
"""


class Popup1(ModalView):

    def load_input(self):
        print("HGJGHJFTJFH")
        user_info = open("userInfo.dat", "rb")
        password_info = open("password.bin", "rb")
        website = user_info.readline()
        username = user_info.readline()
        arguments = user_info.readline()

        nonce, tag, ciphertext = [password_info.read(x) for x in (16, 16, -1)]
        cipher = AES.new(private_key, AES.MODE_EAX, nonce)
        password = cipher.decrypt_and_verify(ciphertext, tag)

        # splice off newlines at the end of all except password, which does not have one
        self.ids.website_input.text = website[:-1]
        self.ids.user_input.text = username[:-1]
        self.ids.password_input.text = password
        self.ids.arguments_input.text = arguments[:-1]
        self.open()
        pass

    def save_input(self):
        # this function does the following:
        # write user input in website, username, password, and arguments to a file
        # encrypt the password using AES encryption before writing it to the file
        # hide the add button and replace it with a modify button
        # modify the label nearby to show the website being entered
        user_info = open("userInfo.dat", "wb")
        password_file = open("password.bin", "wb")

        # turn all input into byte arrays instead of strings
        website = self.ids.website_input.text.encode()
        username = self.ids.user_input.text.encode()
        password = self.ids.password_input.text.encode()
        arguments = self.ids.arguments_input.text.encode()
        encoder = AES.new(private_key, AES.MODE_EAX)
        encrypted_pw, tag = encoder.encrypt_and_digest(password)
        [password_file.write(x) for x in (encoder.nonce, tag, encrypted_pw)]
        user_info.write(website)
        user_info.write(b"\n")
        user_info.write(username)
        user_info.write(b"\n")
        user_info.write(arguments)
        user_info.write(b"\n|\n")
        user_info.close()
        root_ids = App.get_running_app().root.ids
        root_ids.layout.remove_widget(root_ids.add_button)
        self.dismiss()

    # using the given integer, delete the lines of the file for the info
    def delete_info(self, number):
        pass


class Menu(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        modify_button = Button(text="Modify", color=(0, 0, 0, 1), size_hint=(0.13, 0.06),
                               pos_hint={"x": 0.05, "y": 0.8}, font_size=16,
                               on_release=lambda x: Factory.Popup1().load_input())
        self.add_widget(modify_button)
        user_info = open("userInfo.dat", "rb")
        # file containing user's information is empty, so add the first add button
        if os.stat(user_info.name).st_size == 0:
            add_button = Button(text="Add", color=(0, 0, 0, 1), size_hint=(0.13, 0.06),
                                pos_hint={"x": 0.05, "y": 0.8}, font_size=16,
                                on_release=lambda x: Factory.Popup1().open())
            self.add_widget(add_button)
        else:
            logins = 0
            # search for | delimiter to see how many different logins the user has
            for line in user_info:
                if b"|" in line:
                    delete_button = Button(text="Delete", color=(0, 0, 0, 1), size_hint=(0.13, 0.06),
                                           pos_hint={"x": 0.2, "y": 0.8 - (0.1 * logins)}, font_size=16,
                                           on_release=lambda x: Factory.Popup1().delete_info(logins))
                    self.add_widget(delete_button)
                    logins += 1

            add_button = Button(text="Add", color=(0, 0, 0, 1), size_hint=(0.13, 0.06),
                                pos_hint={"x": 0.05, "y": 0.8 - (0.1 * logins)}, font_size=16,
                                on_release=lambda x: Factory.Popup1().open())
            self.add_widget(add_button)


class AutomaticBrowserLogin(App):
    def build(self):
        return Menu()


if __name__ == "__main__":
    AutomaticBrowserLogin().run()
