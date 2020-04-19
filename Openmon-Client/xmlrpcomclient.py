#! python3
# -*- coding: utf-8 -*-

__author__ = "Dennis Voelkel"
__copyright__ = "Copyright 2019, Openmon"
__credits__ = ["Dennis Voelkel"]
__license__ = "MIT"  #
__version__ = "0.0.3"
__maintainer__ = "Dennis Voelkel"
__email__ = "dennis.voelkel@outlook.com"
__status__ = "Released"

"""
xml-rpc-client.py will send data to main Server
"""

import random
import time
import logging
import os
from socketserver import ThreadingMixIn
from logging.handlers import RotatingFileHandler
import xmlrpc.client
#from concurrent.futures import ThreadPoolExecutor, as_completed

logPath = "c:\\temp\\xml-rpc-client.log" #windows
logger = logging.getLogger("xml-rpc-omserver")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def sendchp(data,databaseserver,databaseport):
    server = xmlrpc.client.ServerProxy("https://" + databaseserver + ":" + databaseport +"/xmltest", allow_none=False, verbose=False)
   
    try:
        #logger.info(data)
        server.logchp(data)
    except xmlrpc.client.ProtocolError as err:
        logger.error("A protocol error occurred")
        logger.error("URL: %s" % err.url)
        logger.error("HTTP/HTTPS headers: %s" % err.headers)
        logger.error("Error code: %d" % err.errcode)
        logger.error("Error message: %s" % err.errmsg)
    
    except xmlrpc.client.Fault as err:
        logger.error("A fault occurred")
        logger.error("Fault code: %d" % err.faultCode)
        logger.error("Fault string: %s" % err.faultString)

#with ThreadPoolExecutor() as executor:
#    sleeps = {executor.submit(submit_sleep) for _ in range(4)}
#    for future in as_completed(sleeps):
#        sleep_time = future.result()
#        print(sleep_time)

#Runn Script
if __name__ == '__main__':
    sendchp()