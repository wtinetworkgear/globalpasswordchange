#!/usr/bin/python
# This program will read a wti.ini file for a hostname, username and password.
# It will create a random password and create a JSON block to send the WTI device to change the password.
# Finally it will write this new password to the wti.ini file for future use.
#
# NOTES: the wti.ini file format will be as follows:
# [device.yourcompany.com]
# username = existingdeviceusername
# userpassword = existingdevicepassword
# secure = yes
# verify = yes
#
import urllib3
import requests
import configparser
import random
from requests.exceptions import HTTPError
urllib3.disable_warnings()

# Function to generate a random password
def pw_gen(size = 8):
    sBeginList = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sEndList = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$^*()?"
    sFirstReturn =  "".join(random.sample(sBeginList,size ))
    sSecondReturn =  "".join(random.sample(sEndList,size ))
    return sFirstReturn + sSecondReturn

# Main code section
if __name__ == '__main__':
    timeout = 20
    params = ""
    sURL = ""
    BASE_PATH = "/api/v2/config/users"

    print("\n\nWTI Device Automatic Password Change Program\n")

    config = configparser.ConfigParser()

    config.sections()
    # Open the file wit hthe hostname, username and password entries
    config.read('wti.ini')
    config.sections()

    for section_name in config.sections():
        URI = "http://"
        HOST_NAME = ""
        USERNAME = ""
        PASSWORD = ""
        VERIFY = False
        sNewPassword = ""

        print ('Host Name:', section_name)
        HOST_NAME = section_name
        for name, value in config.items(section_name):
            if (name == "username"):
                USERNAME = value
            if (name == "userpassword"):
                PASSWORD = value
            if (name == "secure"):
                if (value == "yes"):
                    URI = "https://"
            if (name == "verify"):
                if (value == "yes"):
                    VERIFY = True

        if ((len(URI) == 0) or (len(HOST_NAME) == 0) or (len(USERNAME) == 0) or (len(PASSWORD) == 0)):
            print("Zero length something, Stop and check your .ini file")
            exit(0)

        # create the random password (8 chars * 2)
        sNewPassword = pw_gen(8);

        # Assemble the full sURL
        sURL = URI+HOST_NAME+BASE_PATH
        print("    "+sURL)

        # Assemble the JSON load to PUT to the WTI device
        json_load = '{"users":{"username": "' + USERNAME + '","newpasswd": "' + sNewPassword + '"}}'
        print("    JSON Sent: "+json_load)

        try:
            # Put request is for editing, login with the old password
            response = requests.put(sURL, params=params, data=json_load, timeout=timeout, auth=(USERNAME, PASSWORD), verify=VERIFY)
            if (response.status_code == 200):
                # Everything was good, write the new password to the wti.ini file
                config.set(HOST_NAME, 'userpassword', sNewPassword)
                with open('wti.ini', 'w') as configfile:
                    config.write(configfile)

                parsed_json = response.json()
                dStatus = parsed_json['status']
                print(dStatus)
                print("    OK: {0}\n".format(response.status_code))
            else:
                print("    ERROR: {0}\n".format(response.status_code))

        except requests.exceptions.HTTPError as errh:
            print ("    Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("    Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("    Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("    Something Else: ",err)
