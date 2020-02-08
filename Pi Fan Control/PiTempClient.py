'''
Created on Feb 8, 2020

@author: gabez
'''
from datetime import datetime
import hashlib
import json
import random
import socket
import time


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('1.1.1.1', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


host = get_ip()
hostname = socket.gethostname()


def getTemp():
    tFile = open('/sys/class/thermal/thermal_zone0/temp')
    temp = float(tFile.read())
    tempF = (temp / 1000) * (9 / 5) + 32
    return tempF


def checkSum(date, code):
    size = int(len(date) / 2)
    dc1 = date[0:size]
    dc2 = date[size:-1]
    dc = (str(dc1), str(code), str(dc2))
    cSum = hashlib.md5(str(dc).encode()).hexdigest()
    return cSum


def message():
    code = random.random() * 10
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    jsonMsg = {  "data":
                { 
                    "address": host,
                    "hostname":hostname,
                    "temperature":getTemp(),
                    "date" :date,
                    "code" : code,
                    "checksum" : checkSum(date, code)
                } 
              }
    return jsonMsg


def connect():

    s = socket.socket()
    try:
        s.connect(("192.168.0.14", 34289))
        message2 = message()
        s.send(json.dumps(message2).encode("utf-8"))
        s.close()
    except socket.error as msg:
        print("Could not connect to the controller")
        print(msg)


class PiTempClient():
    if __name__ == '__main__':
        while True:
            connect()
            time.sleep(60 * 5)
        pass
