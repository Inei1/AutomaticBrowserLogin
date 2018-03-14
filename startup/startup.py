import os
from time import sleep

from kivy.app import App
from selenium import webdriver
import selenium.webdriver.chrome.options
import selenium.webdriver.firefox.options
import selenium.webdriver.edge.options
from Crypto.Cipher import AES
# noinspection PyUnresolvedReferences
from secret import private_key

# command line arguments
# Firefox: https://developer.mozilla.org/en-US/docs/Mozilla/Command_Line_Options
# Chrome: https://peter.sh/experiments/chromium-command-line-switches/
# Edge: unknown

# web driver downloads: http://www.seleniumhq.org/download/  scroll down


"""
TODO:
documentation
make user info work

For post-release:
add functionality for firefox/IE/edge
implement arguments functionality
clean up code
"""


class Startup:
    def __init__(self):
        self.browser = None
        self.driver = None
        skip_options = False
        options = ""
        try:
            options = open("options.dat", "r")
        except:
            skip_options = True
        if not skip_options:
            self.browser = int(options.readline())
            arguments = options.readline()[:-1]  # splice newline off end of line
            print("arguments:", arguments, "\nbrowser:", self.browser)
        # firefox_arguments = arguments.readline()[:-1]
        # edge_arguments = arguments.readline()[:-1]
        # TODO make function for below
        # forward slashes are needed because shlex.split() performed by webbrowser only recognizes / and not \
        appdata_dir = os.getenv("APPDATA")
        appdata_dir = appdata_dir.replace("\\", "/") + "/"
        self.chrome_driver_path = appdata_dir + "AutomaticBrowserLogin/WebDrivers/chromedriver_win32/chromedriver.exe"
        self.firefox_driver_path = appdata_dir + "AutomaticBrowserLogin/WebDrivers/geckodriver-v0.19.1-win64/" \
                                                 "geckodriver.exe"
        self.edge_driver_path = appdata_dir + "AutomaticBrowserLogin/WebDrivers/MicrosoftWebDriver"
        os.environ["webdriver.chrome.driver"] = self.chrome_driver_path
        # need to have these long chains because Options() is the same name across all drivers
        self.chrome_options = selenium.webdriver.chrome.options.Options()
        self.firefox_options = selenium.webdriver.firefox.options.Options()
        # self.edge_options = selenium.webdriver.edge.options.Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument("disable-infobars")
        # TODO fix lazy try-except
        try:
            self.chrome_options.add_argument(arguments)
            # self.firefox_options.add_argument(arguments)
        except:
            pass
        # causes to not work if browser already open
        appdata_local_dir = os.getenv("LOCALAPPDATA")
        appdata_local_dir = appdata_local_dir.replace("\\", "/") + "/"
        self.chrome_options.add_argument("user-data-dir=" + appdata_local_dir + "Google/Chrome/User Data")

        self.chrome_driver = webdriver.Chrome(executable_path=self.chrome_driver_path,
                                              chrome_options=self.chrome_options)
        # self.firefox_driver = webdriver.Firefox(executable_path=self.firefox_driver_path,
        #                                        firefox_options=self.firefox_options)
        # self.edge_driver = webdriver.Edge(self.edge_driver_path)  # no options for edge
        # self.edge_driver.close()
        # self.driver.set_page_load_timeout(60)

    def open_new(self, url, payload):
        if self.browser == 0:
            self.driver = self.chrome_driver
        elif self.browser == 1:
            pass  # self.driver = self.firefox_driver
        elif self.browser == 3:
            pass  # self.driver = self.edge_driver
        elif self.browser == -1:
            return
        print("first:", self.driver.current_window_handle)
        print("url:", str(url)[2:-3])
        self.driver.execute_script("window.open('%s')" % str(url)[2:-3])
        self.switch_to_new_tab()
        self.wait_for_load()
        print(payload)
        if payload["username"] == b"\n" and payload["password"] == b"":
            return  # no username or password, open tab but do not input any information
        print(str(payload["username"])[2:-3], str(payload["password"])[2:-1])
        user = self.driver.find_element_by_xpath("//input[contains(@name, 'ser') or contains(@name, 'email') "
                                                 "or contains(@name, 'login')]")
        user.send_keys(str(payload["username"])[2:-3])
        # yahoo and google logins ask for your info one at a time
        submit = True
        if self.driver.title.__contains__("Yahoo") or self.driver.title.__contains__("Google"):
            user.submit()
            submit = False
            self.wait_for_load()
        # canvas does not work properly with submit
        if self.driver.current_url.__contains__(".edu/idp"):
            submit = False
        password = self.driver.find_element_by_xpath("//input[contains(@name, 'ass') or contains(@name, 'pw')]"
                                                     "[not(@type='hidden')]")
        password.send_keys(str(payload["password"])[2:-1])
        if submit:
            user.submit()
        return

    def switch_to_new_tab(self):
        handles = self.driver.window_handles
        current_handle = self.driver.current_window_handle
        for handle in handles:
            if not handle == current_handle:
                self.driver.switch_to.window(handle)
                print(self.driver.window_handles, self.driver.current_window_handle)

    def wait_for_load(self):
        while str(self.driver.execute_script("return document.readyState")) != "complete":
            sleep(1)
        return

    def run(self):
        try:
            user_info = open("userInfo.dat", "rb")
            password_file = open("password.bin", "rb")
        except:
            return
        user_info.readline()  # discard pipe (|)
        for index, line in enumerate(user_info):
            # index_original = index
            password_file.seek(0)
            print("line", line, "index", index)
            url = line
            username = user_info.readline()
            # arguments = user_info.readline()
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
            self.open_new(url, payload)

        # close first tab
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        App.get_running_app().stop()
        # if self.driver != self.firefox_driver:
        #    self.firefox_driver.close()
        # elif self.driver != self.chrome_driver:
        #    self.chrome_driver.close()


def run_autologin():
    print("program running")
    s = Startup()
    s.run()

if __name__ == "__main__":
    run_autologin()
