#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = "Dennis Voelkel"
__copyright__ = "Copyright 2019, Openmon"
__credits__ = ["Dennis Voelkel"]
__license__ = "MIT"  #
__version__ = "0.0.1"
__maintainer__ = "Dennis Voelkel"
__email__ = "dennis.voelkel@outlook.com"
__status__ = "Develop"

"""Centralizing Database Communication.
"""

# Generic/Built-in
import sys
import logging
import os
import pymysql
#import psycopg2
import datetime
from logging.handlers import RotatingFileHandler

#create logging folder
#logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log" #Windows
logdirectory = os.path.dirname(os.path.abspath(__file__)) + "/log" #Linux

#check if folder exists
if not os.path.exists(logdirectory):
    os.makedirs(logdirectory)


# create logger
logPath = os.path.dirname(os.path.abspath(__file__)) + "/log/DBCom.log" #LINUX
#logPath = os.path.dirname(os.path.abspath(__file__)) + "\\log\\analysis.log" #Windows
logger = logging.getLogger("DBcommunication")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#logger.addHandler(stream_handler)
logger.addHandler(handler)

def WriteToDatabase(WTDstatement,dbhost,dbport,dbuser,dbpassword,dbdatabase):
    
    #Create SQL DB Connection
    #Postgres
    #db = psycopg2.connect(host=dbhost,
    #                         port= dbport,
    #                         user=dbuser,
    #                         password=dbpassword,
    #                         database=dbdatabase)
    #logger.info(WTDstatement)

    #MySQL
    
    db = pymysql.connect(host=dbhost,port=int(dbport),user=dbuser,passwd=dbpassword,db=dbdatabase)
      
        

    cur = db.cursor()
  
    try:

        cur.execute(WTDstatement) #Execute sql Statment
        db.commit() #Commit sql Statment
        db.close() #Close DB connection
        #logger.info("Connection Open and comit to DB, close the connection")


    except pymysql.err.DataError as e:
        db.rollback()
        logger.info(e)
        logger.info("Data Error")
        logger.info(sql)

    except pymysql.err.InternalError as e:
        db.rollback()
        # print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        logger.info(e)
        logger.info("Internal Error")
        # hier funktioniert die Error Funktion noch nicht.

    except pymysql.err.IntegrityError as e:
        db.rollback()
        logger.info(e)
        logger.info("integrity Error")

    except pymysql.err.OperationalError as e:
        db.rollback()
        logger.info(e)
        logger.info("Operation Error")

    except pymysql.err.NotSupportedError as e:
        db.rollback()
        logger.info(e)
        logger.info("NoSupport Error")

    except pymysql.err.ProgrammingError as e:
        db.rollback()
        logger.info(e)
        logger.info("Programming Error")

    except pymysql.err.Error as e:
        db.rollback()
        logger.info(e)
        logger.info("unknown Error")

########################################
# main function                        #
#Nur im Standalone Betrieb zu Aktivieren#
########################################
def main(WTDstatement):
    #call modbusreadclient() #and start Modbus reading
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    testsql = """UPDATE supervision_chpgeodata SET CHPIDGEO = '{5}',
      CHPInoperation = '{0}', CHPReady = '{1}', CHPWarning = '{2}', CHPMalfunction = '{3}',
      CHPOff = '{4}', CHPLastUpdate = '{6}', CHPDevStatus='{7}' WHERE CHPIDGEO = '{5}'""".format(1, 0, 0, 0, 0, 1541, timestamp, 'AUTO')    
    WriteToDatabase(WTDstatement,'134.255.244.20', 3306, "django", "7qhhr5DFqkAzEpB8", "tsupervision")

    # quit python script
    sys.exit(0)
    
if __name__ == '__main__':
    main()