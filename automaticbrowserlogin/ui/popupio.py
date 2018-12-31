import base64
import json
import logging
import shutil

from Crypto.Cipher import AES

from automaticbrowserlogin import user_info_directory, private_key, temp_directory


class PopupIO:
    def __init__(self, button_number):
        super().__init__()
        self.button_number = button_number

    def delete_login(self):
        user_info_file = open(user_info_directory, "rb")
        temp = open(temp_directory, "wb+")
        for i in range(0, self.button_number):
            temp.write(user_info_file.readline())
        user_info_file.readline()
        for line in user_info_file:
            temp.write(line)
        user_info_file.close()
        temp.close()
        shutil.move(temp_directory, user_info_directory)

    def load_input(self):
        logging.debug("loading login")
        logging.debug("user info directory is", user_info_directory)
        user_info_file = open(user_info_directory, "rb")
        user_info_json = ""
        website = ""
        username = ""
        password = ""
        for i in range(0, self.button_number + 1):
            user_info_json = user_info_file.readline()
        if user_info_json != "":
            user_info = json.loads(user_info_json)
            logging.debug("user info:", user_info)

            website = user_info.get("website")
            username = user_info.get("username")
            password = base64.b64decode(user_info.get("password"))
            if password != b"":
                nonce, tag, cipher_text = [password[x] for x in (16, 16, -1)]
                logging.debug("nonce, tag, cipher_text when loading:", nonce, '\n', tag, '\n', cipher_text, '\n')
                cipher = AES.new(private_key, AES.MODE_EAX, nonce)
                password = cipher.decrypt_and_verify(cipher_text, tag)
            else:
                logging.warning("no password found when loading")
                password = b""
        user_info_file.close()
        return website, username, password

    # write user input in website, username, password, and arguments to a file
    # encrypt the password using AES encryption before writing it to the file
    # hide the add button and replace it with a modify button
    # modify the label nearby to show the website being entered
    @staticmethod
    def save_input(website, username, password):
        logging.debug("saving login")
        logging.debug("user info directory is", user_info_directory)
        user_info_file = open(user_info_directory, "a")

        encoder = AES.new(private_key, AES.MODE_EAX)
        encrypted_pw, tag = encoder.encrypt_and_digest(password)
        logging.debug("written to password file:")
        [logging.debug(x) for x in (encoder.nonce, tag, encrypted_pw)]
        login = {"website": website, "username": username, "password": base64.b64encode(encrypted_pw).decode()}

        json.dump(login, user_info_file)
        user_info_file.write("\n")
        user_info_file.close()
