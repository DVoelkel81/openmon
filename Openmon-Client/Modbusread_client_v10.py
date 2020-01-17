#! python3
# -*- coding: utf-8 -*-

__author__ = "Dennis Voelkel"
__copyright__ = "Copyright 2019, Openmon"
__credits__ = ["Dennis Voelkel"]
__license__ = "MIT"  #
__version__ = "0.0.10"
__maintainer__ = "Dennis Voelkel"
__email__ = "dennis.voelkel@outlook.com"
__status__ = "Released"

"""modbusread_client_v10.py will analyize the Status from the device an store it into the udp Socket
"""

import modbus_tk.modbus
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu


import serial
import time
import sys
import os
import logging
import Errormail
from logging.handlers import RotatingFileHandler
import sqlite3

import random
from socketserver import ThreadingMixIn
import xmlrpc.client
import xmlrpcomclient


#Einfügen Logging Module
#------------------------------------------
#Windows Client
#Funktioniert nicht als Exe, hier muss der Absolute Pfad hinein.
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log"

if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)
    
logPath = "c:\\temp\\log\\Modbus_TK_client.log" #Windows
#logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\Modbusclient.log" #Windows
#logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/Modbusclient.log" #linux
#logPath ="C:\\Myprograms\\Modbusclient.log"
logger = logging.getLogger("Modbusclient")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
#-----------------------------------------

#Auslesen der settings.db
#-----------------------------------------
try:
    #connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/settings.db") #linux
    connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\settings.db") #Windows
    cursor = connection.cursor()
    
    #Request Gensetnumber
    SQL_Command = """SELECT * from settings"""
    cursor.execute(SQL_Command)
    result = cursor.fetchone()
    gennumber = result[1]
    databaseserver = result[3]
    databaseport = result[4]
    result = None #release variable
    SQL_Command = None #empty variable
    
    
    
except SyntaxError:

    logger.info(SyntaxError)
#------------------------------

#Erstellen des Socket
def modbusreadclient():

    
    try:
        #Request comport settings
        SQL_Command = """SELECT * from modbuscom"""
        cursor.execute(SQL_Command)
        result = cursor.fetchone()
        #print(eval(result[5]))
        MBType = result[1]
        MBcomport = result[2]
        MBbaudrate = int(result[3])
        MBparity = result[4] #This must be an Object
        MBstopbit = int(result[5]) #this must be an object
        MBtimeout = result[6] #This must be an Object
        MBID = result[7]
        MBIpAddr = result[8]
        MBIpPort = result[9]
        MBbytes = eval(result[10])
        result = None #release variable
        SQL_Command = None #empty variable
        

        modbusconn = modbus_rtu.RtuMaster(serial.Serial(port= MBcomport, baudrate= MBbaudrate, bytesize= MBbytes, parity= MBparity, stopbits= MBstopbit, xonxoff=0))
        modbusconn.set_timeout(0.5)
        modbusconn.set_verbose(True)
 
        logger.info("connected via Modbus_TK")      
        
    except serial.SerialException as e:
        logger.info("Serial Error: {0}".format(str(e)))

        sys.exit(1) # Beendet das Script aufgrund des port Fehlers
        
    try:
        data = {}
        
        #Insert Gensetnumber
        data["deviceid"] = gennumber
        
        #Read SQl for Modbus
        
        #Request comport settings
        SQL_Command = """SELECT * from modbusregister"""
        cursor.execute(SQL_Command)
        result = cursor.fetchall()        
        #logger.info(result) 
        #result = None #release variable
        SQL_Command = None #empty variable        
                
        
        #create modbus read loop
        for myread in result:

            if myread[3] == 1:
                
                #Remeber the correct Com Port if you receive an IO Error
                stdreg = modbusconn.execute(myread[5], cst.READ_HOLDING_REGISTERS, myread[1], quantity_of_x=myread[3])
                data[myread[6]] = stdreg[0]
                stdreg = None
                
                

            elif myread[3] == 2:
                kwh = modbusconn.execute(myread[5], cst.READ_HOLDING_REGISTERS, myread[1], quantity_of_x=myread[3])
                
                mysum = (65536*kwh[0])+kwh[1]
                
                uint32 = (65535*65536)+65535
                
                if kwh[0] > 32767:
                    kwhvalue = (mysum-uint32)-1
                    
                else:
                    kwhvalue = mysum

                data[myread[6]] = kwhvalue
                kwh = None

            
        #SQL Request error exist
        try:
            SQL_Command = """SELECT * from devicestatus"""
            cursor.execute(SQL_Command)
            result = cursor.fetchone()
            #genseterror = result[2]
            nonacnwarning = result[1]
            nonacnalarm = result[2]
            actwarning = result[3]
            actalarm = result[4]
            alarmlistcount = result[5]
            SQL_Command = None # emtpy variable
            result = None #empty Variable
        except Error as e:
            logger.info("Fehler in der SQLITE Kommunikation aufgetreten. " + str(e))          
                
                
            
        if actalarm == 0 and data["statusword4"] & 0x0001 :
            
            #Read Alarm messages if alarms exists
            if myread[3] == 25:
                Alarm = modbusconn.execute(myread[5], cst.READ_HOLDING_REGISTERS, myread[1], quantity_of_x=myread[3])
                Alarmmail = []
                for Al in range(0,25,1):
                    #Alarmval = Alarm[Al]
                    #print(Alarm[Al])
                    if Alarm[Al] != 0:
                        Alarmmail.append(str((Alarm[Al]).to_bytes(2, byteorder='big').decode('latin1')))
                        Alarmval = None
                data[myread[6]] = ''.join(Alarmmail)
                Alarmmail = [] # Freigeben der Variable
                Al = None #Freigeben des Speichers
                Alarm = None#Freigeben des Speichers
                
                del Alarmmail # Löschen der Variable                
                del Al #Freigeben des Speichers
                del Alarm #Freigeben des Speichers            
            
            logger.error("Störung ist Aktiv")
            #SQL SMTP Daten
            try:
                SQL_Command = """SELECT * from mailing"""
                cursor.execute(SQL_Command)
                result = cursor.fetchone()
                smtpserver = result[1]
                smtpuser = result[2]
                smtppassword = result[3]
                smtpport = result[4]
                SQL_Command = None # emtpy variable
                result = None #empty Variable
            except Error as e:
                logger.info("Fehler in der SQLITE Kommunikation Tabelle mailinglist aufgetreten. " + str(e))
                
            #SQL SMTP Daten
            try:
                SQL_Command = """SELECT * from emaillist"""
                cursor.execute(SQL_Command)
                result = cursor.fetchall()
                sendemail = result
                SQL_Command = None # emtpy variable
                result = None #empty Variable
            except Error as e:
                logger.info("Fehler in der SQLITE Kommunikation Tabelle emaillist aufgetreten. " + str(e))                 
             

                
            for mailadresse in sendemail:
                #Errormail.sendmail(smtpserver, smtpuser, smtppassword, smtpport, mailadresse[1], "Stoerung BHKW K" + str(256*errordata[20] + errordata[21]), "Es ist eine Stoerung an BHKW " + str(256*errordata[20] + errordata[21]) + " aufgetreten. \n Folgende Meldungen sind aufgetretten \n " +
                Errormail.sendmail(smtpserver, smtpuser, smtppassword, smtpport, mailadresse[1], "Stoerung BHKW K" + data["deviceid"] + "", "Es ist eine Stoerung an BHKW " + data["deviceid"] + " aufgetreten. \n Folgende Meldungen sind aufgetretten \n " +
                                   data["Alarmtext1"] + " \n " + data["Alarmtext2"] + " \n " + data["Alarmtext3"] + " \n " + data["Alarmtext4"] + " \n " + data["Alarmtext5"] + " \n " + data["Alarmtext6"] + " \n " + 
                                   data["Alarmtext7"] + " \n " + data["Alarmtext8"] + " \n " + data["Alarmtext9"] + " \n " + data["Alarmtext10"] + " \n " + data["Alarmtext11"] + " \n " + data["Alarmtext12"] + " \n " + data["Alarmtext13"] + " \n " + 
                                   data["Alarmtext14"] + " \n " + data["Alarmtext15"] + " \n " + data["Alarmtext16"])
                time.sleep(1)

                sendemail = None #Variable leeren
                
            #SQL Request error exist
            try:
                SQL_Command = """UPDATE devicestatus SET aktalarm = '1' WHERE id = '1'"""
                cursor.execute(SQL_Command)
                connection.commit()
                SQL_Command = None # emtpy variable
                    
                SQL_Command = """UPDATE devicestatus SET aktwarning = '1' WHERE id = '1'"""
                cursor.execute(SQL_Command)
                connection.commit()
                SQL_Command = None # emtpy variable                    
                    
            except Error as e:
                logger.info("Fehler in der SQLITE Kommunikation aufgetreten, ErrorID konnte nicht auf 1 gesetzt werden." + str(e))
           
        elif actwarning == 0 and data["statusword3"] & 0x8000 :
            #Information Warnung steht an
            logger.warning("Warnung ist Aktiv")
            #Send also process data
            time.sleep(0.2)

            try:
                SQL_Command = """UPDATE devicestatus SET aktwarning = '1' WHERE id = '1'"""
                cursor.execute(SQL_Command)
                connection.commit()
                SQL_Command = None # emtpy variable
                    
            except Error as e:
                logger.info("Fehler in der SQLITE Kommunikation aufgetreten, ErrorID konnte nicht auf 1 gesetzt werden." + e)
        
            else:
                pass
           
        #uebertrage fehler ohne E-Mail    
        if actalarm == 1 and data["statusword4"] & 0x0001 :
            #Information fehler steht noch an
            logger.error("Störung ist noch Aktiv")
            time.sleep(0.2)

                
        if actwarning == 1 and data["statusword3"] & 0x8000 :
            #Information Warnung steht noch an
            logger.warning("Warnung warnung steht noch an")
            time.sleep(0.2)

                
             
        else:
            #SQL Request error exist
            try:
                if not data["statusword4"] & 0x0001:
                    SQL_Command = """UPDATE devicestatus SET aktalarm = '0' WHERE id = '1'"""
                    cursor.execute(SQL_Command)
                    connection.commit()
                    SQL_Command = None # emtpy variable
                    
                if not data["statusword3"] & 0x8000:
                    SQL_Command = """UPDATE devicestatus SET aktwarning = '0' WHERE id = '1'"""
                    cursor.execute(SQL_Command)
                    connection.commit()
                    SQL_Command = None # emtpy variable                
                
            except Error as e:
                logger.info("Fehler in der SQLITE Kommunikation aufgetreten, ErrorID konnte nicht auf 0 gesetzt werden." + str(e))            
            
            #udpsocket.sendto(data,("localhost",7777))
            
        xmlrpcomclient.sendchp(data,databaseserver,databaseport)
        """
        Transfer Data to XML-RPC Client Script
        """            


    except IOError:
        logger.info("Fehler in Modbuscommunication oder Socket konnte nicht geöffent werden")

    #connection.close()
    #Schliessen des Socket
    modbusconn.close()

    


########################################
# main function                        #
#Nur im Standalone Betrieb zu Aktivieren#
########################################
def main():
    #call modbusreadclient() #and start Modbus reading
    modbusreadclient()

    # quit python script
    sys.exit(0)
    
if __name__ == '__main__':
    main()

