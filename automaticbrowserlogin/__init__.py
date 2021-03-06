import os
import keyring
from keyring.backends import Windows
import binascii

keyring.set_keyring(Windows.WinVaultKeyring())

appdata_dir = os.getenv("APPDATA").replace("\\", "/") + "/"
if not os.path.isdir(appdata_dir + "AutomaticBrowserLogin/"):
    os.makedirs(appdata_dir + "AutomaticBrowserLogin/Webdrivers/")

root_directory = appdata_dir + "AutomaticBrowserLogin"
user_info_directory = root_directory + "/userinfo.json"
user_info_test_directory = root_directory + "/userinfotest.json"
temp_directory = root_directory + "/temp.json"
options_directory = root_directory + "/options.json"
chrome_driver_version_directory = root_directory + "/driverversion.json"

service_id = "AutomaticBrowserLogin"
# keyring.delete_password(service_id, "private_key")
private_key = keyring.get_password(service_id, "private_key")
if private_key is None:
    # need to generate 16-bit key that can be converted to string for keyring, and hexlify doubles the length
    private_key = os.urandom(16)
    keyring.set_password(service_id, "private_key", binascii.hexlify(private_key).decode("utf-8"))
else:
    private_key = binascii.unhexlify(private_key.encode("utf-8"))
