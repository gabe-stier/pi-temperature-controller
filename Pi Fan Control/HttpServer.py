'''
Created on Feb 7, 2020

@author: gabez
'''
# coding: utf-8
import socketserver
import threading

from FileHandler import info, getTempAvg
from Main import __HOST

localAddr = (__HOST, 80)


class HTTPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.request.send(self.page().encode("utf-8"))
#        self.server.close()
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
                            <td>""" + str(host[0]) + """</td>
                            <td>""" + str(host[1]) +"""&degF</td>
                            <td>""" + str(host[2]) + """</td>
                        </tr>""" 
        html += """</table>
                    <br> <div>Average Temperature: """ + str(getTempAvg())  + """&degF</div>
                        <style>table, th, td { border: 1px solid black; text-align: center;}</style>
                    </html>"""
        return html
    

show = socketserver.TCPServer(localAddr, HTTPHandler)
ts = threading.Thread(target=show.serve_forever())
ts.setDaemon(True)
