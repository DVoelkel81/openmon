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
    myvalues["statusword1"]= 0
    myvalues["statusword2"]= 0
    myvalues["statusword3"]= 0
    myvalues["statusword4"]= 0
    myvalues["statusword5"]= 0
    myvalues["statusword6"]= 0
    myvalues["statusword7"]= 0
    myvalues["servicetime1"]= 0
    myvalues["servicetime2"]= 0
    myvalues["servicetime3"]= 0
    myvalues["servicetime4"]= 0
    myvalues["khwcount"]= 0
    myvalues["kvarcount"]= 0
    myvalues["runhours"]= 0
    myvalues["Alarmtext1"]= 0
    myvalues["Alarmtext2"]= 0
    myvalues["Alarmtext3"]= 0
    myvalues["Alarmtext4"]= 0
    myvalues["Alarmtext5"]= 0
    myvalues["Alarmtext6"]= 0
    myvalues["Alarmtext7"]= 0
    myvalues["Alarmtext8"]= 0
    myvalues["Alarmtext9"]= 0
    myvalues["Alarmtext10"]= 0
    myvalues["Alarmtext11"]= 0
    myvalues["Alarmtext12"]= 0
    myvalues["Alarmtext13"]= 0
    myvalues["Alarmtext14"]= 0
    myvalues["Alarmtext15"]= 0
    myvalues["Alarmtext16"]= 0
    myvalues["mode"]= 0
    myvalues["startcounter"]= 0
    myvalues["unsuccesstartcounter"]= 0
    myvalues["wastgastemppri"]= 0
    myvalues["wastgastempsec"]= 0
    myvalues["hcltemp"]= 0
    myvalues["hcctemp"]= 0
    myvalues["oiltemp"]= 0
    myvalues["exhaustgastemp"]= 0
    myvalues["motorintemp"]= 0
    myvalues["motorouttemp"]= 0
    myvalues["voltagel1"]= 0
    myvalues["voltagel2"]= 0
    myvalues["voltagel3"]= 0
    myvalues["voltage12"]= 0
    myvalues["voltage23"]= 0
    myvalues["voltage31"]= 0
    myvalues["currentl1"]= 0
    myvalues["currentl2"]= 0
    myvalues["currentl3"]= 0
    myvalues["roomtemp"]= 0
    myvalues["coolingtemp"]= 0
    myvalues["oilpressure"] = 0
    
    
    databaseserver = "134.255.244.24"
    databaseport = "8000"
    
    xmlrpcomclient.sendchp(myvalues,databaseserver,databaseport)
    """
    Transfer Data to XML-RPC Client Script
    """  


########################################
# main function                        #
#Nur im Standalone Betrieb zu Aktivieren#
########################################
def main():
    #call modbusreadclient() #and start Modbus reading
    xmltest()

    # quit python script
    sys.exit(0)
    
if __name__ == '__main__':
    main()