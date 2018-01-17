import kivy
import os
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from Crypto.Cipher import AES
# noinspection PyUnresolvedReferences
from secret import private_key
from startup import run_autologin

kivy.require("1.10.0")

Window.clearcolor = (1, 1, 1, 1)

"""UI:
website username password browser additional-options

TODO:


Bugs:


Features to add:
test button that runs everything
password for the main program, as a sort of master password

username file has this format:
Pipe(|)+\n, website+\n, username+\n, browser+\n arguments+\n, Pipe, repeat

Password file has this format:
Pipe (|), nonce, tag, ciphertext, Pipe, repeat
"""

# global variable used to determine which login is being looked at
# definitely not the best way to do it, but it works
login_number = 0

# another global variable that keeps track of how many logins the user currently has
logins = 0

# global variable to check if modifying or adding
is_modify = False

is_delete = False


class AddOrModifyPopup(ModalView):
    def load_input(self):
        global login_number
        print("number:", login_number)
        user_info = open("userInfo.dat", "rb")
        password_file = open("password.bin", "rb")
        login_original = login_number

        # find the beginning line to read information from
        for line in user_info:
            if b"|" in line:
                login_number -= 1
                if login_number < 0:
                    break
        website = user_info.readline()
        username = user_info.readline()
        # For some reason, 1 needs to be added. Don't ask me why, I'm too lazy to fix it.
        browser = int(user_info.readline()) + 1
        arguments = user_info.readline()
        login_number = login_original

        while True:
            if password_file.read(1) == b"|":
                login_number -= 1
                if login_number < 0:
                    break
        login_number = login_original
        nonce, tag, cipher_text = [password_file.read(x) for x in (16, 16, -1)]
        if cipher_text.find(b"|") != -1:  # last password, do not remove anything from the end
            cipher_text = cipher_text[:cipher_text.find(b"|")]  # get rid of pipe and everything after
        print("nonce, tag, cipher_text:", nonce, '\n', tag, '\n', cipher_text, '\n')
        cipher = AES.new(private_key, AES.MODE_EAX, nonce)
        password = cipher.decrypt_and_verify(cipher_text, tag)

        # splice off newlines at the end of all except password, which does not have one
        self.ids.website_input.text = website[:-1]
        self.ids.user_input.text = username[:-1]
        self.ids.password_input.text = password
        index = 0
        for child in self.children[0].children:
            print("child:", child)
            if type(child) != ToggleButton:
                continue
            elif child.group == "browser_selection":
                index += 1
                if index == browser:
                    child.state = "down"
                    print("newchild:", child)
        # the two lines below do not work because they use pass by value, which doesn't actually change anything
        # print(ToggleButton.get_widgets("browser_selection")[browser])
        # ToggleButton.get_widgets("browser_selection")[browser].state = "down"
        self.ids.arguments_input.text = arguments[:-1]
        self.open()
        user_info.close()
        password_file.close()
        pass

    def save_input(self):
        # this function does the following:
        # write user input in website, username, password, and arguments to a file
        # encrypt the password using AES encryption before writing it to the file
        # hide the add button and replace it with a modify button
        # modify the label nearby to show the website being entered
        global login_number
        global logins
        global is_modify
        user_info = open("userInfo.dat", "ab")
        password_file = open("password.bin", "ab")

        # turn all input into byte arrays instead of strings
        website = self.ids.website_input.text.encode()
        username = self.ids.user_input.text.encode()
        password = self.ids.password_input.text.encode()
        # result is saved as a list with one element, so we access the first and only element at [0]
        browser = str([index for index, button in enumerate(ToggleButton.get_widgets("browser_selection"))
                      if button.state == "down"][0] % 4).encode()
        print(browser)
        """for index, button in enumerate(ToggleButton.get_widgets("browser_selection")):
            if button.state == "down":
                browser = bytearray(index)
                break"""
        arguments = self.ids.arguments_input.text.encode()
        encoder = AES.new(private_key, AES.MODE_EAX)

        # delete to make space for new, login_number is already set
        if is_modify:
            delete_info()
        # anything stored in a file cannot have a | as it is used
        # as a delimiter, so these lines of code generate
        # a new password if a | is found in anything that would otherwise be written to the file
        while encoder.nonce.find(b"|") != -1:
            encoder = AES.new(private_key, AES.MODE_EAX)
        encrypted_pw, tag = encoder.encrypt_and_digest(password)
        while encrypted_pw.find(b"|") != -1 or tag.find(b"|") != -1:
            print("| found, making a new encoder and encrypted password")
            encoder = AES.new(private_key, AES.MODE_EAX)
            while encoder.nonce.find(b"|") != -1:
                encoder = AES.new(private_key, AES.MODE_EAX)
            encrypted_pw, tag = encoder.encrypt_and_digest(password)  # generate encrypted text without pipe |
        # delete_info has temporarily removed one login, so we need to check for one less
        if not is_modify or login_number - 1 != logins:
            password_file.write(b"|")
        [password_file.write(x) for x in (encoder.nonce, tag, encrypted_pw)]
        print("written to password file:")
        [print(x) for x in (encoder.nonce, tag, encrypted_pw)]
        password_file.close()
        user_info.write(b"|\n")
        user_info.write(website)
        user_info.write(b"\n")
        user_info.write(username)
        user_info.write(b"\n")
        user_info.write(browser)
        user_info.write(b"\n")
        user_info.write(arguments)
        user_info.write(b"\n")
        user_info.close()
        app_root = App.get_running_app().root
        # app_root_children = app_root.children
        # there will only ever be one add button, and it will have the id of add_button
        """for child in app_root_children:
            if child.id == "add_button":
                app_root.remove_widget(child)
            # if child.id == "website_label" + str(login_number) and is_modify:
            #     app_root.remove_widget(child)"""
        """global logins
        if not is_modify:
            delete_button = get_standard_button("Delete", 0.2, 0.8 - (0.1 * logins), "delete_button" + str(logins),
                                                delete_button_function, logins)
            app_root.add_widget(delete_button)
            logins += 1
            modify_button = get_standard_button("Modify", 0.05, 0.9 - (0.1 * logins), "modify_button" + str(logins),
                                                modify_function_button, logins - 1)
            app_root.add_widget(modify_button)
            add_button = get_standard_button("Add", 0.05, 0.8 - (0.1 * logins), "add_button",
                                             Factory.AddOrModifyPopup().open)
            app_root.add_widget(add_button)"""
        """info_label = Label(text="website: " + str(website)[2:-1], font_size=24,
                               pos_hint={"x": 0.5, "y": 0.9 - (0.1 * logins)},
                               size_hint=(0.4, 0.05), color=(0, 0, 0, 1), id="website_label" + str(logins))
            app_root.add_widget(info_label)"""
        """else:
            info_label = Label(text="website: " + str(website)[2:-1], font_size=24,
                               pos_hint={"x": 0.5, "y": 0.9 - (0.1 * logins)},
                               size_hint=(0.4, 0.05), color=(0, 0, 0, 1), id="website_label" + str(logins))
            app_root.add_widget(info_label)"""
        fix_password_file()
        is_modify = False
        refresh_screen(app_root)
        self.dismiss()


class DeletePopup(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def delete_info_btn(self):
        delete_info()
        self.dismiss()


def delete_info():
    global login_number
    global logins
    global is_delete
    print("number:", login_number)
    user_info = open("userInfo.dat", "rb")
    password_file = open("password.bin", "rb")
    temp = open("temp.dat", "wb+")
    # noinspection PyUnusedLocal
    delete_begin = 0
    delete_original = login_number
    not_eof_flag = True
    # find the beginning and end of the information to delete
    for line in user_info:
        if b"|" in line:
            login_number -= 1
            if login_number < 0:
                delete_begin = user_info.tell()
                break

    # reset position of user_info file
    user_info.seek(0)
    # go through again, writing to a temp file and overriding the original file
    for line in user_info:
        leave = False
        if user_info.tell() == delete_begin:
            for _ in range(0, 5):
                read_line = user_info.readline()
                print("skipline", read_line)  # discard five lines
                if read_line == b"":  # EOF
                    leave = True
                    break
        if leave:
            break
        print("line:", line)
        temp.write(line)

    user_info.close()
    user_info = open("userInfo.dat", "wb")
    login_number = delete_original

    temp.seek(0)
    for line in temp:
        print("user_info line:", line)
        user_info.write(line)
    temp.close()
    temp = open("temp.dat", "wb+")
    while True:
        file_char = password_file.read(1)
        if file_char == b"|":
            login_number -= 1
            if login_number < 0:
                temp.write(file_char)  # need to keep one |, the other is excluded further down
                break
        temp.write(file_char)
    # skip until a pipe is found
    while True:
        file_char = password_file.read(1)
        if file_char == b"":  # check for EOF
            not_eof_flag = False
            break
        if file_char == b"|":  # not written here
            break
    if not_eof_flag:
        temp.write(password_file.read())
    login_number = delete_original
    user_info.close()
    password_file.close()
    temp.seek(0)
    # special case: if the last login is being deleted (logins == 0), then an extra | delimiter would be added
    # for both files, so both files are completely deleted below
    if logins != 0:
        password_file = open("password.bin", "wb")
        password_file.write(temp.read())
        password_file.close()
        temp.close()
    else:
        # open and close both in write mode, which replaces the contents with nothing
        user_info = open("userInfo.dat", "wb")
        password_file = open("password.bin", "wb")
        user_info.close()
        password_file.close()

    # remove/add GUI buttons
    app_root = App.get_running_app().root
    """app_root_children = app_root.children
    # there will only ever be one add button, and it will have the id of add_button
    if not is_modify:
        for index, child in enumerate(app_root_children):
            if child.id == "add_button":
                app_root.remove_widget(child)
                child = app_root_children[index]  # reset index, otherwise the buttons may be skipped
            if child.id == "modify_button" + str(delete_original):
                app_root.remove_widget(child)
                child = app_root_children[index]
            if child.id == "delete_button" + str(delete_original):
                app_root.remove_widget(child)"""

    """for child in app_root_children:  # shift all buttons below the deleted ones up 0.1y and adjust their ids
            if child.id is None:
                continue
            id_number = child.id[-1:]
            btn_id = child.id[:-1]
            if not id_number.isdigit():
                continue
            if int(id_number) > delete_original:
                # shift buttons up one, adjust ids appropriately, update the functions for each button
                # this creates a new button with updated parameters and deletes the old one
                if btn_id == "modify_button":
                    button = get_standard_button(child.text, child.pos_hint["x"], child.pos_hint["y"] + 0.1,
                                                 btn_id + str(int(id_number) - 1), modify_function_button,
                                                 int(id_number) - 1)
                elif btn_id == "delete_button":
                    button = get_standard_button(child.text, child.pos_hint["x"], child.pos_hint["y"] + 0.1,
                                                 btn_id + str(int(id_number) - 1), delete_button_function,
                                                 int(id_number) - 1)
                else:
                    print("WHAT HAVE YOU DONE!?!?! Congratulations, you broke the program. This should never happen™!")
                    print(child)
                    continue
                app_root.remove_widget(child)
                app_root.add_widget(button)
        add_button = get_standard_button("Add", 0.05, 0.9 - (0.1 * logins), "add_button",
                                         Factory.AddOrModifyPopup().open)
        app_root.add_widget(add_button)"""
    refresh_screen(app_root)
    fix_password_file()
    is_delete = False
    login_number = delete_original
    logins -= 1


class Menu(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        refresh_screen(self)

    @staticmethod
    def run():
        run_autologin()


def refresh_screen(app_root):
    # iterate through the list of buttons on the main screen and delete
    # a for loop is not used because it deletes a button and a new one takes its place, but the for loop
    # iterates to the next one on its own, and some buttons are skipped
    while app_root.children[0].id is not None:
        app_root.remove_widget(app_root.children[0])
    user_info = open("userInfo.dat", "rb")
    print("user_info:", user_info.read())
    user_info.seek(0)
    # if file containing user's information is empty, add the first add button
    if os.stat(user_info.name).st_size == 0:
        add_button = get_standard_button("Add", 0.05, 0.8, "add_button", Factory.AddOrModifyPopup().open)
        app_root.add_widget(add_button)
    else:
        global logins
        logins = 0
        # search for | delimiter to see how many different logins the user has
        for line in user_info:
            if b"|" in line:
                delete_button = get_standard_button("Delete", 0.2, 0.8 - (0.1 * logins),
                                                    "delete_button" + str(logins), delete_button_function, logins)
                app_root.add_widget(delete_button)
                modify_button = get_standard_button("Modify", 0.05, 0.8 - (0.1 * logins), "modify_button" +
                                                    str(logins), modify_function_button, logins)
                app_root.add_widget(modify_button)
                website_label = Label(text="Website: " + str(user_info.readline())[2:-3], size_hint=(0.5, 0.13),
                                      pos_hint={"x": 0.4, "y": 0.8 - (0.1 * logins)}, font_size=24, color=(0, 0, 0, 1),
                                      id="Label" + str(logins))
                app_root.add_widget(website_label)
                logins += 1

        add_button = get_standard_button("Add", 0.05, 0.8 - (0.1 * logins),
                                         "add_button", Factory.AddOrModifyPopup().open)
        app_root.add_widget(add_button)


# if the password file has two pipes || next to each other, then this is clearly an error and one of the pipes should
# be removed
def fix_password_file():
    password_file = open("password.bin", "rb")
    temp = open("temp.dat", "wb")
    while True:
        file_char = password_file.read(1)
        if file_char == b"|":
            # skip one character
            next_char = password_file.read(1)
            if next_char != b"|":
                temp.write(next_char)
            # else, do nothing, as the password file's file location has been moved one further
            else:
                print("Password file contained a buggy result and has been fixed. This is rare, and there may be a"
                      "serious bug in the program if you see this!")
        if file_char == b"":  # EOF
            break
        temp.write(file_char)


class AutomaticBrowserLogin(App):
    def build(self):
        self.icon = "Icon.png"
        return Menu()


def delete_button_function(button_number):
    print(button_number)
    global login_number
    global is_delete
    if not is_modify:
        is_delete = True
    login_number = button_number
    Factory.DeletePopup().open()
    return


def modify_function_button(button_number):
    global is_modify
    global login_number
    is_modify = True
    login_number = button_number
    Factory.AddOrModifyPopup().load_input()
    return


def get_standard_button(txt, x, y, btnid, release, *args):
    return Button(text=txt, color=(0, 0, 0, 1), size_hint=(0.13, 0.06), pos_hint={"x": x, "y": y},
                  font_size=16, on_release=lambda z: release(*args), id=btnid)


if __name__ == "__main__":
    AutomaticBrowserLogin().run()
