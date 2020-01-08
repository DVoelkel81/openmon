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

"""DeviceStateUpdate.py will update the Informatione for every Device like Alarms, Timer and so on.
"""

# Generic/Built-in
import sys
import logging
import os
import datetime
import dbcom
from time import *
from logging.handlers import RotatingFileHandler

#create logging folder
#logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log" #Windows
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "/log" #Linux

#check if folder exists
if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)


# create logger
logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/DeviceStateUpdate.log" #LINUX
#logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\analysis.log" #Windows
logger = logging.getLogger("DeviceStateUpdate")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#logger.addHandler(stream_handler)
logger.addHandler(handler)


def Deviceupdate(scDataArray,dbhost,dbport,dbuser,dbpassword,dbdatabase):
    """Deviceupdate function will only update the timer and counter on the device state, also reset the alarms in case of alarm is over"""
    
    #Zeitstempel Aktuelle Zeit
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    #If State will be true if Genset Error still exist or no error is activ
    if scDataArray[6] == 1 or scDataArray[6] == 0:
        #Update BHKW Timer
        sql = """UPDATE supervision_chpgeodata SET CHPIDGEO = '{0}',
          CHPMaintenance_time1 = '{1}', CHPMaintenance_time2 = '{2}', CHPMaintenance_time3 = '{3}',
          CHPMaintenance_time4 = '{4}', CHPLastUpdate = '{5}', CHPkwhzaehler = '{6}', CHPkVArhzaehler = '{7}',
          CHPbetriebsstunden = '{8}' WHERE CHPIDGEO = '{0}'""".format(scDataArray[0], scDataArray[1], scDataArray[2], scDataArray[3], scDataArray[4],  timestamp, scDataArray[14], scDataArray[15], scDataArray[16])
        
        #write informaiton to DB
        dbcom.WriteToDatabase(sql, dbhost, dbport, dbuser, dbpassword, dbdatabase)


    #If state will be Aktive if no error is active set Error to empty
    if scDataArray[6] == 0:
        #Update Warnung
        sqlwarnupdate = """UPDATE supervision_chpgeodata SET CHPIDGEO = '{0}',
          CHPLastUpdate = '{1}', CHPAlarm1 = '{2}', CHPAlarm2 = '{3}', CHPAlarm3 = '{4}', CHPAlarm4 = '{5}', CHPAlarm5 = '{6}', CHPAlarm6 = '{7}',
          CHPAlarm7 = '{8}', CHPAlarm8 = '{9}', CHPAlarm9 = '{10}',CHPAlarm10 = '{11}', CHPAlarm11 = '{12}', CHPAlarm12 = '{13}',
          CHPAlarm13 = '{14}', CHPAlarm14 = '{15}', CHPAlarm15 = '{16}', CHPAlarm16 = '{17}' WHERE CHPIDGEO = '{0}'""".format(scDataArray[0], timestamp, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ')
        
        #write informaiton to DB
        dbcom.WriteToDatabase(sqlwarnupdate, dbhost, dbport, dbuser, dbpassword, dbdatabase)
