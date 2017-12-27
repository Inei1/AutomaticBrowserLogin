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

Features to add:
password for the main program, as a sort of master password

TODO:
Fix password implementation, currently does not work and would only give the same password for all if it does.
fix modify button not being created when clicking add on the first button at startup for buttons other than the first
make delete button remove the GUI buttons when clicked
add labels to show the website on the right of the buttons so the user does not have to go into each modify button
Write actual script for automatic logging in (startup.py, should be fairly easy)
"""

# global variable used to determine which login to delete
# definitely not the best way to do it, but it works
delete_number = 0

# another global variable that keeps track of how many logins the user currently has
logins = 0


class AddOrModifyPopup(ModalView):

    def load_input(self):
        print("HGJGHJFTJFH")
        user_info = open("userInfo.dat", "rb")
        password_info = open("password.bin", "rb")
        website = user_info.readline()
        username = user_info.readline()
        arguments = user_info.readline()

        password_info.seek(1)
        nonce, tag, cipher_text = [password_info.read(x) for x in (16, 16, -1)]
        print(nonce, tag, cipher_text)
        cipher = AES.new(private_key, AES.MODE_EAX, nonce)
        password = cipher.decrypt_and_verify(cipher_text, tag)

        # splice off newlines at the end of all except password, which does not need one
        self.ids.website_input.text = website[:-1]
        self.ids.user_input.text = username[:-1]
        self.ids.password_input.text = password
        self.ids.arguments_input.text = arguments[:-1]
        self.open()
        user_info.close()
        password_info.close()
        pass

    def save_input(self):
        # this function does the following:
        # write user input in website, username, password, and arguments to a file
        # encrypt the password using AES encryption before writing it to the file
        # hide the add button and replace it with a modify button
        # modify the label nearby to show the website being entered
        user_info = open("userInfo.dat", "ab")
        password_file = open("password.bin", "ab")

        # turn all input into byte arrays instead of strings
        website = self.ids.website_input.text.encode()
        username = self.ids.user_input.text.encode()
        password = self.ids.password_input.text.encode()
        arguments = self.ids.arguments_input.text.encode()
        encoder = AES.new(private_key, AES.MODE_EAX)
        encrypted_pw, tag = encoder.encrypt_and_digest(password)
        password_file.write(b"\n")
        [password_file.write(x) for x in (encoder.nonce, tag, encrypted_pw)]
        password_file.close()
        user_info.write(website)
        user_info.write(b"\n")
        user_info.write(username)
        user_info.write(b"\n")
        user_info.write(arguments)
        user_info.write(b"\n|\n")
        user_info.close()
        app_root = App.get_running_app().root
        app_root_children = app_root.children
        # there will only ever be one add button, and it will have the id of add_button
        for child in app_root_children:
            if child.id == "add_button":
                app_root.remove_widget(child)
        global logins
        delete_button = get_standard_button("Delete", 0.2, 0.8 - (0.1 * logins), "delete_button" + str(logins),
                                            delete_button_function, logins)
        app_root.add_widget(delete_button)
        logins += 1
        modify_button = get_standard_button("Modify", 0.05, 0.8 - (0.1 * logins), "modify_button" + str(logins),
                                            Factory.AddOrModifyPopup().load_input)
        app_root.add_widget(modify_button)
        add_button = get_standard_button("Add", 0.05, 0.8 - (0.1 * logins), "add_button",
                                         Factory.AddOrModifyPopup().open)
        app_root.add_widget(add_button)
        self.dismiss()


class DeletePopup(ModalView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # using the given integer, delete the lines of the file for the info
    def delete_info(self):
        global delete_number
        print("number:", delete_number)
        user_info = open("userInfo.dat", "rb")
        # password_file = open("password.bin", "rb")
        temp = open("temp.dat", "wb+")
        delete_begin = 0
        delete_end = 0
        delete_original = delete_number
        # find the beginning and end of the information to delete
        delete_begin = user_info.tell() + 1  # the delete beginning is going to be +1 if this is the first login
        for line in user_info:
            if b"|" in line:
                delete_number -= 1
                if delete_number < 0:
                    delete_end = user_info.tell()
                    break
                delete_begin = user_info.tell()
        # reset position of user_info file
        user_info.seek(0)
        # go through again, writing to a temp file and overriding the original file
        for line in user_info:
            if user_info.tell() == delete_begin:
                while user_info.tell() != delete_end:
                    user_info.readline()  # discard line
            temp.write(line)

        user_info.close()
        user_info = open("userInfo.dat", "wb")

        temp.seek(0)
        for line in temp:
            print(line)
            user_info.write(line)
        temp.close()
        temp = open("temp.dat", "wb+")
        """for line in password_file:
            print(line)
            temp.write(line)
            delete_original -= 1
            if delete_original < 0:
                password_file.readline()  # discard line"""
        """for pw in [password_file.read(x) for x in (16, 16, -1)]:
            print(pw)
            temp.write(line)
            delete_original -= 1
            if delete_original < 0:
                [password_file.read(x) for x in (16, 16, -1)]  # discard"""
        user_info.close()
        # password_file.close()
        temp.close()
        self.dismiss()


class Menu(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        modify_button = get_standard_button("Modify", 0.05, 0.8, "modify_button", Factory.AddOrModifyPopup().load_input)
        # Button(text="Modify", color=(0, 0, 0, 1), size_hint=(0.13, 0.06),
        #                       pos_hint={"x": 0.05, "y": 0.8}, font_size=16,
        #                       on_release=lambda x: Factory.AddOrModifyPopup().load_input())
        self.add_widget(modify_button)
        user_info = open("userInfo.dat", "rb")
        # if file containing user's information is empty, add the first add button
        if os.stat(user_info.name).st_size == 0:
            add_button = get_standard_button("Add", 0.05, 0.8, "add_button", Factory.AddOrModifyPopup().open)
            # Button(text="Add", color=(0, 0, 0, 1), size_hint=(0.13, 0.06),
            #                    pos_hint={"x": 0.05, "y": 0.8}, font_size=16,
            #                    on_release=lambda x: Factory.AddOrModifyPopup().open(),
            #                    id="add_button")
            self.add_widget(add_button)
        else:
            global logins
            # search for | delimiter to see how many different logins the user has
            for line in user_info:
                if b"|" in line:
                    delete_button = get_standard_button("Delete", 0.2, 0.8 - (0.1 * logins),
                                                        "delete_button" + str(logins), delete_button_function, logins)
                    self.add_widget(delete_button)
                    modify_button = get_standard_button("Modify", 0.05, 0.8 - (0.1 * logins), "modify_button" +
                                                        str(logins), Factory.AddOrModifyPopup().load_input)
                    self.add_widget(modify_button)
                    logins += 1

            add_button = get_standard_button("Add", 0.05, 0.8 - (0.1 * logins),
                                             "add_button", Factory.AddOrModifyPopup().open)
            self.add_widget(add_button)


class AutomaticBrowserLogin(App):
    def build(self):
        return Menu()


def delete_button_function(button_number):
    print(button_number)
    global delete_number
    delete_number = button_number
    Factory.DeletePopup().open()
    return


def get_standard_button(txt, x, y, btnid, release, *args):
    return Button(text=txt, color=(0, 0, 0, 1), size_hint=(0.13, 0.06), pos_hint={"x": x, "y": y},
                  font_size=16, on_release=lambda z: release(*args), id=btnid)


if __name__ == "__main__":
    AutomaticBrowserLogin().run()
