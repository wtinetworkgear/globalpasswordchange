#!/usr/bin/python
# This program will read a wti.ini file for a hostname, username and password.
# It will login to the unit specified and read the Change Log file
# It will compare the values already read in the past and append the new Change Log entries to the existing file.
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
import csv
import os

from requests.exceptions import HTTPError
urllib3.disable_warnings()

iTotalDBMaster = 0;
iTotalLive = 0;
iTotalNewChanges = 0

# Main code section
if __name__ == '__main__':
    timeout = 20
    params = ""
    sURL = ""
    BASE_PATH = "/cgi-bin/gethtml?formWTIChangeLogsB.html"

    print("\n\nWTI Device Change Log Download Program\n")

    config = configparser.ConfigParser()

    config.sections()
    # Open the file with the hostname, username and password entries
    config.read('wti.ini')
    config.sections()

    # remmove file that records all the new Changes requests
    if (os.path.isfile("new.txt")):
        os.remove("new.txt")

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

        # Assemble the full sURL
        sURL = URI+HOST_NAME+BASE_PATH

        cszHostFileName = HOST_NAME.replace(".", "") + ".txt"

        try:
            # Get request to display unit's Change Log
            response = requests.get(sURL, params=params, timeout=timeout, auth=(USERNAME, PASSWORD), verify=VERIFY)
            if (response.status_code == 200):
#                print(response.text)

                # Write the live data that was just read
                with open('out.txt', 'w') as output:
                    output.write("datestamp,user,command,port\n")
                    output.write(response.text)

                # Open the past data
                try:
                    with open(cszHostFileName, mode ='r')as Hostfile:
                        DBMaster = csv.DictReader(Hostfile)
                        DBMasterrow = list(DBMaster)
                        DBMasterCount = len(list(DBMasterrow))                    
                        Hostfile.close()
                except:
                        DBMasterCount = 0

                with open('out.txt', mode ='r')as Livefile:
                    readerLive = csv.DictReader(Livefile)
                    Liverow = list(readerLive)
                    LiveCount = len(list(Liverow))                    
                    Livefile.close()

                os.remove("out.txt")

                print("Total dbMaster %d" % (DBMasterCount))
                print("Live Count: %d" % LiveCount)

                iMatchIndex = 0
                if (DBMasterCount == 0):
                    iMatchIndex = LiveCount
                else:
                    if (LiveCount > 0):
                        for iMatchIndex in range(LiveCount):                    
                            if ((Liverow[iMatchIndex]['datestamp']) == (DBMasterrow[0]['datestamp'])):
                                print("Found match %d." % iMatchIndex)
                                break;

#               print("iMatchIndex Count: %d\n" % iMatchIndex)

                with open(cszHostFileName, 'w+') as Hostfile:
                    Hostfile.write("datestamp,user,command,port\n")
                    if (iMatchIndex > 0):
                        ii = 0
                        for ii in range(iMatchIndex):                    
                            Hostfile.write("%s,%s,%s,%s\n" % (Liverow[ii]['datestamp'], Liverow[ii]['user'], Liverow[ii]['command'], Liverow[ii]['port']))

                        with open("new.txt", 'a+') as Newfile:
                            ii = 0
                            for ii in range(iMatchIndex):                    
                                if (iTotalNewChanges == 0):
                                    Newfile.write("datestamp,user,command,port\n")

                                Newfile.write("%s,%s,%s,%s,%s\n" % (HOST_NAME, Liverow[ii]['datestamp'], Liverow[ii]['user'], Liverow[ii]['command'], Liverow[ii]['port']))
                                iTotalNewChanges = iTotalNewChanges + 1
                            Newfile.close()
                            
                    if (DBMasterCount > 0):
                        ii = 0
                        for ii in range(DBMasterCount):                    
                            Hostfile.write("%s,%s,%s,%s\n" % (DBMasterrow[ii]['datestamp'], DBMasterrow[ii]['user'], DBMasterrow[ii]['command'], DBMasterrow[ii]['port']))

                    Hostfile.close()

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
