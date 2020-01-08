#!/usr/bin/python3
# coding: utf8

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
    _svc_name_ = "Gensetreceive"
    _svc_display_name_ = "Genset receive"
    _svc_description_ = "Die Aufgabe des Service ist der Empfang von Serverbefehlen für den Gensetcontroller via UDP Socket"

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

        self._logger = logging.getLogger("Gensetreceive")
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
        import cmd_analyse
        import datetime
        import threading
        from datetime import date, time
        
        #create UDP Socket*
        #---------------------------------------------------
        UDP_IP = '' #Hier keine Adresse eintragen, damit der Broadcast empfangen werden kann. Keine Bindung zu einer IP-Addresse.
        UDP_PORT = 1203 #Codesys  Port im Netzwerk
                
        sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        
        sock.settimeout(5.0)
        
        #clientaddr = (UDP_IP, UDP_PORT) # Variable um IP-Addresse und Port Festzulegen.
        sock.bind((UDP_IP, UDP_PORT)) # Binden der IP und des Ports an das Socket.
                
        #logger.info("Socket online")
        #Abfrage der 
        while True:
            try:
                #self._logger.info("Wait for Message")                
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                self._logger.info("Receive Message Reset or Powerset")
                
                self._logger.info(str(data))
                datasize = len(data)
                t = threading.Thread(name='cmd_analysis', target=cmd_analyse.socketanalysis, args=(data,))
                t.setDaemon(True)
                t.start()
                data = None
                
            except socket.timeout:
                #self._logger.info("write timeout  socket")
                pass
        
            if win32event.WaitForSingleObject(self.hWaitStop,50) == win32event.WAIT_OBJECT_0:
                self._logger.info("Service has been Stopped")
                break
            
            else:
                pass             
            #except IOError as e:
               # self._logger.info("I/O error({0}): {1}".format(e.errno, e.strerror))
                #data = None
               #pass        
        
        
        """
        x = False
    
        #Abfrage der 
        while True:
            try:
                if x == False:
                    self._logger.info("running threat")
                    t = threading.Thread(name='receivereset', target=servicethread.receivereset)
                    t.setDaemon(True)
                    t.start()
                    x = True
                    
                else:
                    t.join(1)
                    x = t.isAlive()
                    #self._logger.info(x)
                    
                
                if win32event.WaitForSingleObject(self.hWaitStop,500) == win32event.WAIT_OBJECT_0:
                    self._logger.info("Service has been Stopped")
                    break
                
                else:
                    pass                
    
           
            except IOError as e:
                self._logger.info("I/O error({0}): {1}".format(e.errno, e.strerror))
                data = None
                pass        
        """
           
if __name__ == '__main__':  
    win32serviceutil.HandleCommandLine(AppServerSvc)
