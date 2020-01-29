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

"""ComAp_Errortext.py will analyize the Error Message From Comap Gensetcontroller IS-NTC
"""

# Generic/Built-in
import sys
import os
import datetime
import logging
from logging.handlers import RotatingFileHandler
from time import *


# Own modules
import Errormail
import dbcom

#create logging folder
#logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log" #Windows
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "/log" #Linux

#check if folder exists
if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)
    

# create logger
logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/errortext.log" #Mac
logger = logging.getLogger("errortext")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


    
def getErrorText(data,dbhost,dbport,dbuser,dbpassword,dbdatabase,emailsender,emailsmtpserver,emailsmtpusername,emailsmtppassword,emailsmtpport):
    #Create Dataset
    errorvalue = []
    
    #Create Alarmtext
    #create Alarmlist
    genalarm1 = data["Alarmtext1"]
    genalarm2 = data["Alarmtext2"]
    genalarm3 = data["Alarmtext3"]
    genalarm4 = data["Alarmtext4"]
    genalarm5 = data["Alarmtext5"]
    genalarm6 = data["Alarmtext6"]
    genalarm7 = data["Alarmtext7"]
    genalarm8 = data["Alarmtext8"]
    genalarm9 = data["Alarmtext9"]
    genalarm10 = data["Alarmtext10"]
    genalarm11 = data["Alarmtext11"]
    genalarm12 = data["Alarmtext12"]
    genalarm13 = data["Alarmtext13"]
    genalarm14 = data["Alarmtext14"]
    genalarm15 = data["Alarmtext15"]
    genalarm16 = data["Alarmtext16"]
    
    deviceID = data["deviceid"] # Genset ID 
    
    if Data["Alarmtext1"]:
        funcswitchID = 2 # Funcswitch ID
    else:
        funcswitchID = 1
                        
    #Zeitstempel Aktuelle Zeit
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    #Senden einer E-Mail das es zu einer Stoerung im System gekommen ist.
    if funcswitchID == 2:
        Errormail.sendmail(emailsmtpserver,emailsmtpusername,emailsmtppassword,emailsmtpport,"dennis.voelkel@outlook.com", "Von Server Stoerung BHKW K" + str(deviceID), "Es ist eine Stoerung an BHKW " + str(deviceID) + " aufgetreten. \n Folgende Meldugnen sind aufgetretten \n " +
                                                genalarm1 + " \n " + genalarm2 + " \n " + genalarm3 + " \n " + genalarm4 + " \n " + genalarm5 + " \n " + genalarm6 + " \n " +
                                                genalarm7 + " \n " + genalarm8 + " \n " + genalarm9 + " \n " + genalarm10 + " \n " + genalarm11 + " \n " + genalarm12 + " \n " + genalarm13 + " \n " +
                                                genalarm14 + " \n " + genalarm15 + " \n " + genalarm16)
    else:
        pass #Weiterleitung im Programm, keine fehler im Genset
    
    #if funcswitchID == 2 or funcswitchID == 1:
        #try:
            ##-----------
            ##Update Warnung
            #sqlBHKWerror = """UPDATE supervision_chpgeodata SET deviceid = '{0}', alarmtime = '{1}', alarm1 = '{2}', alarm2 = '{3}', alarm3 = '{4}', alarm4 = '{5}', alarm5 = '{6}', CHPAlarm6 = '{7}' WHERE deviceid = '{0}'""".format(deviceID, timestamp, genalarm1, genalarm2, genalarm3, genalarm4, genalarm5)
    
            ##write informaiton to DB
            #dbcom.WriteToDatabase(sqlBHKWerror, dbhost, dbport, dbuser, dbpassword, dbdatabase)    

        #except Exception as e:
            #logger.error(str(e))
    
    if funcswitchID == 2:
        try:
            #-----------
            #Write Errorlog to Database
            sqlerrorlog = """INSERT INTO supervision_errorlog (deviceid, alarmtime, alarm1, alarm2, alarm3, alarm4, alarm5, alarmInfo) VALUE ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')""".format(deviceID, timestamp, genalarm1, genalarm2, genalarm3, genalarm4, genalarm5, genalarm1)

            #write informaiton to DB
            dbcom.WriteToDatabase(sqlerrorlog, dbhost, dbport, dbuser, dbpassword, dbdatabase)
        except Exception as e:
            logger.info(str(e))
