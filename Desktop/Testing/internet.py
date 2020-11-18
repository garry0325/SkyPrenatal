import sys
import time
import bluetooth
import socket
import threading
from multiprocessing import Queue
from PyQt4 import QtGui,QtCore



remoteIP="192.168.31.180"
remotePort=8000


def sendData(IPAddress,port,dataToSend):
    skt=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    while True:
        try:
            skt.connect((IPAddress,port));
            print "Connected..."
            break
        except Exception:
            print "Connection failed...Retry"
            time.sleep(5)
            continue
    first=0
    while True:
        skt.send(dataToSend)
        data=skt.recv(64)
        print data
        if data==dataToSend and first:
            break
        first=1
    skt.close()


sendData(remoteIP,remotePort,"45.56")
