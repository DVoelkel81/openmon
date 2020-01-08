#!/usr/bin/python3
# coding: utf-8


import dataanalysis
import threading
import socket
import sys
import os
import time
import logging
from logging.handlers import RotatingFileHandler

#create logging folder
#logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log" #Windows
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "/log" #MAC

#check if folder exists
if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)
    

# create logger
logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/mythreating.log" #Mac
logger = logging.getLogger("mythreating")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#logger.addHandler(stream_handler)
logger.addHandler(handler)


#create UDP Socket*
#---------------------------------------------------
UDP_IP = '' #Hier keine Adresse eintragen, damit der Broadcast empfangen werden kann. Keine Bindung zu einer IP-Addresse.
UDP_PORT = 1202 #Codesys  Port im Netzwerk
#print ("1 - IP and Port Set")
#logger.info('1 - IP and Port Set')

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#logger.info('1 - Socket Initiated')

clientaddr = (UDP_IP, UDP_PORT) # Variable um IP-Addresse und Port Festzulegen.

#logger.info('2 -  Client Adress Set')

sock.bind(clientaddr) # Binden der IP und des Ports an das Socket.

#logger.info('3 -  Bind SocketAdress to IP')
logger.info('Script gestartet')

#Abfrage der 
while True:
    
    try:

        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        #logger.info(len(data))
        t = threading.Thread(name='dataanalysis', target=dataanalysis.socketanalysis, args=(data,))
        t.setDaemon(True)
        t.start()
        data = None

       
    except:
        logger.info('Error in Array or analysis function!')
        data = None
        pass
