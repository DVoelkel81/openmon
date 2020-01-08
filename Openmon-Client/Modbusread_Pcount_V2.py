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
from datetime import datetime, date, time, timedelta
from logging.handlers import RotatingFileHandler
import sqlite3

#Windows Client
#Funktioniert nicht als Exe, hier muss der Absolute Pfad hinein.
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log" #Windows
#logdirectory = os.path.dirname(os.path.abspath(__file__)) + "/log" #MAC

if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)
    

logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\Pcount.log" #Windows
#logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/Modbusclient.log" #Mac
#logPath ="C:\\Myprograms\\Modbusclient.log"
logger = logging.getLogger("Pcount")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
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
def ModbusPcount():

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
        
    except serial.SerialException as e:
        logger.info("Serial Error: {0}".format(str(e)))

        sys.exit(1) # Beendet das Script aufgrund des port Fehlers
    
    try:
        data = bytearray()
            
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
        #------------------------------
        data.extend((int(gennumber)).to_bytes(2, byteorder='big'))# Genset ID byte 20 + 21
        
        #create modbus read loop

        for myread in result:
            if myread[3] == 1:
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
                    
        #Vorbereiten für Datacount, Wert 3 für Datacount
        data[8] = 0x00
        data[9] = 0x03            
        
        #logger.info(data)  
        udpsocket.sendto(data,("10.8.0.1",1202))
        
    except:
        logger.info("Fehler im Script")

    modbusconn.close()
    udpsocket.close()
    connection.close()

def StartPcount():
    
    #connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/settings.db") #Mac
    connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\settings.db") #Windows
    cursor = connection.cursor()
    
    #Request Timestamp pcount
    SQL_Command = """SELECT * from timestampe"""
    cursor.execute(SQL_Command)
    result = cursor.fetchone()
    PcountTimestamp = datetime.strptime(result[1],'%Y-%m-%d %H:%M:%S')
    result = None #release variable
    SQL_Command = None #empty variable
    #connection.close()# Schliessen der Datenbankverbindung                
    ActTime = datetime.now()
    connection.close()
    
    if PcountTimestamp < ActTime:
        
        #Run Pcountscript
        ModbusPcount()
        
        #Set Actual date + 24h
        newtime = datetime.combine(date.today(),time(5,00))
        newtime = newtime + timedelta(days = 1)

        connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\settings.db") #Windows
        #connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/settings.db") #Windows
        cursor = connection.cursor()
        SQL_Command = """UPDATE timestampe SET updatetime = '{0}' WHERE id = '1'""".format(newtime)
        cursor.execute(SQL_Command)
        connection.commit()
        SQL_Command = None # emtpy variable
        connection.close()
        
    else:
        pass    

########################################
# main function                        #
#Nur im Standalone Betrieb zu Aktivieren#
########################################
def main():
    #call modbusreadclient() #and start Modbus reading
    StartPcount()

    # quit python script
    sys.exit(0)
    
if __name__ == '__main__':
    main()
        
            
