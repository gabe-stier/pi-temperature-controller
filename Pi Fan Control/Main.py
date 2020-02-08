'''
Created on Feb 6, 2020

@author: gabez
'''
from multiprocessing import Pool
import os
from socket import socket


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


def run(process):
    os.system('python {}'.format(process))


__HOST = '127.0.0.1'


class Main():
    if __name__ == '__main__':
        processes = ('HttpServer.py', 'DataServer.py')
        pool = Pool(processes=2)
        pool.map(run, processes)
        pass
    
