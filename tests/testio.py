from automaticbrowserlogin import user_info_test_directory
from automaticbrowserlogin.ui.popupio import PopupIO

import json
import os
import unittest


class TestPopupIO(unittest.TestCase):
    """
    Tests for the PopupIO class.
    """
    def setUp(self):
        self.user_info_line_1 = {"website": "https://example.com", "username": "testuser", "password": "testpass"}
        self.user_info_line_2 = {"website": "https://github.com/login", "username": "fakeuser",
                                 "password": "fakepassword"}
        self.user_info_line_3 = {"website": "website", "username": "user", "password": "pass"}
        self.reload_user_info()
        self.io_1 = PopupIO(0, user_info_test_directory)
        self.io_2 = PopupIO(1, user_info_test_directory)
        self.io_3 = PopupIO(2, user_info_test_directory)

    def reload_user_info(self):
        self.user_info = open(user_info_test_directory, "w")
        json.dump(self.user_info_line_1, self.user_info)
        self.user_info.write("\n")
        json.dump(self.user_info_line_2, self.user_info)
        self.user_info.write("\n")
        self.user_info.close()
        self.user_info = open(user_info_test_directory, "r")

    def tearDown(self):
        self.user_info.close()
        os.remove(user_info_test_directory)

    def test_load_login_unencrypted(self):
        self.reload_user_info()
        website, username, password = self.io_1.load_login(encrypted=False)
        self.assertEqual(website, "https://example.com")
        self.assertEqual(username, "testuser")
        self.assertEqual(password, "testpass")

    def test_add_login_unencrypted(self):
        self.reload_user_info()

        self.io_3.save_login("website", "user", "pass", encrypted=False)
        self.assertEqual(json.loads(self.user_info.readline()), self.user_info_line_1)
        self.assertEqual(json.loads(self.user_info.readline()), self.user_info_line_2)
        self.assertEqual(json.loads(self.user_info.readline()), self.user_info_line_3)

    def test_add_login_encrypted(self):
        self.reload_user_info()
        self.io_3.save_login("website", "user", b"pass")
        self.user_info.readline()
        self.user_info.readline()
        user_info_pw_encrypted = json.loads(self.user_info.readline())
        self.assertEqual(user_info_pw_encrypted.get("website"), "website")
        self.assertEqual(user_info_pw_encrypted.get("username"), "user")
        self.assertNotEqual(user_info_pw_encrypted.get("password"), "pass")

    def test_add_and_load_login_encrypted(self):
        self.reload_user_info()
        self.io_3.save_login("website", "user", b"pass")
        website, username, password = self.io_3.load_login()
        self.assertEqual(password, b"pass")

    def test_delete_login(self):
        self.reload_user_info()
        self.io_2.delete_login()
        self.assertEqual(json.loads(self.user_info.readline()), self.user_info_line_1)
        self.reload_user_info()
        self.io_1.delete_login()
        self.assertEqual(json.loads(self.user_info.readline()), self.user_info_line_2)

    def test_modify_login(self):
        self.reload_user_info()
        self.io_2.delete_login()
        self.io_2.save_login("website", "user", b"pass")
        self.assertEqual(json.loads(self.user_info.readline()), self.user_info_line_1)
        login = json.loads(self.user_info.readline())
        self.assertEqual(login.get("website"), "website")
        self.assertEqual(login.get("username"), "user")
        self.assertNotEqual(login.get("password"), "pass")

    def test_modify_middle_encrypted(self):
        self.reload_user_info()
        self.io_3.save_login("website", "user", b"pass")
        self.io_2.delete_login()
        self.io_2.save_login("https://github.com/login", "fakeuser", b"fakepass")
        website, username, password = self.io_1.load_login(encrypted=False)
        self.assertEqual(password, "testpass")
        website, username, password = self.io_2.load_login()
        self.assertEqual(password, b"pass")
        website, username, password = self.io_3.load_login()
        self.assertEqual(password, b"fakepass")


if __name__ == "__main__":
    unittest.main()
