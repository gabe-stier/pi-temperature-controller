'''
Created on Feb 6, 2020

@author: gabez
'''

import socketserver
import json
import logging
import datetime
import http.server
from FileHandler import *


class Server(object):

    def __init__(self, params):
        self.run()

    def run(self):
        pass

    def listen(self):
        pass

    def post(self):
        pass


class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        data = self.request.recv(1024).decode('utf-8')
        addr = self.client_address
        ip = addr[0]
        info = json.load(data)
        if(str(ip) == info["data"]["address"] and hash(info["data"]["date"], info["data"]["checksum"], info["data"]["code"])):
            hostname = info["data"]["hostname"]
            temp = info["data"]["temperature"]
            if not getHostName(ip):
                addHostName(ip, hostname, temp)
            else:
                if not checkHostName(ip, hostname):
                    setHostName(ip, hostname)

    def hash(self, date, checksum, code):
        date_code = id(date)
        size = len(date_code)/2

        return True
        return False
