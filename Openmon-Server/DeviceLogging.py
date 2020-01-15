#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

__author__ = "Dennis Voelkel"
__copyright__ = "Copyright 2019, Openmon"
__credits__ = ["Dennis Voelkel"]
__license__ = "MIT"  #
__version__ = "0.0.2"
__maintainer__ = "Dennis Voelkel"
__email__ = "dennis.voelkel@outlook.com"
__status__ = "Develop"

"""Deviceloggin.py will update log all process values and store it into the Database.
"""

# Generic/Built-in
import sys
import logging
import os
#import pymysql
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
logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/DeviceLogging.log" #LINUX
#logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\analysis.log" #Windows
logger = logging.getLogger("DeviceLogging")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#logger.addHandler(stream_handler)
logger.addHandler(handler)


def Devicelog(scDataArray,dbhost,dbport,dbuser,dbpassword,dbdatabase):
    """Devicelog function will insert the process data directly to ghe Database"""
    
    try:

        #--------------
        if scDataArray[6] == 3:
        
            #Zeitstempel Aktuelle Zeit
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
            
            sqlleistung = """INSERT INTO supervision_chppowercount (CHPPCIDGEO, CHPPCkwhzaehler, CHPPCkVArhzaehler, CHPPCinserttime) VALUE ('{0}', '{1}', '{2}', '{3}')""".format(scDataArray[0], scDataArray[14], scDataArray[15], timestamp)
            #logger.info("update des Powercount")
    
                
            #write informaiton to DB
            dbcom.WriteToDatabase(sqlleistung, dbhost, dbport, dbuser, dbpassword, dbdatabase)
            #logger.info("write to DB")
        else:
            #logger.info("test[6] enthielt keine daten " + str(test[6]))
            #logger.info(sql)
            pass
        
    except:
        logger.error("Unknown Failure in Powercounting ")
        
def DeviceTemplog(scDataArray,dbhost,dbport,dbuser,dbpassword,dbdatabase):
    """Devicelog function will insert the Temperatur data directly to the Database"""
    
    try:
        
        #Zeitstempel Aktuelle Zeit
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
            
        sqlleistung = """INSERT INTO supervision_chptemperature (CHPIDGEO, CHPwastgaspri, CHPwastgassec, 
        CHPTempHV, CHPTempRV, CHPboilertemp, CHPRoomtemp, CHPAWT, CHPMotorIN, CHPMotorOUT, CHPReginsertfrom, 
        CHPDReginserttime) VALUE ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', 
        '{11}')""".format(scDataArray[0], scDataArray[20], scDataArray[21], scDataArray[22], scDataArray[23], '0', scDataArray[24], 
                          scDataArray[25], scDataArray[26], scDataArray[27], scDataArray[0],timestamp)
        #logger.info("update des Powercount")
        
                
        #write informaiton to DB
        dbcom.WriteToDatabase(sqlleistung, dbhost, dbport, dbuser, dbpassword, dbdatabase)
        #logger.info("write to DB")
        
    except:
        logger.error("Unknown Failure in DeviceTemplog ")     
    
def DeviceStartsLog(scDataArray,dbhost,dbport,dbuser,dbpassword,dbdatabase):
    #hier weiter
    """Devicelog function will insert the Starts data directly to the Database"""
    
    try:
        
        #Zerlegen des Statusbyte und vorbereitung fuer SQL
        CHPStatus = bytearray(1)
        #Genset in Operation
        if scDataArray[10] & 0xC000 == 0xC000:
            CHPStatus[0] = 0x01 #CHP in Operation
         
        else:
            CHPStatus[0] = 0x00 #CHP in Operation
            pass        
        
        #Zeitstempel Aktuelle Zeit
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
            
        sqlleistung = """INSERT INTO supervision_chprps (CHPIDGEO, CHPStartcounter, CHPbetriebsstunden, 
        CHPInoperation, CHPCMDinserttime) VALUE ('{0}', '{1}', '{2}', '{3}', 
        '{4}')""".format(scDataArray[0], scDataArray[18], scDataArray[16], CHPStatus[0], timestamp)
        #logger.info("update des Counter")
        
                
        #write informaiton to DB
        dbcom.WriteToDatabase(sqlleistung, dbhost, dbport, dbuser, dbpassword, dbdatabase)
        #logger.info("write to DB")
        
    except:
        logger.error("Unknown Failure in DeviceTemplog ")     

def DeviceStateLog(scDataArray,dbhost,dbport,dbuser,dbpassword,dbdatabase):
    #hier weiter
    """Devicelog function will insert the Starts data directly to the Database"""
    
    try:
           
        #Zeitstempel Aktuelle Zeit
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        Tempvalue = '0'
            
        sqlleistung = """INSERT INTO supervision_chpstatus (CHPIDGEO, CHPstate1, CHPstate2, 
        CHPstate3, CHPstate4, CHPstate5, CHPstate6, CHPstate7, CHPstate8, CHPstate9, CHPstate10, CHPReginsertfrom, CHPDReginserttime) VALUE ('{0}', '{1}', '{2}', '{3}', 
        '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}')""".format(scDataArray[0], scDataArray[7], scDataArray[8], scDataArray[9], scDataArray[10], scDataArray[11], scDataArray[12], scDataArray[13], Tempvalue, Tempvalue, Tempvalue, scDataArray[0], timestamp)
        #logger.info("update des Counter")
        
                
        #write informaiton to DB
        dbcom.WriteToDatabase(sqlleistung, dbhost, dbport, dbuser, dbpassword, dbdatabase)
        #logger.info("write to DB")
        
    except:
        logger.error("Unknown Failure in DeviceStatuslog ") 
    

########################################
# main function                        #
#Nur im Standalone Betrieb zu Aktivieren#
########################################

def main():
    
    mytest = []
    mytest.append(1514) #Test0
    mytest.append(0) #Test1
    mytest.append(0) #Test2
    mytest.append(3) #Test3
    mytest.append(0) #Test4
    mytest.append(0) #Test5
    mytest.append(3) #Test6
    mytest.append(0) #Test7
    mytest.append(0) #Test8
    mytest.append(0) #Test9
    mytest.append(0) #Test10
    mytest.append(0) #Test11
    mytest.append(0) #Test12
    mytest.append(0) #Test13
    mytest.append(200) #Test14
    mytest.append(200) #Test15
    mytest.append(5600) #Test16
    mytest.append(0) #Test17
    mytest.append(105) #Test18
    mytest.append(20) #Test19
    mytest.append(150) #Test20
    mytest.append(160) #Test21
    mytest.append(60) #Test22
    mytest.append(25) #Test23
    mytest.append(30) #Test24
    mytest.append(680) #Test25
    mytest.append(250) #Test26
    mytest.append(650) #Test27
    
    
    DeviceTemplog(mytest,'134.255.244.20', 3306, "django", "7qhhr5DFqkAzEpB8", "tsupervision")  
    
    # quit python script
    sys.exit(0)

if __name__ == '__main__':
    main()