# AutomaticBrowserLogin

AutomaticBrowserLogin is a configurable python script that automatically opens browser tabs and logs you in. A frontend made in Kivy is provided to configure the websites to visit and the login information to enter. To log on to the websites, selenium webdriver is used to automatically submit login information. AutomaticBrowserLogin only supports the Chrome browser on Windows.

## Installation

The newest version of AutomaticBrowserLogin can be found on the releases page [here](https://github.com/Inei1/AutomaticBrowserLogin/releases). The file may be downloaded to any location. The `config.exe` executable is used to input desired websites and login information, as well as run arguments for Chrome. Look at the Usage section for information on configuring the program. Run `startup.exe` to test the program, then put it into the user startup directory at `C:\Users\Username\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`. Hidden folders must to be visible to show `ProgramData`.

**_Note: The webbrowser that you wish to use must NOT be open for this program to work!_** 

## Usage

When first running the program, look at the options menu and enter any browser arguments in the arguments box, separated by a space. A list of arguments can be found online for [Chrome](https://peter.sh/experiments/chromium-command-line-switches/). To add a login, click on the add button on the main screen. In the website box, give the _full_ url to the login page of the website you with to login to. It is recommended to copy-paste the address when you navigate to the login page, such as https://github.com/login. The username and password boxes are self-explanitory, and should be given your username and password. You can leave them blank if you do not wish to login to the webpage.

## Common Problems

#### Website does not login correctly/browser stops prematurely:

Report the website by opening a Github issue. Due to the nature of this program, this is not possible to fix on the user's end.

#### Username/Password are wrong:

Double check that the information you entered is correct. Open a github issue if the username and password are confirmed to be correct.

#### Program crashes before opening browser:

Update Google Chrome and restart your computer.

## License

This program is liscensed under MIT. See LICENSE.txt.

All technologies used belong to their respective owners.
