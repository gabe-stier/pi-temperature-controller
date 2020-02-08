'''
Created on Feb 7, 2020

@author: gabez
'''
import socketserver
import threading

from FileHandler import info, getTempAvg
from Main import __HOST

localAddr = (__HOST, 80)


class HTTPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.request.send(self.page().encode("utf-8"))
        return

    def page(self): 
        html = """<html><head><meta http-equiv="refresh" content="300" ><title>Pi Temperatures</title></head>
                    <table>
                        <tr>
                            <th>Host Name</th>
                            <th>Temperature</th>
                            <th>Last Update</th>
                        </tr>"""
        for host in info():
            html += """ <tr>
                            <td>""" + str(host[0]) + """</td>
                            <td>""" + "{0:.2f}".format(host[1]) +"""&degF</td>
                            <td>""" + str(host[2]) + """</td>
                        </tr>""" 
        html += """</table>
                    <br> <div>Average Temperature: """ + "{0:.2f}".format(getTempAvg())  + """&degF</div><div>Updated time: <script> var today = new Date();var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();var dateTime = date+' '+time; document.write(dateTime)</script>
                        <style>table, th, td { border: 1px solid black; text-align: center;}</style>
                    </html>"""
        return html
    

show = socketserver.TCPServer(localAddr, HTTPHandler)
ts = threading.Thread(target=show.serve_forever())
ts.setDaemon(True)
