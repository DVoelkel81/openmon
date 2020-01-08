import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import configparser
import os
import inspect
import logging
import time
from logging.handlers import RotatingFileHandler



class AppServerSvc (win32serviceutil.ServiceFramework):  
    _svc_name_ = "GensetTransmit"
    _svc_display_name_ = "Genset Transmit"
    _svc_description_ = "Die Aufgabe des Service ist die Abfrage der Gensecontroller via Modbus und die Uebertragung via UDP Socket"

    _config = configparser.ConfigParser()

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
        self._config.read(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/config.ini')
        print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/teconfig.ini')

        print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))  
        print(self._config.sections())
        
        #Windows Client only
        logdirectory = os.path.dirname(os.path.abspath(__file__)) + "\\log" #Funktioniert nicht als Exe, hier muss der Absolute Pfad hinein
        
        if not os.path.exists(logdirectory):
            os.makedirs(logdirectory)        

        logPath = logdirectory + "\\service-log.log"#Funktioniert nicht als Exe, hier muss der Absolute Pfad hinein

        self._logger = logging.getLogger("GensetTransmit")
        self._logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(logPath, maxBytes=4096, backupCount=10)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self._logger.info("Send stopp Request")
        

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))

        self._logger.info("Service Is Starting")

        self.main()

    def main(self):
        # your code could go here
        import Modbusread_client_v8
        import Modbusread_Pcount_V2
        import cmd_send
        import sqlite3
        import datetime
        import threading
        from datetime import date, time
        
        #Herstellen der Datenbankverbindung
        #try:
            #connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\settings.db") #Windows
            #cursor = connection.cursor()
            
        #except:
            #logger.info("problem with SQLite connection")
            #pass
        
        

        #Your code Here  
        while True:
            try:
                
                #Check and Send Reset Command
                cmd_send.modbussendreset()
                
                #Ausfuehren des Modbus Lese und Uebertragungsscript
                Modbusread_client_v8.modbusreadclient()

                t=threading.Thread(target=Modbusread_Pcount_V2.StartPcount,name='Modbuscount')
                t.setDaemon(True)
                t.start()
                
                #Starte die Leistungszaehlungsuebertragung
                #Modbusread_Pcount.StartPcount()
                
                if win32event.WaitForSingleObject(self.hWaitStop,10000) == win32event.WAIT_OBJECT_0:
                    self._logger.info("Service has been Stopped")
                    break
                
                else:
                    pass
                
            except IOError as e:
                self._logger.info("I/O error({0}): {1}".format(e.errno, e.strerror))
                           
            
           
if __name__ == '__main__':  
    win32serviceutil.HandleCommandLine(AppServerSvc)
