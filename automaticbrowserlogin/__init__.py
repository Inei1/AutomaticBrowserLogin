import os
import keyring
import binascii

root_directory = os.path.dirname(os.path.dirname(__file__))
user_info_directory = root_directory + "/userInfo.json"
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
