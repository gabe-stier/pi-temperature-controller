'''
Created on Feb 6, 2020

@author: gabez
'''
from datetime import datetime as __datetime
import json

__json_fileR = open("hosts.json", "r")
__host_file = json.load(__json_fileR)


def getHostName(ip):
    if str(ip) in __host_file:
        name = __host_file[str(ip)]["hostname"]
        return name
    else:
        return False


def addHostName(ip, hostname, temp):
    if(str(ip) not in __host_file):
        time = __datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        __host_file[str(ip)] = {
            "hostname": str(hostname),
            "address": str(ip),
            "last report": time,
            "temperature": temp
        }
        __saveFile()
        return True
    else:
        return False


def setHostName(ip, hostname):
    if str(ip) in __host_file:
        if not checkHostName(ip, hostname):
            __host_file[str(ip)]["name"] = hostname
            __saveFile()
            return True
    else:
        return False


def checkHostName(ip, hostname):
    stored_hostname = getHostName(ip)
    if (hostname.lower() == stored_hostname.lower()):
        return True
    else:
        return False


def __saveFile():
    json_fileW = open("hosts.json", 'w')
    json_fileW.write(json.dump(__host_file, indent=4))
    json_fileW.close()
    return True


def update(ip, time, temp):
    if(str(ip) in __host_file):
        __host_file[str(ip)]["last report"] = time
        __host_file[str(ip)]["temperature"] = temp
        __saveFile()
        return True
    else:
        return False 


def info():
    info = []
    for host in __host_file:
        info.append((__host_file[host]["hostname"], __host_file[host]["temperature"], __host_file[host]["last report"]))
    return info
    
