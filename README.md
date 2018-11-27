WTI Device Automatic Password Change Program

Summary:
This program is used to globally change many WTI device passwords with one running of the program. 
Instead of logging into multiple units, one at a time, then thinking of a new password, this program will automativally login to the WTI device, create a random password, set the new password on the WTI device and then record the new password in an ini file.

Overview:
1. This program will read wti.ini file for hostnames
2. Create a new random password
3. Create a new JSON load to send the edit the username with the new password on the WTI device
4. Login to a WTI device via http(s) with an exising username/password combination and send the JSON blob
5. If sucessful write the new password to the wti.ini file.


wti.ini file format:

[device.yourcompany.com]

This entry and be an IP address or a fully qualified URL

username: the Username on the WTI device that you are attemping to change the password

userpassword: The Current Password of the Username on the WTI device

secure: yes/no yes = https, no = http

verify: if using https, then the certificate will not be validated.


To Run: 
python wti.py


Documentation:

The HTML or RAML file relating to the RESTful API calls can be found here:

https://www.wti.com/t-wti-restful-api-download.aspx

Contact WTI:

If you have any questions, comments or suggestions you can email us at kenp@wti.com

About WTI:

WTI - Western Telematic, Inc. 5 Sterling, Irvine, California 92618

Western Telematic Inc. was founded in 1964 and is an industry leader in designing and manufacturing power management and remote console management solutions for data centers and global network locations. Our extensive product line includes Intelligent PDUs for remote power distribution, metering, reporting and control, Serial Console Servers, RJ45 A/B Fallback Switches and Automatic Power Transfer Switches.