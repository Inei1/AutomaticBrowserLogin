from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Crypto.Cipher import AES
# noinspection PyUnresolvedReferences
from secret import private_key

# IE command line arguments: https://msdn.microsoft.com/en-us/library/hh826025(v=vs.85).aspx
# Firefox: https://developer.mozilla.org/en-US/docs/Mozilla/Command_Line_Options
# Chrome: https://peter.sh/experiments/chromium-command-line-switches/
# Edge: unknown


class Startup:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, chrome_options=self.options)
        self.chrome_driver_path = "D:/Users/PCUser4/Desktop/School/chromedriver_win32/chromedriver"
        self.options = Options()

    def open_new_browser_window(self, url, payload):
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--incognito")
        self.options.add_argument("user-data-dir=C:/Users/PCUser4/AppData/Local/Google/Chrome/User Data")
        self.options.add_experimental_option("detach", True)
        self.driver.get(url)
        user = self.driver.find_element_by_name("user")
        user.send_keys(payload[0])
        passwd = self.driver.find_element_by_name("passwd")
        passwd.send_keys(payload[1])
        user.submit()

    def run(self):
        user_info = open("userInfo.dat", "rb")
        password_file = open("password.bin", "rb")
        for line in user_info:
            url = line
            username = user_info.readline()
            # TODO refactor duplicate code
            nonce, tag, cipher_text = [password_file.read(x) for x in (16, 16, -1)]
            if cipher_text.find(b"|") != -1:  # last password, do not remove anything from the end
                cipher_text = cipher_text[:cipher_text.find(b"|")]  # get rid of pipe and everything after
            print("nonce, tag, cipher_text:", nonce, '\n', tag, '\n', cipher_text, '\n')
            cipher = AES.new(private_key, AES.MODE_EAX, nonce)
            password = cipher.decrypt_and_verify(cipher_text, tag)

        # forward slashes are needed because shlex.split() performed by webbrowser only recognizes / and not \
        url = "chrome://newtab"
        payload = {"user": "nerd951", "passwd": "RHitN77"}
        # self.driver.execute_script("window.open('chrome://newtab', 'tab2')")
        # self.driver.switch_to.window("tab2")
        # self.driver.get(url2)


def run_autologin():
    s = Startup()
    s.run()

if __name__ == "__main__":
    run_autologin()
