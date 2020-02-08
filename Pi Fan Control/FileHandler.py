'''
Created on Feb 6, 2020

@author: gabez
'''
from datetime import datetime as __datetime
import json


def getHostName(ip):
    with open("hosts.json", "r") as __json_fileR:
        __host_file = json.load(__json_fileR)
        if str(ip) in __host_file:
            name = __host_file[str(ip)]["hostname"]
            return name
        else:
            return False


def addHostName(ip, hostname, temp):
    with open("hosts.json", "r") as __json_fileR:
        __host_file = json.load(__json_fileR)
        if(str(ip) not in __host_file):
            time = __datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            __host_file[str(ip)] = {
                "hostname": str(hostname),
                "address": str(ip),
                "last report": time,
                "temperature": temp
            }
            __saveFile(__host_file)
            return True
        else:
            return False


def setHostName(ip, hostname):
    with open("hosts.json", "r") as __json_fileR:
        __host_file = json.load(__json_fileR)
        if str(ip) in __host_file:
            if not checkHostName(ip, hostname):
                __host_file[str(ip)]["hostname"] = hostname
                __saveFile(__host_file)
                return True
        else:
            return False


def checkHostName(ip, hostname):
    stored_hostname = getHostName(ip)
    if (hostname.lower() == stored_hostname.lower()):
        return True
    else:
        return False


def __saveFile(__host_file):
    with open("hosts.json", 'w') as outfile:
        json.dump(__host_file, outfile)
    return True


def update(ip, time, temp):
    with open("hosts.json", "r") as __json_fileR:
        __host_file = json.load(__json_fileR)
        if(str(ip) in __host_file):
            __host_file[str(ip)]["last report"] = time
            __host_file[str(ip)]["temperature"] = temp
            __saveFile(__host_file)
            return True
        else:
            return False 


def info():
    with open("hosts.json", "r") as __json_fileR:
        __host_file = json.load(__json_fileR)
        # print(json.dumps(__host_file, indent=4))
        info = []
        for host in __host_file:
            info.append((__host_file[host]["hostname"], __host_file[host]["temperature"], __host_file[host]["last report"]))
    return info

    
def getTempAvg():
    with open("hosts.json", "r") as __json_fileR:
        __host_file = json.load(__json_fileR)
        temp = 0
        count = 0
        for host in __host_file:
            temp += __host_file[host]["temperature"] 
            count += 1
        if count is not 0:
            return float(temp / count)
        else: 
            return 0
