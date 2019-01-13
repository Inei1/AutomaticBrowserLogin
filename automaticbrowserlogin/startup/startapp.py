import io
import zipfile

from kivy.app import App
from kivy.logger import Logger

from selenium import webdriver
import selenium.webdriver.chrome.options
from selenium.webdriver.common.keys import Keys

from automaticbrowserlogin import options_directory, user_info_directory, chrome_driver_version_directory, appdata_dir
from automaticbrowserlogin.ui.popupio import PopupIO

from time import sleep
import os
import json
import requests


# TODO: add some unit tests for this class
# May need to refactor some of the functions to make better use of return values for this to be possible
class Startup:
    """
    Starting point for the Startup App.
    This does not use kivy, as it looks into the user info file to get its data,
    which means it can be run as its own app.
    """
    def __init__(self):
        self.arguments = ""
        self.driver = None
        self.load_options()
        self.setup_browser()

    def load_options(self):
        try:
            options_file = open(options_directory, "r")
        except FileNotFoundError:
            Logger.error("options file not found, unable to determine arguments")
            return
        options = json.load(options_file)
        self.arguments = options.get("args")

    def setup_browser(self):
        """
        Get the browser and WebDriver ready to open the webpages.
        The appdata directory is used to download and store the Chrome WebDriver.
        Some Chrome options are mandatory for the app to work, which are detach, disable-infobars, and user-data-dir.

        Without adding the detach option, the web browser would immediately close after opening the web pages.
        It ensures that selenium exits after opening the web pages.

        disable-infobars gets rid of the annoying message that says "chrome is being controlled by automated software."
        This does have the side effect of not showing info bars, but they seem to barely be used by Chrome in the
        first place.

        The user-data-dir option imports Chrome user data, and without this it would load up a Chrome browser with
        what is essentially a fresh install. This means that there are no bookmarks or extensions without specifying the
        user data. It is assumed that the user data is stored in Chrome's default directory.

        Also, the ChromeDriver online API is used to determine if the latest version of the ChromeDriver is installed.
        :return: nothing
        """
        driver_path = appdata_dir + "AutomaticBrowserLogin/WebDrivers/chromedriver_win32/chromedriver.exe"
        latest = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
        try:
            driver_version_file = open(chrome_driver_version_directory, "r")
            driver_version = json.load(driver_version_file)
            if not os.path.isfile(driver_path) or latest != driver_version:
                self.update_webdriver(appdata_dir, latest)
        except FileNotFoundError:
            self.update_webdriver(appdata_dir, latest)

        browser_options = webdriver.chrome.options.Options()
        os.environ["webdriver.chrome.driver"] = driver_path
        browser_options.add_experimental_option("detach", True)
        browser_options.add_argument("disable-infobars")
        if self.arguments:
            browser_options.add_argument(self.arguments)

        # causes to not work if browser already open
        appdata_local_dir = os.getenv("LOCALAPPDATA")
        appdata_local_dir = appdata_local_dir.replace("\\", "/") + "/"
        browser_options.add_argument("user-data-dir=" + appdata_local_dir + "Google/Chrome/User Data")

        self.driver = webdriver.Chrome(executable_path=driver_path, chrome_options=browser_options)

    @staticmethod
    def update_webdriver(appdata_dir, latest):
        """
        Download the newest version of the Chrome WebDriver using the online API.
        Since it is downloaded as a zip file, the process of unzipping must be done. The zip file itself is
        stored in memory with BytesIO, so it doesn't need to be cleaned up. This is a fair expenditure seeing as the
        ChromeDriver is only a few megabytes.
        :param appdata_dir: the appdata directory
        :param latest: the latest version of the Chrome WebDriver
        :return: nothing
        """
        webdriver_download = requests.get("https://chromedriver.storage.googleapis.com/" + latest +
                                          "/chromedriver_win32.zip")
        webdriver_zip = zipfile.ZipFile(io.BytesIO(webdriver_download.content))
        webdriver_zip.extractall(appdata_dir + "AutomaticBrowserLogin/Webdrivers/chromedriver_win32/")
        driver_version_file = open(chrome_driver_version_directory, "w")
        json.dump({"version": latest}, driver_version_file)
        driver_version_file.close()

    def open_new(self, website, payload):
        self.driver.execute_script("window.open('%s')" % website)
        self.switch_to_new_tab()
        self.wait_for_load()
        self.do_login(website, payload)

    def do_login(self, website, payload):
        """
        Perform the actual input of the username and password into the website.
        :param website: the website to log in to.
        :param payload: the username and password  # TODO split this up into normal username/password
        :return: nothing
        """
        if payload.get("username") == "" and payload.get("password") == "":
            return
        Logger.debug("website:", website)
        Logger.debug("payload:", payload)
        user = self.driver.find_element_by_xpath("//input[contains(@name, 'ser') or contains(@name, 'email') "
                                                 "or contains(@name, 'login') or contains(@type, 'email')]")
        user.send_keys(payload.get("username"))

        # special cases

        # Google login is unusual and a <span> element is used to submit both the username and password,
        # so we need to use the enter key instead
        if website.__contains__("google.com") or website.__contains__("yahoo.com"):
            user.send_keys(Keys.ENTER)
            # TODO: find a better method, this one is prone to race conditions
            sleep(1)
            self.wait_for_load()
        password = self.driver.find_element_by_xpath("//input[contains(@name, 'ass') or contains(@name, 'pw')]"
                                                     "[not(@type='hidden')]")
        password.send_keys(payload.get("password"))
        if website.__contains__("google.com") or website.__contains__("yahoo.com"):
            password.send_keys(Keys.ENTER)
        else:
            user.submit()

    def switch_to_new_tab(self):
        handles = self.driver.window_handles
        current_handle = self.driver.current_window_handle
        for handle in handles:
            if handle != current_handle:
                self.driver.switch_to.window(handle)

    def wait_for_load(self):
        while str(self.driver.execute_script("return document.readyState")) != "complete":
            sleep(1)
        return

    def run(self):
        """
        Automatically login to each webpage using the information from the user info file.
        :return: nothing
        """
        try:
            user_info = open(user_info_directory, "rb")
        except FileNotFoundError:
            Logger.error("User info file not found")
            return
        for index, line in enumerate(user_info):
            website, username, password = PopupIO(index, user_info_directory).load_login()
            payload = {"username": username, "password": password.decode()}
            self.open_new(website, payload)

        # close first tab
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        App.get_running_app().stop()


def run_autologin():
    Logger.info("opening browser tabs")
    s = Startup()
    s.run()


if __name__ == "__main__":
    run_autologin()
