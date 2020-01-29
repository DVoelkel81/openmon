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


        
def chpdatalog(data,dbhost,dbport,dbuser,dbpassword,dbdatabase):
    """chpdatalog function will insert the CHP data directly to the Database.
    Some states will be decode from interger values that contains the states from the CHP,
    analog values will also stored in the databese, all values inside of dict data will transfert.
    
    :param data: The dict contains the complete CHP data from CHP
    :type data: dict
    
    :param dbhost: IP-Address or domain fromt the Server
    :type dbhost: string
    
    :param dbhost: IP-Address or domain fromt the Database Server
    :type dbhost: string
    
    :param dbuser: Database username
    :type dbuser: string
    
    :param dbpassword: Database user password
    :type dbpassword: string
    
    :param dbdatabase: Databasename
    :type dbdatabase: string
    
    :returns: Nothing
    :rtype: Nothing
    
    """    
    
    #decode Statuswords for SQL entry
    CHPStatus = bytearray(5)

    #Genset is Ready
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

    #Actual CHP operation mode
    if data["mode"] == 0x00:
        CHPStatus[0] = 0x00 #CHP in Operation
        CHPStatus[1] = 0x00 #CHP Ready
        CHPStatus[2] = 0x00 #CHP Warning
        CHPStatus[3] = 0x00 #CHP Alarm
        CHPStatus[4] = 0x01 #CHP Off
        
    else:
        pass


    #Analyse Genset Mode
    if data["mode"] == 0x00: #Genset in off mode
        CHPdevstatusoff = 1
        
    elif data["mode"] == 0x01: #Genset in manual mode
        CHPdevstatusman = 1
        
    elif data["mode"] == 0x03:#genset in auto mode
        CHPdevstatusauto = 1    
    
    #Status of GBC
    if data["statusword4"] & 0x0001 == 0x0001:
        GCBstatus = 0x01 # GCB Status is closed
    else:
        GCBstatus = 0x00 # GCB Status is open
        
    
    if data["statusword4"] & 0x0002 == 0x0002:
        MCBstatus = 0x01 # GCB Status is closed
    else:
        MCBstatus = 0x00 # GCB Status is open
        
    
    try:
        
        #Actual timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
            
        sqlchpdatalog = """INSERT INTO supervision_chptemperature (deviceid, hcltemp, hcctemp, 
        boilertoptemp, boilermidtemp, boilerbuttemp, coolingtemp, motorintemp, motorouttemp, wastgastemppri, wastgastempsec, 
        oiltemp, oilpressure, exhaustgastemp, voltagel1, voltagel2, voltagel3, voltage12, voltage23, voltage31, currentl1, currentl2, currentl3, startcounter, unsuccesstartcounter,
        runhours, khwcount, kvarcount, stateerror, statewarning, staterunning, statestop, modeauto, modeman, modestop, gcbstate, mcbstate, modepowerderate, inserttime) VALUE ('{0}',
        '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '{20}',
        '{21}', '{22}', '{23}', '{24}', '{25}', '{26}', '{27}', '{28}', '{29}', '{30}', '{31}', '{32}', '{33}', '{34}', '{35}', '{36}', '{37}', '{38}'
        )""".format(data["deviceid"], data["hcltemp"], data["hcctemp"], 0, 0, 0, data["coolingtemp"], data["motorintemp"], data["motorouttemp"], data["wastgastemppri"], data["wastgastempsec"],
                    data["oiltemp"], data["oilpressure"], data["exhaustgastemp"], data["voltagel1"], data["voltagel2"], data["voltagel3"], data["voltage12"], data["voltage23"], data["voltage31"],
                    data["currentl1"], data["currentl2"], data["currentl3"], data["startcounter"], data["unsuccesstartcounter"], data["runhours"], data["khwcount"], data["kvarcount"],
                    CHPStatus[3], CHPStatus[2], CHPStatus[0], CHPStatus[4], CHPdevstatusauto, CHPdevstatusman, CHPdevstatusoff, GCBstatus,
                    MCBstatus, 0,timestamp)
        
                
        #write informaiton to DB
        dbcom.WriteToDatabase(sqlchpdatalog, dbhost, dbport, dbuser, dbpassword, dbdatabase)
        
    except:
        logger.error("Unknown Failure in chpdatalog ")     
        

def DeviceStateLog(data,dbhost,dbport,dbuser,dbpassword,dbdatabase):

    """DeviceStateLog function will insert the status from every device separate to the database.
    
    :param data: The dict contains the complete CHP data from CHP
    :type data: dict
    
    :param dbhost: IP-Address or domain fromt the Server
    :type dbhost: string
    
    :param dbhost: IP-Address or domain fromt the Database Server
    :type dbhost: string
    
    :param dbuser: Database username
    :type dbuser: string
    
    :param dbpassword: Database user password
    :type dbpassword: string
    
    :param dbdatabase: Databasename
    :type dbdatabase: string
    
    :returns: Nothing
    :rtype: Nothing
    
    """  
    
    try:
           
        #Actual timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        Tempvalue = '0'
            
        sqlleistung = """INSERT INTO supervision_devicestateLog (deviceid, state1, state2, 
        state3, state4, state5, state6, state7, state8, state9, state10, insertby, inserttime) VALUE ('{0}', '{1}', '{2}', '{3}', 
        '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}')""".format(data["deviceid"], data["statusword1"], data["statusword2"], data["statusword3"], data["statusword4"], data["statusword5"], data["statusword6"], data["statusword7"], Tempvalue, Tempvalue, Tempvalue, data["deviceid"], timestamp)
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