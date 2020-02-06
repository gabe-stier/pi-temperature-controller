'''
Created on Feb 6, 2020

@author: gabez
'''

from datetime import datetime
import hashlib
import http.server
import json
import logging
import socketserver
import socket
import threading

from FileHandler import *


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('1.1.1.1', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


__HOST = get_ip()
__PORT = "34289"
localAddrPi = (__HOST, __PORT)
localAddr = (__HOST, 80)


class DataHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).decode('utf-8')
        addr = self.client_address
        ip = addr[0]
        info = json.load(data)
        if(str(ip) == info["data"]["address"] and self.__checkHash(info["data"]["date"], info["data"]["checksum"], info["data"]["code"])):
            hostname = info["data"]["hostname"]
            temp = info["data"]["temperature"]
            if not getHostName(ip):
                addHostName(ip, hostname, temp)
            else:
                if not checkHostName(ip, hostname):
                    setHostName(ip, hostname)
                update(ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), temp)
                
        self.server.close()
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


class HTTPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.request.send(self.page())
        self.server.close()
        return

    def page(self): 
        html = """<html><head><title>Pi Temperatures</title></head>
                    <table>
                        <tr>
                            <th>Host Name</th>
                            <th>Temperature</th>
                            <th>Last Update</th>
                        </tr>"""
        for host in info():
            html += """ <tr>
                            <td>""" + host[0] + """</td>
                            <td>""" + host[1] + """</td>
                            <td>""" + host[2] + """</td>
                        </tr>""" 
        html += """</table>
                        <style>table, th, td { border: 1px solid black;}</style>
                    </html>"""
        return html


def start():
    server = socketserver.TCPServer(localAddrPi, DataHandler)
    t = threading.Thread(target=server.serve_forever())
    t.setDaemon(True)
    t.start()
    show = socketserver.TCPServer(localAddr, HTTPHandler)
    ts = threading.Thread(target=show.serve_forever())
    ts.setDaemon(True)
    ts.start()
    
    
