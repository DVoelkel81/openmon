#!/var/www/venv/bin/python

# -*- coding: utf-8 -*-

__author__ = "Dennis Voelkel"
__copyright__ = "Copyright 2019, Openmon"
__credits__ = ["Dennis Voelkel"]
__license__ = "MIT"  #
__version__ = "0.0.2"
__maintainer__ = "Dennis Voelkel"
__email__ = "dennis.voelkel@outlook.com"
__status__ = "Develop"

"""
xml-rpc transmission
"""

import random
import time
import logging
import sys
import os
import threading
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from logging.handlers import RotatingFileHandler

"""
Import python system functions
"""

import dataanalysis
"""
Import project functions
"""


#logPath = "/var/log/xml-rpc-omserver.log" #linux
logPath = "c:\\temp\\xml-rpc-omserver.log" #Mac
logger = logging.getLogger("xml-rpc-omserver")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=4096000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class LoggingSimpleXMLRPCRequestHandler(SimpleXMLRPCRequestHandler): 
    """Overides the default SimpleXMLRPCRequestHander to support logging.  Logs
    client IP and the XML request and response.
    """

    def do_POST(self):
        clientIP, port = self.client_address
        # Log client IP and Port
        logger.info('Client IP: %s - Port: %s' % (clientIP, port))
        try:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            # Filename to write
            filenameget = "c:\\temp\\xml-rpc-receive-" + timestr + ".xml"
            filenamesend = "c:\\temp\\xml-rpc-answere-" + timestr + ".xml"
                       
            
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            
            # Open the file with writing permission
            myfileget = open(filenameget, 'w')
            
            # Write a line to the file
            myfileget.write('%s' % data)
            
            # Close the file
            myfileget.close()             
            
            # Log client request
            #logger.info('Client request: \n%s\n' % data)

            response = self.server._marshaled_dispatch(
                data, getattr(self, '_dispatch', None)
            )
            # Log server response
            #logger.info('Server response: \n%s\n' % response)
            
            # Open the file with writing permission
            #myfilesend = open(filenamesend, 'w')
            
            # Write a line to the file
            #myfilesend.write('%s' % response)
            
            # Close the file
            #myfilesend.close()             
            

        except: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown(1)

class REMOTEMETHODS: 
    def hello(self, string):    
        return "Hello %s" % string



def logchp(chpdict):
    """
    Logging CHP values
    """
    
    try:

        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        #logger.info(len(data))
        t = threading.Thread(name='dataanalysis', target=dataanalysis.socketanalysis, args=(chpdict,))
        t.setDaemon(True)
        t.start()
        data = None

       
    except:
        logger.info('Error in Array or analysis function!')
        data = None
        pass    
    
    #print (chpdict.get('chpid'))
    
    returnval = "ok"
    return returnval
    
    

# run server
def run_server(host="localhost", port=8000):
    server_addr = (host, port)
    server = SimpleThreadedXMLRPCServer(server_addr,LoggingSimpleXMLRPCRequestHandler)
    remotemethod = REMOTEMETHODS()
    server.register_instance(remotemethod)
    server.register_function(logchp, 'logchp')
    
    logger.info("Server thread started.")
    logger.info('listening on {} port {}'.format(host, port))

    server.serve_forever()

#Run Script
if __name__ == '__main__':
    run_server()