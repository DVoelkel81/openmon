#!/usr/bin/python3
# coding: utf8
#Author: Dennis Voelkel
#Date: 2018-08-21 20:34
#Version: 1

#import time
import socket
import sys
import logging
import os
import pymysql
import datetime
from logging.handlers import RotatingFileHandler
#Erstellen des Datenloggers
#--------------------------------------------------

# create logger
logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/server-send-reset.log" #Mac
#logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\analysis.log" #Mac
logger = logging.getLogger("sendreset")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#logger.addHandler(stream_handler)
logger.addHandler(handler)

#check is empty
#---------------------
def is_empty(checkvalue):
    if checkvalue:
        return False
    else:
        return True
#----------------------

#initiate connection
#----------------------------------------
db = pymysql.connect(host="134.255.244.20",
                     port=3306,
                     user="django",
                    passwd="7qhhr5DFqkAzEpB8",
                    db="tsupervision")

#print ("Initate connection to Mysql Database")
#logger.info('Initate connection to Mysql Database')
cur = db.cursor()

SQL="""SELECT * FROM supervision_chpcmd WHERE CHPCMDRESET = 1;"""

cur.execute(SQL)

result = cur.fetchall()

#logger.info(len(result))
if len(result) > 0:
    
    for r in result:
    
        resetobject = r[0:3]
       # logger.info(resetobject[2])
    
        #erstellen des Sockets
        udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    
        #create array
        try:
            data = bytearray()
        
            #------------------------------
            for i in range(0,20):
                data.append(0) #byte 0 

            data.extend((int(resetobject[1])).to_bytes(2, byteorder='big'))# Genset ID byte 20 + 21
            data.extend((1).to_bytes(2, byteorder='big'))
        
    
            udpsocket.sendto(data,(resetobject[2],1203))
            

            SQL="""UPDATE supervision_chpcmd SET CHPCMDRESET = '0' WHERE CHPIDGEO = '{0}';""".format(resetobject[1])
            cur.execute(SQL)
            db.commit()
            logger.info("Reset send to K" + resetobject[1] + ". Set value in Datsbase to 0")
        
        #logger.info("Sending data to " + resetobject[2] + " Client K" + resetobject[1] + "  " + str(data[23]) )
        except Exception as e:
            logger.info("A fault occur on creating array or send to client Error %s " % str(e))
        
        udpsocket.close()    
else:
    #logger.info("nothing in Database")
    pass
    

cur.close()
db.close()
