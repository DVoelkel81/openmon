#! python3
# -*- coding: utf-8 -*-

#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClientserial

import serial
import time
import socket
import sys
import os
import logging
import Errormail
from logging.handlers import RotatingFileHandler
#from xml.dom import minidom
import sqlite3


#Einfügen Logging Module
#------------------------------------------
#Windows Client
#Funktioniert nicht als Exe, hier muss der Absolute Pfad hinein.
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log"

if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)
    

logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\Modbusclient.log" #Windows
#logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/Modbusclient.log" #Mac
#logPath ="C:\\Myprograms\\Modbusclient.log"
logger = logging.getLogger("Modbusclient")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
#-----------------------------------------

#Auslesen der settings.xml
#-----------------------------------------
#xmldoc = minidom.parse(os.path.dirname(os.path.abspath(__file__)) + "\\settings.xml") #WINDOWSFunktioniert nicht als Exe, hier muss der Absolute Pfad hinein
#xmldoc = minidom.parse(os.path.dirname(os.path.abspath(__file__)) + "/settings.xml") #MACOSFunktioniert nicht als Exe, hier muss der Absolute Pfad hinein
#itemlist = xmldoc.getElementsByTagName('gensetnumber')
#gennumber = itemlist[0].childNodes[0].nodeValue
#-----------------------------------------

#Auslesen der settings.db
#-----------------------------------------
try:
    #connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/settings.db") #Mac
    connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\settings.db") #Windows
    cursor = connection.cursor()
    
    #Request Gensetnumber
    SQL_Command = """SELECT * from settings"""
    cursor.execute(SQL_Command)
    result = cursor.fetchone()
    gennumber = result[1]
    result = None #release variable
    SQL_Command = None #empty variable
    
    
    
except SyntaxError:

    logger.info(SyntaxError)
#------------------------------

#Erstellen des Socket
def modbusreadclient():
    #erstellen des Sockets
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    #print("socket OK")
    
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
        
        #if MBType == 'RTU' or 'rtu':
        modbusconn = ModbusClientserial(method=MBType, port=MBcomport, stopbits=MBstopbit, bytesize=MBbytes, parity=MBparity, baudrate=MBbaudrate)
        
        #if MBType == 'TCP' or 'tcp':
        #modbusconn = ModbusClient(MBIpAddr, port=MBIpPort)
        modbusconn.connect()
        
        #Clean Variables
        #MBcomport = None
        #MBbaudrate = None
        #MBparity = None
        #MBstopbit = None
        #MBtimeout = None        

        
    except serial.SerialException as e:
        logger.info("Serial Error: {0}".format(str(e)))

        sys.exit(1) # Beendet das Script aufgrund des port Fehlers
        
    try:
        data = bytearray()
        errordata = bytearray()
        
        #Read SQl for Modbus
        
        #Request comport settings
        SQL_Command = """SELECT * from modbusregister"""
        cursor.execute(SQL_Command)
        result = cursor.fetchall()        
        #logger.info(result) 
        #result = None #release variable
        SQL_Command = None #empty variable        
                
        #Erzeugt eine Forschleife für die ersten 20 byte um mit dem codesysprotocoll conform zu bleiben
            
        #------------------------------
        for i in range(0,20):
            data.append(0) #byte 0
            errordata.append(0) #byte = 0
        #------------------------------
        data.extend((int(gennumber)).to_bytes(2, byteorder='big'))# Genset ID byte 20 + 21
        
        #create modbus read loop
        for myread in result:
            if myread[3] == 1:
                
                #Remeber the correct Com Port if you receive an IO Error
                test99 = modbusconn.read_holding_registers(myread[1], myread[3], unit=0x01)
                test100 = test99.registers[0]
                test99 = None
                #print(test100)
                data.extend((test100).to_bytes(2, byteorder='big'))
                #logger.info(myread[3])

            elif myread[3] == 2:
                kwh = modbusconn.read_holding_registers(myread[1], myread[3], unit=0x01)# kWh erzeugt
                kwhval1 = kwh.registers[0]
                kwhval2 = kwh.registers[1]
                #print(kwhval1)
                #print(kwhval2)
                data.extend((kwhval1).to_bytes(2, byteorder='big')) #
                data.extend((kwhval2).to_bytes(2, byteorder='big')) # 
                kwhval1 = None
                kwhval2 = None
                kwh = None
                
        #logger.info(data)        
        #data.extend((modbusconn.read_register(129,0,3)).to_bytes(2, byteorder='big')) # Logbout1 byte 22 + 23
        #data.extend((modbusconn.read_register(130,0,3)).to_bytes(2, byteorder='big')) # Logbout2 byte 24 + 25
        #data.extend((modbusconn.read_register(131,0,3)).to_bytes(2, byteorder='big')) # Logbout3 byte 26 + 27
        #data.extend((modbusconn.read_register(132,0,3)).to_bytes(2, byteorder='big')) # Logbout4 byte 28 + 29
        #data.extend((modbusconn.read_register(133,0,3)).to_bytes(2, byteorder='big')) # Logbout5 byte 30 + 31
        #data.extend((modbusconn.read_register(134,0,3)).to_bytes(2, byteorder='big')) # Logbout6 byte 32 + 23
        #data.extend((modbusconn.read_register(135,0,3)).to_bytes(2, byteorder='big')) # Logbout7 byte 34 + 35
        #data.extend((modbusconn.read_register(3590,0,3)).to_bytes(2, byteorder='big')) # Service Timer 1 byte 36 + 37
        #data.extend((modbusconn.read_register(3591,0,3)).to_bytes(2, byteorder='big')) # Service Timer 2 byte 38 + 39
        #data.extend((modbusconn.read_register(3592,0,3)).to_bytes(2, byteorder='big')) # Service Timer 3 byte 40 + 41
        #data.extend((modbusconn.read_register(3593,0,3)).to_bytes(2, byteorder='big')) # Servier Timer 4 byte 42 + 43
                
        #konverttierung kwh 4 register byte 44 + 45 + 46 + 47
        #kwh = modbusconn.read_registers(3594,2,3)# kWh erzeugt
        #data.extend((kwh[0]).to_bytes(2, byteorder='big')) #
        #data.extend((kwh[1]).to_bytes(2, byteorder='big')) #
            
        #konverttierung kvah 4 register byte 48 + 49 + 50+ 51
        #kvah = modbusconn.read_registers(3596,2,3)# kVAh erzeug
        #data.extend((kvah[0]).to_bytes(2, byteorder='big')) #
        #data.extend((kvah[1]).to_bytes(2, byteorder='big')) #3
             
        #konverttierung kvah 4 register byte 52 + 53 + 54 + 55
        #runhours = modbusconn.read_registers(3586,2,3)# Run hours erzeugt
        #data.extend((runhours[0]).to_bytes(2, byteorder='big')) #
        #data.extend((runhours[1]).to_bytes(2, byteorder='big')) 
            
        #read List of Mode byte 56 + 57
        #data.extend((modbusconn.read_register(3026,0,3)).to_bytes(2, byteorder='big')) #
        #print(data)
            
        if data[26] & 0x80 or data[29] & 0x01:
            errordata[8] = 0x00
            errordata[9] = 0x02
            
            errordata.extend((int(gennumber)).to_bytes(2, byteorder='big'))# Genset ID byte 20 + 21
       
            
            Alarm = modbusconn.read_holding_registers(6668,25, unit=0x01) # Alarm Text Line 1
            Alarmmail = []
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm1 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm1)
            Alarmmail = [] # Freigeben der Variable
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers
            
            Alarm = modbusconn.read_holding_registers(6693,25, unit=0x01) # Alarm Text Line 2 
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm2 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm2)
            Alarmmail = [] # Freigeben der Variable                
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers
            
            Alarm = modbusconn.read_holding_registers(6718,25, unit=0x01) # Alarm Text Line 3
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm3 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm3)
            Alarmmail = [] # Löschen der Variable                 
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers    
           
            Alarm = modbusconn.read_holding_registers(6743,25, unit=0x01) # Alarm Text Line 4
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm4 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm4)
            Alarmmail = [] # Löschen der Variable                 
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers       
            
            Alarm = modbusconn.read_holding_registers(6768,25, unit=0x01) # Alarm Text Line 5
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm5 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm5)
            Alarmmail = [] # Löschen der Variable                 
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers        
        
            Alarm = modbusconn.read_holding_registers(6793,25, unit=0x01) # Alarm Text Line 6
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm6 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm6)
            Alarmmail = [] # Löschen der Variable                 
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers
        
            Alarm = modbusconn.read_holding_registers(6818,25, unit=0x01) # Alarm Text Line 7
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm7 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm7)
            Alarmmail = [] # Löschen der Variable                 
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers        
        
            Alarm = modbusconn.read_holding_registers(6843,25, unit=0x01) # Alarm Text Line 8
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm8 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm8)
            Alarmmail = [] # Löschen der Variable                 
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers 
        
            Alarm = modbusconn.read_holding_registers(6868,25, unit=0x01) # Alarm Text Line 9
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm9 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm9)
            Alarmmail = [] # Löschen der Variable                 
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers 
            
            Alarm = modbusconn.read_holding_registers(6893,25, unit=0x01) # Alarm Text Line 10
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm10 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm10)
            Alarmmail = [] # Löschen der Variable                 
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers 
        
            Alarm = modbusconn.read_holding_registers(6918,25, unit=0x01) # Alarm Text Line 11
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm11 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm11)
            Alarmmail = [] # Löschen der Variable                
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers 
        
            Alarm = modbusconn.read_holding_registers(6943,25, unit=0x01) # Alarm Text Line 12
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm12 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm12)
            Alarmmail = [] # Löschen der Variable                
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers
        
            Alarm = modbusconn.read_holding_registers(6968,25, unit=0x01) # Alarm Text Line 13
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm13 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm13)
            Alarmmail = [] # Löschen der Variable                
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers
        
            Alarm = modbusconn.read_holding_registers(6993,25, unit=0x01) # Alarm Text Line 14
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm14 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm14)
            Alarmmail = [] # Löschen der Variable                
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers
            
            Alarm = modbusconn.read_holding_registers(7018,25, unit=0x01) # Alarm Text Line 15
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm15 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm15)
            Alarmmail = [] # Löschen der Variable                
            Al = None #Freigeben des Speichers
            Alarm = None#Freigeben des Speichers
             
            Alarm = modbusconn.read_holding_registers(7043,25, unit=0x01) # Alarm Text Line 16
            for Al in range(0,25,1):
                Alarmval = Alarm.registers[Al]
                errordata.extend((Alarmval).to_bytes(2, byteorder='big'))
                if Alarmval != 0:
                    Alarmmail.append(str((Alarmval).to_bytes(2, byteorder='big').decode('latin1')).replace('\x00',''))
                Alarmval = None
            genalarm16 = ''.join(str(e) for e in Alarmmail)
            #logger.info(genalarm16)
            del Alarmmail # Löschen der Variable                
            del Al #Freigeben des Speichers
            del Alarm #Freigeben des Speichers
            
            #SQL Request error exist
            try:
                SQL_Command = """SELECT * from settings"""
                cursor.execute(SQL_Command)
                result = cursor.fetchone()
                genseterror = result[2]
                SQL_Command = None # emtpy variable
                result = None #empty Variable
            except Error as e:
                logger.info("Fehler in der SQLITE Kommunikation aufgetreten. " + e)          
                
                
            
            if genseterror == 0 and data[29] & 0x01 :
                
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
                    logger.info("Fehler in der SQLITE Kommunikation aufgetreten. " + e)                
             
                udpsocket.sendto(errordata,("10.8.0.1",1202))
                time.sleep(0.2)
                
                #Information fehler steht an
                data[8] = 0x00
                data[9] = 0x01
                
                udpsocket.sendto(data,("10.8.0.1",1202))
                #Errormail.sendmail("stoerung@tuxhorn-blockheizkraftwerke.de", "Stoerung BHKW K" + str(test[0]), "Es ist eine Stoerung an BHKW " + str(test[0]) + " aufgetreten.")
                Errormail.sendmail(smtpserver,smtpuser,smtppassword, smtpport, "service@tuxhorn-blockheizkraftwerke.de", "Stoerung BHKW K" + str(256*errordata[20] + errordata[21]), "Es ist eine Stoerung an BHKW " + str(256*errordata[20] + errordata[21]) + " aufgetreten. \n Folgende Meldungen sind aufgetretten \n " +
                                   genalarm1 + " \n " + genalarm2 + " \n " + genalarm3 + " \n " + genalarm4 + " \n " + genalarm5 + " \n " + genalarm6 + " \n " + 
                                   genalarm7 + " \n " + genalarm8 + " \n " + genalarm9 + " \n " + genalarm10 + " \n " + genalarm11 + " \n " + genalarm12 + " \n " + genalarm13 + " \n " + 
                                   genalarm14 + " \n " + genalarm15 + " \n " + genalarm16)
                
                #SQL Request error exist
                try:
                    SQL_Command = """UPDATE settings SET genseterror = '1' WHERE id = '1'"""
                    cursor.execute(SQL_Command)
                    connection.commit()
                    SQL_Command = None # emtpy variable
                    
                except Error as e:
                    logger.info("Fehler in der SQLITE Kommunikation aufgetreten, ErrorID konnte nicht auf 1 gesetzt werden." + e)
           
            elif genseterror == 0 and data[26] & 0x80 :
                #Information fehler steht an
                data[8] = 0x00
                data[9] = 0x01            
                #Send also process data
                udpsocket.sendto(errordata,("10.8.0.1",1202))
                time.sleep(0.2)
                udpsocket.sendto(data,("10.8.0.1",1202))
                try:
                    SQL_Command = """UPDATE settings SET genseterror = '1' WHERE id = '1'"""
                    cursor.execute(SQL_Command)
                    connection.commit()
                    SQL_Command = None # emtpy variable
                    
                except Error as e:
                    logger.info("Fehler in der SQLITE Kommunikation aufgetreten, ErrorID konnte nicht auf 1 gesetzt werden." + e)
           
           
            #uebertrage fehler ohne E-Mail    
            elif genseterror == 1 and data[29] & 0x01 :
                #Information fehler steht an
                data[8] = 0x00
                data[9] = 0x01            
                #Send also process data
               # udpsocket.sendto(errordata,("10.8.0.1",1202))
                time.sleep(0.2)
                udpsocket.sendto(data,("10.8.0.1",1202))
                
            elif genseterror == 1 and data[26] & 0x80 :
                #Information fehler steht an
                data[8] = 0x00
                data[9] = 0x01            
                #Send also process data
                #udpsocket.sendto(errordata,("10.8.0.1",1202))
                time.sleep(0.2)
                udpsocket.sendto(data,("10.8.0.1",1202))
                
            else:
                pass
            
             
        else:
            #SQL Request error exist
            try:
                if not data[29] & 0x01:
                    SQL_Command = """UPDATE settings SET genseterror = '0' WHERE id = '1'"""
                    cursor.execute(SQL_Command)
                    connection.commit()
                    SQL_Command = None # emtpy variable
                
            except Error as e:
                logger.info("Fehler in der SQLITE Kommunikation aufgetreten, ErrorID konnte nicht auf 0 gesetzt werden." + e)            
            
            udpsocket.sendto(data,("10.8.0.1",1202))
    


    except IOError:
        logger.info("Fehler in Modbuscommunication oder Socket konnte nicht geöffent werden")

    #connection.close()
    #Schliessen des Socket
    modbusconn.close()
    udpsocket.close()
    


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

