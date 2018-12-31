(note: this project's code is not a good indicator of my current skills. A complete rewrite of the code is in progress.)

# AutomaticBrowserLogin

AutomaticBrowserLogin is a configurable python script that automatically opens browser tabs and logs you in. A frontend made in Kivy is provided to configure the websites to visit and the login information to enter. To log on to the websites, selenium webdriver is used to automatically submit login information. AutomaticBrowserLogin currently only supports the Chrome browser on Windows, but other platforms and browsers may be supported in the future.

**_WARNING:_** Your passwords are not securely stored with this program! They are encrypted before being stored on disk, but they can be easily decrypted. If an attacker gains access to your computer, your passwords may be compromised. Use with caution, and do not use this program with anything confidential!

## Installation

The newest version of AutomaticBrowserLogin can be found on the releases page [here](https://github.com/Inei1/AutomaticBrowserLogin/releases). The file may be downloaded to any location. After unzipping the folder, run "Config.bat" to configure the websites and information to for automatically logging in. Look at the Usage section for information on configuring the program. Run "Startup.bat" to test the program, then put "Startup.vbs" into the [startup directory](http://www.thewindowsclub.com/startup-folder-in-windows-8). After that, press WIN+R and type in APPDATA. Create a new folder called AutomaticBrowserLogin, and in that folder create another one called WebDrivers. Download the Chrome web driver at https://sites.google.com/a/chromium.org/chromedriver/ and unzip it into the newly created WebDrivers directory. (Doing this automatically is on the feature roadmap.)

**_Note: The webbrowser that you wish to use must NOT be open for this program to work!_** 

## Usage

When first running the program, look at the options menu and be sure the button for the browser you want to use is _blue_. Enter any arguments in the arguments box, separated by a space. A list of arguments can be found online for [Chrome](https://peter.sh/experiments/chromium-command-line-switches/) and [Firefox](https://developer.mozilla.org/en-US/docs/Mozilla/Command_Line_Options). To add a login, click on the add button on the main screen. In the website box, give the _full_ url to the login page of the website you with to login to. It is recommended to copy-paste the address when you navigate to the login page, such as https://github.com/login. The username and password boxes are self-explanitory, and should be given your username and password. You can leave them blank if you do not wish to login to the webpage.

## Common Problems

These common problems may or may not be fixable by you. Try opening "Startup.bat" to get debug messages and error messages.

#### Website does not login correctly/browser stops prematurely:

Report the website by opening a Github issue. Due to the nature of this program, this is not possible to fix on the user's end.

#### Username/Password are wrong:

Double check that the information you entered is correct. If the problem persists, open "Startup.bat" to look for debug messages, and open a Github issue if the problem cannot be solved.

#### Web browser does not start:

Check that the browser is selected in the options menu. If the problem persists, follow the steps directly above.

#### The batch file error message says something about Selenium

Update your [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/).

## License

This program is liscensed under MIT. See LICENSE.txt.

All technologies used belong to their respective owners.
