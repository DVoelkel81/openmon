#! python3
# -*- coding: utf-8 -*-

#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClientserial
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
import serial
import time
import socket
import sys
import os
import logging
#import Errormail
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
    

logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\sendresetcmd.log" #Windows
#logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/Modbusclient.log" #Mac
#logPath ="C:\\Myprograms\\Modbusclient.log"
logger = logging.getLogger("sendresetcmd")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def modbussendreset():
    
    
    
    try:
        
        #connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/settings.db") #Mac
        connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\settings.db") #Windows
        cursor = connection.cursor()

        #Request for Reset command
        SQL_Command = """SELECT * from servercmd"""
        cursor.execute(SQL_Command)
        result = cursor.fetchone()
        Resetinit = result[1]
        result = None #release variable
        SQL_Command = None #empty variable
        
        if Resetinit == 1:
            #Request comport settings
            SQL_Command = """SELECT * from modbuscom"""
            cursor.execute(SQL_Command)
            result = cursor.fetchone()
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

            #Request for
        
            #if MBType == 'RTU' or 'rtu':
            modbusconn = ModbusClientserial(method=MBType, port=MBcomport, stopbits=MBstopbit, bytesize=MBbytes, parity=MBparity, baudrate=MBbaudrate)
        
            #if MBType == 'TCP' or 'tcp':
            #modbusconn = ModbusClient(MBIpAddr, port=MBIpPort)
            modbusconn.connect()
        
            #Create register builder
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)

            #comap funktionsregister
            mbresetreg1 = 6358
        
            #reset command
            builder.add_16bit_uint(0x08f7) #Anwahl reset funktion
            builder.add_16bit_uint(0x0000) #funktinsschalter client
            builder.add_16bit_uint(0x0001) #setze reset bit comap
            mbresetcmd = builder.to_registers()
        
            #write reset
            rq = modbusconn.write_registers(mbresetreg1, mbresetcmd, unit=1)
            logger.info("Send Reset command to controller")
            #print ("command send "  + str(rq))
            if rq.isError() == True:
                logger.error(str(rq))
                registererror = builder.build()
                logger.error("Error in command adress: " + str(mbresetreg1) + " register: " + str(registererror) + " unit: 1")
            else:
                pass
        
            #empty Variable
            builder.reset()
        
            modbusconn.close()
            #print("connection closed")

            #datenbankfeld zurueck setzen
            sql_command = """UPDATE servercmd SET resetcmd = '0' WHERE id = '1'"""          
            cursor.execute(sql_command)
            connection.commit()

        else:
            pass

        cursor.close()
        connection.close()
        
    except serial.SerialException as e:
        logger.info("Serial Error: {0}".format(str(e)))

        sys.exit(1) # Beendet das Script aufgrund des port Fehlers    


########################################
# main function                        #
#Nur im Standalone Betrieb zu Aktivieren#
########################################
def main():
    #call modbusreadclient() #and start Modbus reading
    modbussendreset()

    # quit python script
    sys.exit(0)
    
if __name__ == '__main__':
    main()