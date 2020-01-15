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
    
    
    #---------------------------------------------
    Alarm2 = []
    for Al in range(72, 122, 1): #Alarm 2
        if data[Al] != 0:
            Alarm2.append(str(chr(data[Al])))
            #print(str(chr(data[Al])))
    
    genalarm2 = ''.join(map(str,Alarm2))
    #logger.info(genalarm2)
    del Alarm2 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #-------------------------------------------
    Alarm3 = []
    for Al in range(122, 172, 1): #Alarm 3
        if data[Al] != 0:
            Alarm3.append(str(chr(data[Al])))
    
    genalarm3 = ''.join(map(str,Alarm3))
    #logger.info(genalarm3)
    del Alarm3 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #-------------------------------------------
    Alarm4 = []
    for Al in range(172, 222, 1): #Alarm 4
        if data[Al] != 0:
            Alarm4.append(str(chr(data[Al])))
    
    genalarm4 = ''.join(map(str,Alarm4))
    #logger.info(genalarm4)
    del Alarm4 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #-------------------------------------------
    Alarm5 = []
    for Al in range(222, 272, 1): #Alarm 5
        if data[Al] != 0:
            Alarm5.append(str(chr(data[Al])))
    
    genalarm5 = ''.join(map(str,Alarm5))
    #logger.info(genalarm5)
    del Alarm5 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #-------------------------------------------
    Alarm6 = []
    for Al in range(272, 322, 1): #Alarm6
        if data[Al] != 0:
            Alarm6.append(str(chr(data[Al])))
    
    genalarm6 = ''.join(map(str,Alarm6))
    #logger.info(genalarm6)
    del Alarm6 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #--------------------------------------------
    Alarm7 = []
    for Al in range(322, 372, 1): # Alarm 7
        if data[Al] != 0:
            Alarm7.append(str(chr(data[Al])))
    
    genalarm7 = ''.join(map(str,Alarm7))
    #logger.info(genalarm7)
    del Alarm7 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #------------------------------------------
    #Hier stimmt etwas mit den Daten nicht.
    Alarm8 = []
    for Al in range(372, 422, 1): #Alarm 8
        if data[Al] != 0:
            Alarm8.append(str(chr(data[Al])))
    
    genalarm8 = ''.join(map(str,Alarm8))
    #logger.info(genalarm8)
    del Alarm8 # Löschen der Variable
    AL = None #Löschen der Variablen
    #Hier stimmt etwas mit den Daten nicht.
    
    #------------------------------------------
    Alarm9 = []
    for Al in range(422, 472, 1): #Alarm 9
        if data[Al] != 0:
            Alarm9.append(str(chr(data[Al])))
    
    genalarm9 = ''.join(map(str,Alarm9))
    #logger.info(genalarm9)
    del Alarm9 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #------------------------------------------
    Alarm10 = []
    for Al in range(472, 522, 1): #Alarm 10
        if data[Al] != 0:
            Alarm10.append(str(chr(data[Al])))
    
    genalarm10 = ''.join(map(str,Alarm10))
    #logger.info(genalarm10)
    del Alarm10 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #-------------------------------------------
    Alarm11 = []
    for Al in range(522, 572, 1): #Alarm 11
        if data[Al] != 0:
            Alarm11.append(str(chr(data[Al])))
    
    genalarm11 = ''.join(map(str,Alarm11))
    #logger.info(genalarm11)
    del Alarm11 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #------------------------------------------
    Alarm12 = []
    for Al in range(572, 622, 1): #Alarm12
        if data[Al] != 0:
            Alarm12.append(str(chr(data[Al])))
    
    genalarm12 = ''.join(map(str,Alarm12))
    #logger.info(genalarm12)
    del Alarm12 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #-----------------------------------------
    Alarm13 = []
    for Al in range(622, 672, 1): #Alarm 13
        if data[Al] != 0:
            Alarm13.append(str(chr(data[Al])))
    
    genalarm13 = ''.join(map(str,Alarm13))
    #logger.info(genalarm13)
    del Alarm13 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #------------------------------------------
    Alarm14 = []
    for Al in range(672, 722, 1): #Alarm 14
        if data[Al] != 0:
            Alarm14.append(str(chr(data[Al])))
    
    genalarm14 = ''.join(map(str,Alarm14))
    #logger.info(genalarm14)
    del Alarm14 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #------------------------------------------
    Alarm15 = []
    for Al in range(722, 772, 1): #Alarm15
        if data[Al] != 0:
            Alarm15.append(str(chr(data[Al])))
    
    genalarm15 = ''.join(map(str,Alarm15))
    #logger.info(genalarm15)
    del Alarm15 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    #-----------------------------------------
    Alarm16 = []
    for Al in range(772, 822, 1): #Alarm16
        if data[Al] != 0:
            Alarm16.append(str(chr(data[Al])))
    
    genalarm16 = ''.join(map(str,Alarm16))
    #logger.info(genalarm16)
    del Alarm16 # Löschen der Variable
    AL = None #Löschen der Variablen
    
    deviceID = 256*data[20] + data[21] # Genset ID 
    funcswitchID = 256*data[8] + data[9] # Funcswitch ID
                        
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
    
    if funcswitchID == 2 or funcswitchID == 1:
        try:
            #-----------
            #Update Warnung
            sqlBHKWerror = """UPDATE supervision_chpgeodata SET CHPIDGEO = '{0}', CHPLastUpdate = '{1}', CHPAlarm1 = '{2}', CHPAlarm2 = '{3}', CHPAlarm3 = '{4}', CHPAlarm4 = '{5}', CHPAlarm5 = '{6}', CHPAlarm6 = '{7}', CHPAlarm7 = '{8}', CHPAlarm8 = '{9}', CHPAlarm9 = '{10}',CHPAlarm10 = '{11}', CHPAlarm11 = '{12}', CHPAlarm12 = '{13}', CHPAlarm13 = '{14}', CHPAlarm14 = '{15}', CHPAlarm15 = '{16}', CHPAlarm16 = '{17}' WHERE CHPIDGEO = '{0}'""".format(deviceID, timestamp, genalarm1, genalarm2, genalarm3, genalarm4, genalarm5, genalarm6, genalarm7, genalarm8, genalarm9, genalarm10, genalarm11, genalarm12, genalarm13, genalarm14, genalarm15, genalarm16)
    
            #write informaiton to DB
            dbcom.WriteToDatabase(sqlBHKWerror, dbhost, dbport, dbuser, dbpassword, dbdatabase)    

        except Exception as e:
            logger.error(str(e))
    
    if funcswitchID == 2:
        try:
            #-----------
            #Write Errorlog to Database
            sqlerrorlog = """INSERT INTO supervision_chperrorlog (CHPnumber, CHPAlarmtime, CHPAlarm1, CHPAlarm2, CHPAlarm3, CHPAlarm4, CHPAlarm5, CHPAlarm6, CHPAlarm7, CHPAlarm8, CHPAlarm9, CHPAlarm10, CHPAlarm11, CHPAlarm12, CHPAlarm13, CHPAlarm14, CHPAlarm15, CHPAlarm16, CHPAlarmInfo) VALUE ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}','{18}')""".format(deviceID, timestamp, genalarm1, genalarm2, genalarm3, genalarm4, genalarm5, genalarm6, genalarm7, genalarm8, genalarm9, genalarm10, genalarm11, genalarm12, genalarm13, genalarm14, genalarm15, genalarm16,genalarm1)

            #write informaiton to DB
            dbcom.WriteToDatabase(sqlerrorlog, dbhost, dbport, dbuser, dbpassword, dbdatabase)
        except Exception as e:
            logger.info(str(e))
