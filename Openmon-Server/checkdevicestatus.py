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

"""checkdevicestatus.py will analyize the Status from the device an store it into the Database
"""

import sys
import logging
import os
#import pymysql
#import psycopg2
import dbcom
import datetime
from time import *
from logging.handlers import RotatingFileHandler


#create logging folder
#logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log" #Windows
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "/log" #Linux

#check if folder exists
if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)


# create logger
logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/checkdevicestatus.log" #Linux
#logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\analysis.log" #Windows
logger = logging.getLogger("checkdevicestatus")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def statuscheck(data,dbhost,dbport,dbuser,dbpassword,dbdatabase):
    """Statuscheck use the transmited status from the Device and write it to the Database"""
    
    #Zerlegen des Statusbyte und vorbereitung fuer SQL
    CHPStatus = bytearray(5)

    #Genset is Ready
    #if test[13] & 0x0002 == 0x0002:
    if ((data["mode"] == 0x01) or (data["mode"] == 0x02) or (data["mode"] == 0x03)) and not(data["statusword4"] & 0x0001 == 0x0001):
        CHPStatus[0] = 0x00 #CHP in Operation
        CHPStatus[1] = 0x01 #CHP Ready
        CHPStatus[2] = 0x00 #CHP Warning
        CHPStatus[3] = 0x00 #CHP Alarm
        CHPStatus[4] = 0x00 #CHP Off
    else:
        pass
    #Genset in Operation
    if data["statusword4"] & 0xC000 == 0xC000:
        CHPStatus[0] = 0x01 #CHP in Operation
        CHPStatus[1] = 0x00 #CHP Ready
        CHPStatus[2] = 0x00 #CHP Warning
        CHPStatus[3] = 0x00 #CHP Alarm
        CHPStatus[4] = 0x00 #CHP Off
    else:
        pass
    #Genset has a Warning
    if data["statusword3"] & 0x8000 == 0x8000:
        CHPStatus[0] = 0x00 #CHP in Operation
        CHPStatus[1] = 0x00 #CHP Ready
        CHPStatus[2] = 0x01 #CHP Warning
        CHPStatus[3] = 0x00 #CHP Alarm
        CHPStatus[4] = 0x00 #CHP Off
    else:
        pass

    #Genset has an Alarm
    if data["statusword4"] & 0x0001 == 0x0001:
        CHPStatus[0] = 0x00 #CHP in Operation
        CHPStatus[1] = 0x00 #CHP Ready
        CHPStatus[2] = 0x00 #CHP Warning
        CHPStatus[3] = 0x01 #CHP Alarm
        CHPStatus[4] = 0x00 #CHP Off
    else:
        pass

    if data["mode"] == 0x00:
        CHPStatus[0] = 0x00 #CHP in Operation
        CHPStatus[1] = 0x00 #CHP Ready
        CHPStatus[2] = 0x00 #CHP Warning
        CHPStatus[3] = 0x00 #CHP Alarm
        CHPStatus[4] = 0x01 #CHP Off
    else:
        pass

    #logger.info(CHPStatus)

    #Auswertung Genset Mode
    if data["mode"] == 0x00:
        CHPdevstatus = "OFF"
    elif data["mode"] == 0x01:
        CHPdevstatus = "MAN"
    elif data["mode"] == 0x02:
        CHPdevstatus = "SEM"
    elif data["mode"] == 0x03:
        CHPdevstatus = "AUTO"

        #logger.info(CHPdevstatus)
    #Zeitstempel Aktuelle Zeit
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #http://mysql.lernenhoch2.de/lernen/mysql-anfanger/update-daten-andern/    
    
    #create the SQL Statement
    sql = """UPDATE supervision_chpgeodata SET CHPIDGEO = '{5}',
      CHPInoperation = '{0}', CHPReady = '{1}', CHPWarning = '{2}', CHPMalfunction = '{3}',
      CHPOff = '{4}', CHPLastUpdate = '{6}', CHPDevStatus='{7}' WHERE CHPIDGEO = '{5}'""".format(CHPStatus[0], CHPStatus[1], CHPStatus[2], CHPStatus[3], CHPStatus[4], data["deviceid"], timestamp, CHPdevstatus)
    
    #logger.info(sql)
    
    #write informaiton to DB
    dbcom.WriteToDatabase(sql, dbhost, dbport, dbuser, dbpassword, dbdatabase)
    #dbcom.main(sql)
