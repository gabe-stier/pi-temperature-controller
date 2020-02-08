'''
Created on Feb 7, 2020

@author: gabez
'''
import socketserver
from FileHandler import info
from Main import __HOST
import threading

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
                            <td>""" + host[0] + """</td>
                            <td>""" + host[1] + """</td>
                            <td>""" + host[2] + """</td>
                        </tr>""" 
        html += """</table>
                        <style>table, th, td { border: 1px solid black;}</style>
                    </html>"""
        return html
    

show = socketserver.TCPServer(localAddr, HTTPHandler)
ts = threading.Thread(target=show.serve_forever())
ts.setDaemon(True)