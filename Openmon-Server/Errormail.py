#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

#
# Creation:    16.08.2013
# Last Update: 07.04.2015
#
# Copyright (c) 2013-2015 by Georg Kainzbauer <http://www.gtkdb.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

# import required modules
from email.mime.text import MIMEText
from email.utils import formatdate
import logging
import os
from logging.handlers import RotatingFileHandler
import smtplib
import sys

#########################
#Einfügen Logging Module#
#########################
#Windows Client
#Funktioniert nicht als Exe, hier muss der Absolute Pfad hinein.
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "/log"

if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)
    

#logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\Errormail.log" #Windows
logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/Errormail.log" #Linux
#logPath ="C:\\Myprograms\\Errormail.log"
logger = logging.getLogger("Errormail")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
#-----------------------------------------

########################################
# declaration of default mail settings #
########################################
# mail address of the sender
#sender = 'xxx@xxx.xx'
sender = 'xxx@xxx.xxx'

## fqdn of the mail server

#smtpserver = 'xxx.xxxx.xxx'
smtpserver = 'xxx.xxxx.xxxx'

## username for the SMTP authentication
#smtpusername = 'xxxx@xxxx.xxxx'
smtpusername = 'xxxx'

## password for the SMTP authentication
#smtppassword = 'xxxxx'
smtppassword = 'xxxxx'
smtpport = '587'

##smtp Port selection
#smtpport = '587'

# use TLS encryption for the connection
usetls = True

########################################
# function to send a mail              #
########################################
#def sendmail(server,user,password,port,recipient,subject,content):
def sendmail(server,user,password,port,recipient,subject,content):
    # generate a RFC 2822 message
    msg = MIMEText(content)
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg["Date"] = formatdate(localtime=True)
    
    try:
        # open SMTP connection
        server = smtplib.SMTP(server)

        # start TLS encryption
        if usetls:
            server.starttls()

        # login with specified account
        if user and password:
            server.login(user,password)

        # send generated message
        server.sendmail(sender,recipient,msg.as_string())

        # close SMTP connection
        server.quit()
        
    except smtplib.SMTPException as e:
    
        logger.info(str(e))
    #------------------------------        

########################################
# main function                        #
########################################
def main():

    # call sendmail() and generate a new mail with specified subject and content

    sendmail(smtpserver,smtpusername,smtppassword,smtpport,'dennis.voelkel@outlook.de','Service Fault Test 2','Service Testfehler fuer Mail system')
    # quit python script
    sys.exit(0)
    
if __name__ == '__main__':
    main()    
