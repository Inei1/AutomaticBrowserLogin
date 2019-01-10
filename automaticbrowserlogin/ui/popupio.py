from kivy.logger import Logger

from Crypto.Cipher import AES

from automaticbrowserlogin import user_info_directory, private_key, temp_directory

from base64 import b64encode, b64decode
import json
import shutil


class PopupIO:
    """
    Defines the functions to be used by the add/modify/delete operations.
    Options IO is handled in the options popup class.
    """
    def __init__(self, button_number, user_info_path):
        super().__init__()
        self.button_number = button_number
        self.user_info_path = user_info_path

    def delete_login(self):
        """
        delete a login from the user info file
        :return:
        """
        user_info_file = open(self.user_info_path, "rb")
        temp = open(temp_directory, "wb+")
        for i in range(0, self.button_number):
            temp.write(user_info_file.readline())
        user_info_file.readline()
        for line in user_info_file:
            temp.write(line)
        user_info_file.close()
        temp.close()
        shutil.move(temp_directory, self.user_info_path)

    def load_login(self, encrypted=True):
        """
        Load a login from the user info file.
        :param encrypted: whether or not the password must be decrypted first
        :return: a tuple containing the website, username, and password
        """
        Logger.debug("loading login")
        Logger.debug("user info directory is" + self.user_info_path)
        user_info_file = open(self.user_info_path, "rb")
        user_info_json = ""
        website = ""
        username = ""
        password = ""
        for i in range(0, self.button_number + 1):
            user_info_json = user_info_file.readline()
        if user_info_json != "":
            user_info = json.loads(user_info_json)
            Logger.debug("user info:", user_info)

            website = user_info.get("website")
            username = user_info.get("username")
            if encrypted:
                password = b64decode(user_info.get("password"))
                if password != b"":
                    nonce = password[:16]
                    tag = password[16:32]
                    cipher_text = password[32:]
                    cipher = AES.new(private_key, AES.MODE_EAX, nonce)
                    password = cipher.decrypt_and_verify(cipher_text, tag)
                else:
                    Logger.warning("no password found when loading")
                    password = b""
            else:
                password = user_info.get("password")
        user_info_file.close()
        return website, username, password

    def save_login(self, website, username, password, encrypted=True):
        """
        Write website, username, password, from UI into the user info file.
        The password is encrypted using AES encryption before writing it to the file.
        :param website: the website to go to
        :param username: the username to login to the website (may be empty)
        :param password: the password to login to the website (may be empty)
        :param encrypted: whether or not to encrypt the password
        :return: nothing
        """
        Logger.debug("saving login")
        Logger.debug("user info directory is" + self.user_info_path)
        # TODO: the user info JSON file does not follow the json standard, a new outer field should be added when
        # first creating the user_info JSON file
        user_info_file = open(self.user_info_path, "a")
        if encrypted:
            encoder = AES.new(private_key, AES.MODE_EAX)
            encrypted_pw, tag = encoder.encrypt_and_digest(password)
            Logger.debug("nonce, tag, encrypted_pw:")
            Logger.debug([x for x in (encoder.nonce, tag, encrypted_pw)])
            encrypted_password_tuple = [x for x in (encoder.nonce, tag, encrypted_pw)]
            json_password = b64encode(b"".join(encrypted_password_tuple)).decode()
        else:
            json_password = password
        Logger.debug("password written to file:")
        Logger.debug(json_password)

        login = {"website": website, "username": username, "password": json_password}
        json.dump(login, user_info_file)
        user_info_file.write("\n")
        user_info_file.close()
