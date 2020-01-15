#! python3
#!/usr/bin/python3
# coding: utf8

#import time
import socket
import sys
import logging
import pymysql
import datetime

#Erstellen des Datenloggers
#--------------------------------------------------

logger = logging.getLogger('initiate')
logger.setLevel(logging.DEBUG)
hdlr = logging.FileHandler('/home/supervision-script/timecalc.log')
#hdlr = logging.FileHandler('C:\\Myprograms\\test.log')
hdlr.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 

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

SQL="""SELECT CHPLastUpdate, CHPIDGEO FROM supervision_chpgeodata;"""

cur.execute(SQL)

result = cur.fetchall()

#Zerlegen des Statusbyte und vorbereitung fuer SQL
CHPStatus = bytearray(5)

#zuweisen der Bits
CHPStatus[0] = 0x00 #CHP in Operation
CHPStatus[1] = 0x00 #CHP Ready
CHPStatus[2] = 0x00 #CHP Warning
CHPStatus[3] = 0x00 #CHP Alarm
CHPStatus[4] = 0x01 #CHP Off
    
#logger.info(datetime.datetime.now())

for r in result:
    time1 = datetime.datetime.now()
    #time1 = datetime.datetime(2016, 4, 1, 17, 3, 0, 000000)
    time2 = r[0:1]
    
    time4 = time1 + datetime.timedelta(minutes = -6)


    
    if time2[0] < time4:
        #logger.info("BHKW is Disconnected")
        SQL="""UPDATE supervision_chpgeodata SET CHPConStatus = '{0}',
        CHPInoperation = '{2}', CHPReady = '{3}', CHPWarning = '{4}', CHPMalfunction = '{5}',
        CHPOff = '{6}' WHERE CHPIDGEO = '{1}'""".format("Disconnected", r[1:2][0], CHPStatus[0], CHPStatus[1], CHPStatus[2], CHPStatus[3], CHPStatus[4])
        cur.execute(SQL)
        db.commit()
        #logger.info("sql successfull transmit")
        
    else:
        #print("everything is fine")
        SQL="""UPDATE supervision_chpgeodata SET CHPConStatus = '{0}' WHERE CHPIDGEO = '{1}'""".format("Connected", r[1:2][0])
        cur.execute(SQL)
        db.commit()        

  
cur.close()
db.close() 

