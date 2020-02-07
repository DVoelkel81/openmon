#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = "Dennis Voelkel"
__copyright__ = "Copyright 2019, Openmon"
__credits__ = ["Dennis Voelkel"]
__license__ = "MIT"  #
__version__ = "0.0.2"
__maintainer__ = "Dennis Voelkel"
__email__ = "dennis.voelkel@outlook.com"
__status__ = "Develop"

"""Centralizing Database Communication.
"""

# Generic/Built-in
import sys
import logging
import os
import psycopg2
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

def WriteToDatabase(WTDstatement,dbhost,dbport,dbuser,dbpassword,dbdatabase,fromfunction):
    """WriteToDatabase is a global function to write data to SQL database, 
    so that the SQL creation code not must insert in every required function..
    
    :param WTDstatement: The dict contains the complete CHP data from CHP
    :type WTDstatement: string
    
    :param dbhost: IP-Address or domain fromt the Server
    :type dbhost: string
    
    :param dbhost: IP-Address or domain fromt the Database Server
    :type dbhost: string
    
    :param dbuser: Database username
    :type dbuser: string
    
    :param dbpassword: Database user password
    :type dbpassword: string
    
    :param dbdatabase: Databasename
    :type dbdatabase: string
    
    :param dbdatabase: fromfunction
    :type dbdatabase: string
    
    :returns: Nothing
    :rtype: Nothing
    
    """    
    
    #Create SQL DB Connection
    #Postgres
    db = psycopg2.connect(host=dbhost,
                             port= dbport,
                             user=dbuser,
                             password=dbpassword,
                             database=dbdatabase)
    #logger.info(WTDstatement)

    #MySQL
    #db = pymysql.connect(host=dbhost,port=int(dbport),user=dbuser,passwd=dbpassword,db=dbdatabase)
      
        

    cur = db.cursor()
  
    try:

        cur.execute(WTDstatement) #Execute sql Statment
        db.commit() #Commit sql Statment
        db.close() #Close DB connection
        #logger.info("Connection Open and comit to DB, close the connection")

    except psycopg2.InterfaceError as e:
    #except pymysql.err.DataError as e:
        db.rollback()
        logger.info(e.pgerror)
        logger.info("InterfaceError")
        logger.info(e)
        logger.info(WTDstatement)
        logger.info(fromfunction)
        

    except psycopg2.DatabaseError as e:
    #except pymysql.err.DataError as e:
        db.rollback()
        logger.info(e.pgerror)
        logger.info("DatabaseError")
        logger.info(e)
        logger.info(WTDstatement)
        logger.info(fromfunction)

    except psycopg2.DataError as e:
    #except pymysql.err.DataError as e:
        db.rollback()
        logger.info(e.pgerror)
        logger.info("Data Error")
        logger.info(e)
        logger.info(WTDstatement)
        logger.info(fromfunction)
        
    except psycopg2.InternalError as e:
    #except pymysql.err.InternalError as e:
        db.rollback()
        # print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        logger.info(e.pgerror)
        logger.info("Internal Error")
        logger.info(e)
        logger.info(fromfunction)
        # hier funktioniert die Error Funktion noch nicht.

    except psycopg2.IntegrityError as e:
    #except pymysql.err.IntegrityError as e:
        db.rollback()
        logger.info(e.pgerror)
        logger.info("integrity Error")
        logger.info(e)
        logger.info(fromfunction)

    except psycopg2.OperationalError as e:
    #except pymysql.err.OperationalError as e:
        db.rollback()
        logger.info(e.pgerror)
        logger.info("Operation Error")
        logger.info(e)
        logger.info(fromfunction)

    except psycopg2.NotSupportedError as e:
    #except pymysql.err.NotSupportedError as e:
        db.rollback()
        logger.info(e.pgerror)
        logger.info("NoSupport Error")
        logger.info(e)
        logger.info(fromfunction)

    except psycopg2.ProgrammingError as e:
    #except pymysql.err.ProgrammingError as e:
        db.rollback()
        logger.info(e.pgerror)
        logger.info("Programming Error")
        logger.info(e)
        logger.info(fromfunction)

    except psycopg2.Error as e:
    #except pymysql.err.Error as e:
        db.rollback()
        logger.info(e.pgerror)
        logger.info("unknown Error")
        logger.info(e)
        logger.info(fromfunction)
    
    finally:
        WTDstatement = None

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
    WriteToDatabase(WTDstatement,'xxx.xxx.xxx.xxx', 3306, "xxx", "xxx", "xxx")

    # quit python script
    sys.exit(0)
    
if __name__ == '__main__':
    main()