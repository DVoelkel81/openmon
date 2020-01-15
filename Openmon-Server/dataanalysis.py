#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

__author__ = "Dennis Voelkel"
__copyright__ = "Copyright 2019, Openmon"
__credits__ = ["Dennis Voelkel"]
__license__ = "MIT"  #
__version__ = "0.0.1"
__maintainer__ = "Dennis Voelkel"
__email__ = "dennis.voelkel@outlook.com"
__status__ = "Develop"

"""dataanalysis.py will analyse the incoming UDP Package an send the data
to the requested functions
"""

# Generic/Built-in
import sys
import logging
import os
#import pymysql
import datetime
from time import *
import xml.etree.ElementTree as ET
from logging.handlers import RotatingFileHandler

# Own modules
import ComAp_Errortext
import checkdevicestatus
import DeviceStateUpdate
import DeviceLogging



#create logging folder
#logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log" #Windows
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "/log" #MAC

#check if folder exists
if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)


# create logger
logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/dataanalysis.log" #LINUX
#logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\analysis.log" #Windows
logger = logging.getLogger("dataanalysis")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#logger.addHandler(stream_handler)
logger.addHandler(handler)

try:
    # Parse DBConfig.xml
    tree = ET.parse('/home/supervision-script/dbconfig.xml')
    root = tree.getroot()
    for DBServer in root.findall('DBServer'):
        dbhost = DBServer.find('host').text
        #logger.info(dbhost)
        dbport = DBServer.find('port').text
        #logger.info(dbport)
        dbuser = DBServer.find('user').text
        #logger.info(dbuser)
        dbpassword = DBServer.find('password').text
        #logger.info(dbpassword)
        dbdatabase = DBServer.find('database').text
        #logger.info(dbdatabase)
    
    for EmailServer in root.findall('EmailServer'):
        emailsender = EmailServer.find('sender').text # fqdn of the mail server
        #logger.info(emailsender)
        emailsmtpserver = EmailServer.find('smtpserver').text # username for the SMTP authentication
        #logger.info(emailsmtpserver)
        emailsmtpusername = EmailServer.find('smtpusername').text # username for the SMTP authentication
        #logger.info(emailsmtpusername)
        emailsmtppassword = EmailServer.find('smtppassword').text # password for the SMTP authentication
        #logger.info(emailsmtppassword)
        emailsmtpport =EmailServer.find('smtpport').text #smtp Port selection
        #logger.info(emailsmtpport)
except:
    logger.error("Could not open dbconfig.xml or parse the values")


#Function for Dataanalysis
def socketanalysis(data):
    """Put the incoming data into an array for analysis, converting and manitulation"""
    
    #Create a array for DAta
    DataArray =[]
    DataArray.append(256*data[20] + data[21]) # Genset ID / Test[0]
    DataArray.append(256*data[36] + data[37]) # Genset Timer 1 / Test[1]
    DataArray.append(256*data[38] + data[39]) # Genset Timer 2 / Test[2]
    DataArray.append(256*data[40] + data[41]) # Genset Timer 3 / Test[3]
    DataArray.append(256*data[42] + data[43]) # Genset Timer 4 / Test[4]
    DataArray.append(256*data[20] + data[21]) #SGENSET ID / Test[5]
    DataArray.append(256*data[8] + data[9]) #Festellen der COB ID test[6]
    DataArray.append(256*data[22] + data[23]) #Logbout 1 Test7
    DataArray.append(256*data[24] + data[25]) #Logbout 2 Test8
    DataArray.append(256*data[26] + data[27]) #Logbout 3 Test9
    DataArray.append(256*data[28] + data[29]) #Logbout 4 Test10
    DataArray.append(256*data[30] + data[31]) #Logbout 5 Test11
    DataArray.append(256*data[32] + data[33]) #Logbout 6 Test12
    DataArray.append(256*data[34] + data[35]) #Logbout 7 Test13
    DataArray.append(256*256*256*data[44] + 256*256*data[45] + 256*data[46] + data[47]) #kwh Powercount Test14
    DataArray.append('0')# Actuall fix implementing the KVAR with Zero because negative Value are Possible, have to fix Negaitv Value Handling
    DataArray.append(256*256*256*data[52] + 256*256*data[53] + 256*data[54] + data[55]) #Runhours Test16
    DataArray.append(256*data[56] + data[57]) #liste3 modus Test17
    DataArray.append(256*data[58] + data[59]) #Startcounter test 18
    #logger.info(str(DataArray[0]) + "-" + str(len(data)))
    
    if len(data) > 59:
        #DataArray.append(256*data[58] + data[59]) #Startcounter test 18
        DataArray.append(256*data[60] + data[61]) #Fail satrts test 19
        DataArray.append(256*data[62] + data[63]) #Wastegas pri test 20
        DataArray.append(256*data[64] + data[65]) #AbgasWastegassec test 21
        DataArray.append(256*data[66] + data[67]) #Temp HV test 22
        DataArray.append(256*data[68] + data[69]) #Temp RV test 23
        DataArray.append(256*data[70] + data[71]) #Roomtemp test 24
        DataArray.append(256*data[72] + data[73]) #Temp AWT test 25
        DataArray.append(256*data[74] + data[75]) #Motorincoming test 26
        DataArray.append(256*data[76] + data[77]) #Motoroutgoing test 27 
        #logger.info(len(data))   
    
    if DataArray[6] == 2:
            
        #Read COmap Errortext
        ComAp_Errortext.getErrorText(data,dbhost,dbport,dbuser,dbpassword,dbdatabase,emailsender,emailsmtpserver,emailsmtpusername,emailsmtppassword,emailsmtpport)
        
    else:
        pass #Weiterleitung im Programm, keine fehler im Genset        
    try:
        #Check the Status of Devie Information
        checkdevicestatus.statuscheck(DataArray, dbhost, dbport, dbuser, dbpassword, dbdatabase)
    except:
        logger.error("Error loading function checkdevicestatus")
    
    try:
        #update the devicestate
        DeviceStateUpdate.Deviceupdate(DataArray, dbhost, dbport, dbuser, dbpassword, dbdatabase)
    except:
        logger.error("Error loading function DeviceStateUpdate")
        
    try:
        #Insert the Processdata into the Database
        DeviceLogging.Devicelog(DataArray, dbhost, dbport, dbuser, dbpassword, dbdatabase)
    except:
        logger.error("Error loading function Devicelog")
         
    try:
        #Insert the Processdata into the Database
        DeviceLogging.DeviceTemplog(DataArray, dbhost, dbport, dbuser, dbpassword, dbdatabase)
    except:
        logger.error("Error loading function DevicelogTemp")
        
    try:
        #Insert the Processdata into the Database
        DeviceLogging.DeviceStartsLog(DataArray, dbhost, dbport, dbuser, dbpassword, dbdatabase)
    except:
        logger.error("Error loading function DeviceStartsLog")
    
