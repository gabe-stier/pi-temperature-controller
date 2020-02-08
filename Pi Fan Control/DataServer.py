'''
Created on Feb 6, 2020

@author: gabez
'''

from datetime import datetime
import hashlib
import json
import logging
import socket
import socketserver
import threading

from FileHandler import *
from Main import __HOST

__PORT = 34289
localAddrPi = (__HOST, __PORT)


class DataHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).decode('utf-8')
        addr = self.client_address
        print(data)
        ip = addr[0]
        info = json.loads(str(data))
        if(str(ip) == info["data"]["address"] and self.__checkHash(info["data"]["date"], info["data"]["checksum"], info["data"]["code"])):
            hostname = info["data"]["hostname"]
            temp = info["data"]["temperature"]
            if not getHostName(ip):
                addHostName(ip, hostname, temp)
            else:
                if not checkHostName(ip, hostname):
                    setHostName(ip, hostname)
                update(ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), temp)
        return 
    
    def __checkHash(self, date, checksum, code):
        size = int(len(date) / 2)
        dc1 = date[0:size]
        dc2 = date[size:-1]
        dc = (str(dc1), str(code), str(dc2))
        cSum = hashlib.md5(str(dc).encode()).hexdigest()
        if(checksum == cSum):
            return True
        else:
            return False


server = socketserver.TCPServer(localAddrPi, DataHandler)
t = threading.Thread(target=server.serve_forever())
t.setDaemon(True)
print("DataServer starting")
t.start()
