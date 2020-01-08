#!/usr/bin/python3
# coding: utf-8

import sys
import logging
import os
import sqlite3
import datetime
from time import *
from logging.handlers import RotatingFileHandler


#create logging folder
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log" #Windows
#logdirectory = os.path.dirname(os.path.abspath(__file__)) + "/log" #MAC

#check if folder exists
if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)


# create logger
#logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/analysis.log" #Mac
logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\analysis_rec.log" #win
logger = logging.getLogger("analysis")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#logger.addHandler(stream_handler)
logger.addHandler(handler)

def socketanalysis(data):
    newcm = []
    
    newcm.append(256*data[20] + data[21])
    newcm.append(256*data[22] + data[23])
    #logger.info(newcm[1])
    #logger.info(newcm[0])
    
    if newcm[1] == 1:
        
        #Auslesen der settings.db
        #-----------------------------------------
        try:
            #connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/settings.db") #Mac
            connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\settings.db") #Windows
            cursor = connection.cursor()
            
            sql_command = """UPDATE servercmd SET resetcmd = '1' WHERE id = '1'"""          
            #hier weiter
            #Request Gensetnumber
            #SQL_Command = """SELECT * from servercmd"""
            cursor.execute(sql_command)
            connection.commit()
            #result = cursor.fetchone()
            #gennumber = result[1]
            #result = None #release variable
            #SQL_Command = None #empty variable
            newcm = None
                       
            
        except Exception as e:
        
            logger.info("A fault occur on open sqlite database %s " % str(e))

########################################
# main function                        #
#Nur im Standalone Betrieb zu Aktivieren#
########################################
def main():
    #call modbusreadclient() #and start Modbus reading
    socketanalysis()

    # quit python script
    sys.exit(0)
    
if __name__ == '__main__':
    main()