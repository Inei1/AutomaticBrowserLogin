from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
        # forward slashes are needed because shlex.split() performed by webbrowser only recognizes / and not \
        url = "chrome://newtab"
        payload = {"user": "nerd951", "passwd": "RHitN77"}
        # self.driver.execute_script("window.open('chrome://newtab', 'tab2')")
        # self.driver.switch_to.window("tab2")
        # self.driver.get(url2)

if __name__ == "__main__":
    s = Startup()
    s.run()
