'''
Created on Feb 6, 2020

@author: gabez
'''

import time
import threading
from FileHandler import getTempAvg

__fans_running = False


def __init__():
    while(True):
        avg = getTempAvg()
        
        if(avg >= 95):
            if not __fans_running:
                __start_fans()
        else:
            if __fans_running:
                __stop_fans()
#         time.sleep(60)


def __start_fans():
    print("Starting Fans")
    return


def __stop_fans():
    print("Stopping Fans")
    return


fs = threading.Thread(targe=__init__())
fs.setDaemon(True)
