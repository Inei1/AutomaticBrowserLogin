from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Crypto.Cipher import AES
# noinspection PyUnresolvedReferences
from secret import private_key

# IE command line arguments: https://msdn.microsoft.com/en-us/library/hh826025(v=vs.85).aspx
# Firefox: https://developer.mozilla.org/en-US/docs/Mozilla/Command_Line_Options
# Chrome: https://peter.sh/experiments/chromium-command-line-switches/
# Edge: unknown


"""TODO:
add functionality for firefox/IE/edge
allow specifying a different webdriver path
implement arguments functionality
clean up code
documentation
"""


class Startup:
    def __init__(self):
        # forward slashes are needed because shlex.split() performed by webbrowser only recognizes / and not \
        self.chrome_driver_path = "D:/Users/PCUser4/Desktop/School/chromedriver_win32/chromedriver"
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("disable-infobars")
        # self.options.add_argument("user-data-dir=C:/Users/PCUser4/AppData/Local/Google/Chrome/User Data")
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, chrome_options=self.options)
        # self.driver.set_page_load_timeout(60)

    def open_new(self, url, payload, browser, index):
        # self.options.add_argument("--incognito")
        # self.driver.execute_script("window.open('chrome://newtab', 'newtab')")
        # self.driver.switch_to.window("newtab")
        # self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, chrome_options=self.options)
        # self.switch_to_new_tab()
        print("first:", self.driver.current_window_handle)
        print("url:", str(url)[2:-3])
        self.driver.execute_script("window.open('%s')" % str(url)[2:-3])
        self.switch_to_new_tab()
        # self.driver.execute_script("window.open('chrome://newtab', 'tab0')")
        # self.driver.execute_script("window.open(" + "\"" + str(url)[2:-3] + "\"" + ")")
        # self.driver.get(url)
        print(payload)
        print(str(payload["username"])[2:-3], str(payload["password"])[2:-1])
        user = self.driver.find_element_by_xpath("//input[contains(@name, 'user') or contains(@name, 'email') "
                                                 "or contains(@name, 'login')]")
        user.send_keys(str(payload["username"])[2:-3])
        password = self.driver.find_element_by_xpath("//input[contains(@name, 'pass') or contains(@name, 'pw')]")
        password.send_keys(str(payload["password"])[2:-1])
        user.submit()
        # self.switch_to_new_tab()
        # self.driver.execute_script("window.open('chrome://newtab')")
        # self.driver.execute_script("window.open('chrome://newtab', 'tab%s')" % str(index))
        # sleep(5)
        # newest_handle = ""
        # for handles in self.driver.window_handles:
        #    newest_handle = handles
        # self.driver.switch_to.window(newest_handle)
        # self.driver.execute_script("window.focus();")
        # self.driver.switch_to.window("tab" + str(index))
        # self.driver.switch_to.active_element()
        # self.driver.execute_script("window.location.replace = " + str(url)[2:-3])
        return

    def switch_to_new_tab(self):
        handles = self.driver.window_handles
        current_handle = self.driver.current_window_handle
        for handle in handles:
            if not handle == current_handle:
                self.driver.switch_to.window(handle)
                print(self.driver.window_handles, self.driver.current_window_handle)

    def run(self):
        user_info = open("userInfo.dat", "rb")
        password_file = open("password.bin", "rb")
        user_info.readline()  # discard pipe (|)
        for index, line in enumerate(user_info):
            index_original = index
            password_file.seek(0)
            print("line", line, "index", index)
            url = line
            username = user_info.readline()
            browser = user_info.readline()
            arguments = user_info.readline()
            user_info.readline()  # discard pipe (|)

            while True:
                if password_file.read(1) == b"|":
                    index -= 1
                    if index < 0:
                        break

            # TODO refactor duplicate code
            nonce, tag, cipher_text = [password_file.read(x) for x in (16, 16, -1)]
            if cipher_text.find(b"|") != -1:  # last password, do not remove anything from the end
                cipher_text = cipher_text[:cipher_text.find(b"|")]  # get rid of pipe and everything after
            print("nonce, tag, cipher_text:", nonce, '\n', tag, '\n', cipher_text, '\n')
            cipher = AES.new(private_key, AES.MODE_EAX, nonce)
            password = cipher.decrypt_and_verify(cipher_text, tag)

            payload = {"username": username, "password": password}
            # self.options.add_argument(arguments)
            self.open_new(url, payload, browser, index_original)

        # close first tab
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()


def run_autologin():
    print("program running")
    s = Startup()
    s.run()

if __name__ == "__main__":
    run_autologin()
