#! python3
# -*- coding: utf-8 -*-

__author__ = "Dennis Voelkel"
__copyright__ = "Copyright 2019, Openmon"
__credits__ = ["Dennis Voelkel"]
__license__ = "MIT"  #
__version__ = "0.0.1"
__maintainer__ = "Dennis Voelkel"
__email__ = "dennis.voelkel@outlook.com"
__status__ = "Develop"

"""
xml-rpc-client.py will send data to main Server
"""

#import systemlib
import time
import sys
import os
import random
#import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from socketserver import ThreadingMixIn

#Import custom lib
import xmlrpc.client
import xmlrpcomclient

def xmltest():
    """
    Test of XML Transmitted Values to Server
    """
    
    myvalues = {}

    myvalues["deviceid_id"] = "5668c90a-80ed-4b7b-a467-f4d9789982fb"
    myvalues["deviceid"] = 1719
    myvalues["statusword1"]= 30201
    myvalues["statusword2"]= 30202
    myvalues["statusword3"]= 30203
    myvalues["statusword4"]= 30203
    myvalues["statusword5"]= 30204
    myvalues["statusword6"]= 30205
    myvalues["statusword7"]= 30206
    myvalues["servicetime1"]= 12001
    myvalues["servicetime2"]= 12002
    myvalues["servicetime3"]= 12003
    myvalues["servicetime4"]= 12004
    myvalues["khwcount"]= 35
    myvalues["kvarcount"]= 2
    myvalues["runhours"]= 235
    myvalues["Alarmtext1"]= "Alarm1"
    myvalues["Alarmtext2"]= "Alarm2"
    myvalues["Alarmtext3"]= "Alarm3"
    myvalues["Alarmtext4"]= "Alarm4"
    myvalues["Alarmtext5"]= "Alarm5"
    myvalues["Alarmtext6"]= "Alarm6"
    myvalues["Alarmtext7"]= "Alarm7"
    myvalues["Alarmtext8"]= "Alarm8"
    myvalues["Alarmtext9"]= "Alarm9"
    myvalues["Alarmtext10"]= "Alarm10"
    myvalues["Alarmtext11"]= "Alarm11"
    myvalues["Alarmtext12"]= "Alarm12"
    myvalues["Alarmtext13"]= "Alarm13"
    myvalues["Alarmtext14"]= "Alarm14"
    myvalues["Alarmtext15"]= "Alarm15"
    myvalues["Alarmtext16"]= "Alarm16"
    myvalues["mode"]= 3
    myvalues["startcounter"]= 14
    myvalues["unsuccesstartcounter"]= 2
    myvalues["wastgastemppri"]= 750
    myvalues["wastgastempsec"]= 752
    myvalues["hcltemp"]= 71
    myvalues["hcctemp"]= 61
    myvalues["oiltemp"]= 85
    myvalues["exhaustgastemp"]= 650
    myvalues["motorintemp"]= 70
    myvalues["motorouttemp"]= 750
    myvalues["voltagel1"]= 230
    myvalues["voltagel2"]= 231
    myvalues["voltagel3"]= 232
    myvalues["voltage12"]= 400
    myvalues["voltage23"]= 401
    myvalues["voltage31"]= 402
    myvalues["currentl1"]= 120
    myvalues["currentl2"]= 121
    myvalues["currentl3"]= 122
    myvalues["roomtemp"]= 23
    myvalues["coolingtemp"]= 75
    myvalues["oilpressure"] = 8
    
    
    databaseserver = "134.255.244.24"
    databaseport = "8000"

    
    xmlrpcomclient.sendchp(myvalues,databaseserver,databaseport)
    xmlrpcomclient
    print("is running")

    """
    Transfer Data to XML-RPC Client Script
    """  


########################################
# main function                        #
#Nur im Standalone Betrieb zu Aktivieren#
########################################
def main():
    #call modbusreadclient() #and start Modbus reading
    #xmltest()
    
    with ThreadPoolExecutor() as executor:
        sleeps = {executor.submit(xmltest) for _ in range(1)}
        for future in as_completed(sleeps):
            sleep_time = future.result()
            print(sleep_time)    
    
    #try:
        
        #for x in range(2):
            ##data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            ##logger.info(len(data))
            #t = threading.Thread(name='xmltest', target=xmltest)
            #t.setDaemon(True)
            #t.start()
            ##print("is running")
            #data = None

       
    #except Exception as e:
        
        #print('Error in Array or analysis function!')
        #print(type(e))
        #print(e.args)
        #print(e)
        #data = None
        #pass     

    # quit python script
    sys.exit(0)
    
if __name__ == '__main__':
    main()